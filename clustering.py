"""
Module for clustering embeddings using HDBSCAN with KMeans fallback.
"""
import logging
from typing import Tuple
import numpy as np
from sqlalchemy.orm import Session
from sklearn.cluster import HDBSCAN, KMeans
from sklearn.metrics import silhouette_score

from models import Insight

logger = logging.getLogger(__name__)


def cluster_embeddings(embeddings: np.ndarray) -> Tuple[np.ndarray, int]:
    """
    Cluster embeddings using HDBSCAN, with fallback to KMeans if needed.
    
    Args:
        embeddings: NumPy array of shape (n_samples, embedding_dim)
        
    Returns:
        Tuple of (cluster_labels, n_clusters) where:
        - cluster_labels: array of cluster assignments (same length as embeddings)
        - n_clusters: number of clusters found
        
    Raises:
        ValueError: If embeddings array is empty or invalid
    """
    if embeddings.size == 0:
        raise ValueError("Embeddings array cannot be empty")
    
    if len(embeddings.shape) != 2:
        raise ValueError(f"Embeddings must be 2D, got shape {embeddings.shape}")
    
    n_samples = embeddings.shape[0]
    logger.info(f"Starting clustering on {n_samples} embeddings...")
    
    # Try HDBSCAN first
    try:
        logger.info("Attempting HDBSCAN clustering...")
        clusterer = HDBSCAN(min_cluster_size=max(5, n_samples // 10), min_samples=1)
        labels = clusterer.fit_predict(embeddings)
        
        # Count clusters (excluding noise label -1)
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        
        # HDBSCAN succeeded if we have at least 2 clusters
        if n_clusters >= 2:
            logger.info(f"HDBSCAN succeeded: {n_clusters} clusters found")
            return labels, n_clusters
        else:
            logger.warning(f"HDBSCAN produced fewer than 2 clusters ({n_clusters}), falling back to KMeans")
    except Exception as e:
        logger.warning(f"HDBSCAN failed: {str(e)}, falling back to KMeans")
    
    # Fallback to KMeans with silhouette score optimization
    logger.info("Using KMeans with silhouette score optimization (k=2 to 10)...")
    
    # Determine max k
    max_k = min(10, n_samples - 1) if n_samples > 1 else 2
    
    best_k = 2
    best_score = -1
    
    for k in range(2, max_k + 1):
        try:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels_k = kmeans.fit_predict(embeddings)
            score = silhouette_score(embeddings, labels_k)
            
            logger.info(f"k={k}: silhouette_score={score:.4f}")
            
            if score > best_score:
                best_score = score
                best_k = k
        except Exception as e:
            logger.warning(f"KMeans with k={k} failed: {str(e)}")
            continue
    
    logger.info(f"Best k={best_k} with silhouette_score={best_score:.4f}")
    
    # Final KMeans with best k
    kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(embeddings)
    
    logger.info(f"KMeans completed: {best_k} clusters")
    return labels, best_k


def get_cluster_assignments(embeddings: np.ndarray, db: Session) -> Tuple[np.ndarray, int]:
    """
    Get cluster assignments for embeddings, computing new ones if needed.
    Updates the database with theme_id (cluster assignments).
    
    Args:
        embeddings: NumPy array of embeddings (must match order from get_embeddings_for_clustering)
        db: Database session
        
    Returns:
        Tuple of (cluster_labels, n_clusters)
    """
    # Run clustering
    cluster_labels, n_clusters = cluster_embeddings(embeddings)
    
    # Update database with cluster assignments
    insights = db.query(Insight).filter(Insight.embedding != None).all()
    
    logger.info(f"Updating {len(insights)} insights with cluster assignments...")
    
    for idx, insight in enumerate(insights):
        insight.theme_id = int(cluster_labels[idx])
    
    db.commit()
    logger.info("Cluster assignments saved to database.")
    
    return cluster_labels, n_clusters


def get_cluster_samples(texts: list[str], cluster_labels: np.ndarray, n_clusters: int, samples_per_cluster: int = 3) -> list[dict]:
    """
    Extract sample texts from each cluster.
    
    Args:
        texts: List of text strings corresponding to embeddings
        cluster_labels: Cluster assignment for each text
        n_clusters: Number of clusters
        samples_per_cluster: Number of samples to extract per cluster (default 3)
        
    Returns:
        List of dicts with cluster_id, size, and samples
    """
    cluster_info = []
    
    for cluster_id in range(n_clusters):
        # Find indices in this cluster
        cluster_indices = np.where(cluster_labels == cluster_id)[0]
        cluster_size = len(cluster_indices)
        
        # Get samples (up to samples_per_cluster)
        sample_indices = np.random.choice(
            cluster_indices,
            size=min(samples_per_cluster, cluster_size),
            replace=False
        )
        samples = [texts[idx] for idx in sample_indices]
        
        cluster_info.append({
            "cluster_id": int(cluster_id),
            "size": int(cluster_size),
            "samples": samples
        })
    
    return cluster_info
