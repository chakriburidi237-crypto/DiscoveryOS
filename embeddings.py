"""
Module for generating and storing embeddings using sentence-transformers.
"""
import logging
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session

from models import RawInput, Insight

logger = logging.getLogger(__name__)

# Initialize the model globally to avoid reloading
_model = None


def get_embedding_model():
    """
    Lazy-load the sentence-transformers model.
    Uses all-MiniLM-L6-v2 for fast, lightweight embeddings.
    """
    global _model
    if _model is None:
        logger.info("Loading sentence-transformers model (all-MiniLM-L6-v2)...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        logger.info("Model loaded successfully.")
    return _model


def embed_texts(texts: List[str]) -> np.ndarray:
    """
    Generate embeddings for a list of texts using sentence-transformers.
    
    Args:
        texts: List of text strings to embed
        
    Returns:
        NumPy array of shape (len(texts), 384) containing embeddings
        
    Raises:
        ValueError: If texts list is empty
    """
    if not texts:
        raise ValueError("texts list cannot be empty")
    
    model = get_embedding_model()
    logger.info(f"Generating embeddings for {len(texts)} texts...")
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    logger.info(f"Generated embeddings with shape: {embeddings.shape}")
    
    return embeddings


def process_unprocessed_inputs(db: Session, force: bool = False) -> int:
    """
    Process unprocessed raw inputs: generate embeddings and store in insights table.
    
    Args:
        db: Database session
        force: If True, reprocess all inputs; otherwise only process rows without embeddings
        
    Returns:
        Number of insights processed
        
    Raises:
        Exception: If database operations fail
    """
    try:
        if force:
            # Reprocess all: clear existing embeddings
            logger.info("Force reprocessing: clearing all existing embeddings...")
            db.query(Insight).update({Insight.embedding: None})
            db.commit()
        
        # Query raw_inputs that don't have corresponding insights with embeddings
        unprocessed_inputs = db.query(RawInput).all()
        
        if not unprocessed_inputs:
            logger.info("No raw inputs found to process.")
            return 0
        
        logger.info(f"Found {len(unprocessed_inputs)} raw input(s) to process.")
        
        # Extract text and prepare for embedding
        texts_to_embed = []
        raw_input_ids = []
        
        for raw_input in unprocessed_inputs:
            # Check if this raw_input already has an insight with an embedding
            existing_insight = db.query(Insight).filter(
                Insight.raw_input_id == raw_input.id,
                Insight.embedding != None
            ).first()
            
            if existing_insight is None:
                texts_to_embed.append(raw_input.raw_text)
                raw_input_ids.append(raw_input.id)
        
        if not texts_to_embed:
            logger.info("All raw inputs already have embeddings.")
            return 0
        
        logger.info(f"Processing {len(texts_to_embed)} new embeddings...")
        
        # Generate embeddings
        embeddings = embed_texts(texts_to_embed)
        
        # Store embeddings in the database
        processed_count = 0
        for idx, (raw_input_id, embedding) in enumerate(zip(raw_input_ids, embeddings)):
            # Convert embedding to bytes for storage
            embedding_bytes = embedding.astype(np.float32).tobytes()
            
            # Check if insight exists, if not create it
            insight = db.query(Insight).filter(Insight.raw_input_id == raw_input_id).first()
            if insight is None:
                insight = Insight(raw_input_id=raw_input_id)
                db.add(insight)
                db.flush()
            
            # Update embedding
            insight.embedding = embedding_bytes
            db.commit()
            processed_count += 1
        
        logger.info(f"Successfully processed {processed_count} embeddings.")
        return processed_count
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error processing unprocessed inputs: {str(e)}")
        raise


def get_embeddings_for_clustering(db: Session) -> tuple[np.ndarray, List[int]]:
    """
    Retrieve all embeddings from the database for clustering.
    
    Args:
        db: Database session
        
    Returns:
        Tuple of (embeddings array, insight_ids list)
        
    Raises:
        ValueError: If no embeddings found
    """
    insights = db.query(Insight).filter(Insight.embedding != None).all()
    
    if not insights:
        raise ValueError("No embeddings available for clustering")
    
    logger.info(f"Retrieved {len(insights)} embeddings from database.")
    
    embeddings_list = []
    insight_ids = []
    
    for insight in insights:
        # Convert bytes back to numpy array
        embedding = np.frombuffer(insight.embedding, dtype=np.float32)
        embeddings_list.append(embedding)
        insight_ids.append(insight.id)
    
    embeddings_array = np.array(embeddings_list)
    logger.info(f"Embeddings shape: {embeddings_array.shape}")
    
    return embeddings_array, insight_ids
