"""
Module for LLM-based theme labeling of text clusters.
Supports OpenAI (GPT-4/3.5) and Anthropic (Claude) providers.
"""
import logging
import os
import json
import re
from typing import List, Optional, Dict
from collections import Counter

logger = logging.getLogger(__name__)


def get_llm_provider() -> str:
    """
    Get the configured LLM provider from environment variables.
    
    Returns:
        LLM provider name: "openai" or "anthropic"
    """
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    if provider not in ["openai", "anthropic"]:
        logger.warning(f"Invalid LLM_PROVIDER '{provider}', defaulting to 'openai'")
        return "openai"
    return provider


def get_llm_model() -> str:
    """
    Get the configured LLM model from environment variables.
    
    Returns:
        Model name for the provider
    """
    return os.getenv("LLM_MODEL", "gpt-3.5-turbo")


def extract_keywords(texts: List[str], num_keywords: int = 5) -> List[str]:
    """
    Extract the most common keywords from a list of texts.
    Used as fallback when LLM fails.
    
    Args:
        texts: List of text samples
        num_keywords: Number of top keywords to extract
        
    Returns:
        List of top keywords
    """
    # Simple word-level frequency analysis
    words = []
    stop_words = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "is", "are", "was", "be", "that", "this",
        "it", "as", "we", "they", "you", "i", "my", "our", "their", "more",
        "can", "could", "should", "would", "do", "does", "did", "have", "has",
        "had", "will", "just", "very", "much", "too", "also", "its"
    }
    
    for text in texts:
        # Convert to lowercase and split
        text_words = text.lower().split()
        for word in text_words:
            # Remove punctuation and filter
            clean_word = re.sub(r'[^\w]', '', word)
            if len(clean_word) > 3 and clean_word not in stop_words:
                words.append(clean_word)
    
    if not words:
        return ["content", "feedback"]
    
    # Get most common
    counter = Counter(words)
    top_words = [word for word, _ in counter.most_common(num_keywords)]
    
    return top_words if top_words else ["content", "feedback"]


def fallback_theme_generation(texts: List[str]) -> Dict[str, Optional[str]]:
    """
    Generate a simple theme when LLM fails.
    Extracts keywords and creates a basic name.
    
    Args:
        texts: List of sample texts from the cluster
        
    Returns:
        Dictionary with theme_name, summary, and segment (optional)
    """
    logger.info("Using fallback theme generation")
    
    keywords = extract_keywords(texts, num_keywords=3)
    theme_name = " - ".join(keywords[:2]).title()
    
    # Create summary from first text
    summary = texts[0][:100].strip() + "..."
    
    return {
        "theme_name": theme_name if theme_name else "Unclassified Feedback",
        "summary": summary,
        "segment": None
    }


def parse_llm_response(response_text: str) -> Optional[Dict[str, Optional[str]]]:
    """
    Parse the LLM response to extract theme name, summary, and segment.
    
    Args:
        response_text: Raw response from LLM (expected to contain JSON)
        
    Returns:
        Dictionary with keys: theme_name, summary, segment
        Returns None if parsing fails
    """
    try:
        # Try to extract JSON from response
        # Look for JSON object in the response
        json_match = re.search(r'\{[^{}]*\}', response_text, re.DOTALL)
        
        if not json_match:
            logger.warning("No JSON found in LLM response")
            return None
        
        json_str = json_match.group(0)
        parsed = json.loads(json_str)
        
        # Extract fields
        theme_name = parsed.get("theme_name") or parsed.get("name") or ""
        summary = parsed.get("summary") or parsed.get("description") or ""
        segment = parsed.get("segment") or parsed.get("user_segment") or None
        
        # Validate fields
        if not theme_name or not summary:
            logger.warning("Missing required fields in LLM response")
            return None
        
        # Limit length
        theme_name = str(theme_name)[:100].strip()
        summary = str(summary)[:500].strip()
        segment = str(segment)[:100].strip() if segment else None
        
        return {
            "theme_name": theme_name,
            "summary": summary,
            "segment": segment
        }
    
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from LLM response: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Error parsing LLM response: {str(e)}")
        return None


def label_cluster_with_openai(samples: List[str]) -> Optional[Dict[str, Optional[str]]]:
    """
    Send cluster samples to OpenAI API and get theme labeling.
    
    Args:
        samples: List of text samples from the cluster
        
    Returns:
        Dictionary with theme_name, summary, segment, or None if failed
    """
    try:
        import openai
    except ImportError:
        logger.error("openai package not installed. Install with: pip install openai")
        return None
    
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        logger.error("LLM_API_KEY not configured for OpenAI")
        return None
    
    try:
        openai.api_key = api_key
        model = get_llm_model()
        
        # Prepare sample text
        sample_text = "\n\n".join([f"[Sample {i+1}]: {sample[:200]}" for i, sample in enumerate(samples[:5])])
        
        prompt = f"""Analyze these customer feedback texts and categorize them into a theme:

{sample_text}

Respond with ONLY a JSON object (no markdown, no extra text):
{{
  "theme_name": "Brief theme name (2-4 words)",
  "summary": "One-sentence summary of what users are saying",
  "segment": "Target user segment if identifiable (e.g., 'product managers', 'end users', 'support team') or null"
}}"""
        
        logger.info(f"Calling OpenAI API with model {model}...")
        
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a product research analyst. Analyze customer feedback and extract themes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500,
            timeout=30
        )
        
        response_text = response.choices[0].message.content
        logger.info(f"OpenAI response: {response_text[:100]}...")
        
        parsed = parse_llm_response(response_text)
        return parsed
    
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {str(e)}")
        return None


def label_cluster_with_anthropic(samples: List[str]) -> Optional[Dict[str, Optional[str]]]:
    """
    Send cluster samples to Anthropic Claude API and get theme labeling.
    
    Args:
        samples: List of text samples from the cluster
        
    Returns:
        Dictionary with theme_name, summary, segment, or None if failed
    """
    try:
        import anthropic
    except ImportError:
        logger.error("anthropic package not installed. Install with: pip install anthropic")
        return None
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        logger.error("ANTHROPIC_API_KEY not configured")
        return None
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
        model = get_llm_model()
        
        # Prepare sample text
        sample_text = "\n\n".join([f"[Sample {i+1}]: {sample[:200]}" for i, sample in enumerate(samples[:5])])
        
        prompt = f"""Analyze these customer feedback texts and categorize them into a theme:

{sample_text}

Respond with ONLY a JSON object (no markdown, no extra text):
{{
  "theme_name": "Brief theme name (2-4 words)",
  "summary": "One-sentence summary of what users are saying",
  "segment": "Target user segment if identifiable (e.g., 'product managers', 'end users', 'support team') or null"
}}"""
        
        logger.info(f"Calling Anthropic API with model {model}...")
        
        response = client.messages.create(
            model=model,
            max_tokens=500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = response.content[0].text
        logger.info(f"Anthropic response: {response_text[:100]}...")
        
        parsed = parse_llm_response(response_text)
        return parsed
    
    except Exception as e:
        logger.error(f"Error calling Anthropic API: {str(e)}")
        return None


def label_cluster_with_llm(samples: List[str], llm_provider: Optional[str] = None) -> Dict[str, Optional[str]]:
    """
    Send cluster samples to LLM and get theme labeling.
    Falls back to simple text-based naming if LLM fails.
    
    Args:
        samples: List of text samples from the cluster
        llm_provider: "openai" or "anthropic" (uses env default if not specified)
        
    Returns:
        Dictionary with keys:
        - theme_name: Short theme name (2-4 words)
        - summary: One-sentence summary
        - segment: User segment if inferable, or None
    """
    if not samples:
        logger.warning("No samples provided for theme labeling")
        return {
            "theme_name": "Empty Cluster",
            "summary": "No data available",
            "segment": None
        }
    
    # Determine provider
    provider = (llm_provider or get_llm_provider()).lower()
    
    logger.info(f"Labeling cluster with {len(samples)} samples using {provider}")
    
    # Call appropriate LLM
    result = None
    if provider == "anthropic":
        result = label_cluster_with_anthropic(samples)
    else:  # default to openai
        result = label_cluster_with_openai(samples)
    
    # Use fallback if LLM fails
    if result is None:
        logger.warning(f"LLM failed, using fallback theme generation")
        result = fallback_theme_generation(samples)
    
    return result
