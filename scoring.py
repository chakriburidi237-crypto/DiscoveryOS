"""
Module for scoring themes by business impact and calculating priority scores.
"""
import logging
import os
import json
import re
from typing import List, Optional, Dict
from collections import Counter
from datetime import datetime

logger = logging.getLogger(__name__)

# Keyword mappings for fallback scoring
CRITICAL_KEYWORDS = {"crash", "error", "broken", "fail", "down", "blocked", "unable", "broken"}
HIGH_KEYWORDS = {"slow", "performance", "lag", "hang", "freeze", "stuck", "timeout"}
MEDIUM_KEYWORDS = {"improve", "enhance", "better", "should", "could", "need"}
LOW_KEYWORDS = {"nice", "want", "like", "prefer", "would", "feature"}


def get_llm_provider() -> str:
    """Get configured LLM provider."""
    return os.getenv("LLM_PROVIDER", "openai").lower()


def get_llm_model() -> str:
    """Get configured LLM model."""
    return os.getenv("LLM_MODEL", "gpt-3.5-turbo")


def extract_score_from_response(response_text: str) -> Optional[float]:
    """
    Extract business impact score from LLM response.
    Expects JSON with 'business_impact' field (1-5 float).
    
    Args:
        response_text: LLM response text
        
    Returns:
        Score between 1-5, or None if parsing fails
    """
    try:
        # Try to find JSON in response
        json_match = re.search(r'\{[^{}]*\}', response_text, re.DOTALL)
        if not json_match:
            logger.warning("No JSON found in LLM response")
            return None
        
        parsed = json.loads(json_match.group(0))
        score = parsed.get("business_impact")
        
        if score is None:
            logger.warning("No business_impact field in LLM response")
            return None
        
        # Validate score is between 1-5
        score = float(score)
        if not (1.0 <= score <= 5.0):
            logger.warning(f"Score {score} outside 1-5 range, clamping")
            score = max(1.0, min(5.0, score))
        
        return round(score, 2)
    
    except (json.JSONDecodeError, ValueError, AttributeError) as e:
        logger.error(f"Failed to parse score from response: {str(e)}")
        return None


def score_with_openai(summary: str, segment: Optional[str]) -> Optional[float]:
    """
    Score theme business impact using OpenAI API.
    
    Args:
        summary: Theme summary text
        segment: Target user segment
        
    Returns:
        Business impact score (1-5), or None if failed
    """
    try:
        import openai
    except ImportError:
        logger.error("openai package not installed")
        return None
    
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        logger.error("LLM_API_KEY not configured for OpenAI")
        return None
    
    try:
        openai.api_key = api_key
        model = get_llm_model()
        
        segment_text = f"Target Segment: {segment}" if segment else "Target Segment: Not specified"
        
        prompt = f"""Estimate business impact (1-5) for this customer feedback theme:

Summary: {summary}
{segment_text}

Respond with ONLY a JSON object (no markdown, no extra text):
{{
  "business_impact": 3.5,
  "reasoning": "Brief explanation"
}}

Scale:
1 = Nice-to-have (cosmetic improvements)
2 = Low-medium (minor improvements)
3 = Medium (moderate improvements, affects workflow)
4 = High (significant issue, affects many users)
5 = Critical (blocks usage, major business impact)"""
        
        logger.info(f"Calling OpenAI API for business impact scoring...")
        
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a product analyst. Score customer feedback themes by business impact (1-5 scale)."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=200,
            timeout=30
        )
        
        response_text = response.choices[0].message.content
        score = extract_score_from_response(response_text)
        
        if score:
            logger.info(f"OpenAI scored theme: {score}")
        
        return score
    
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {str(e)}")
        return None


def score_with_anthropic(summary: str, segment: Optional[str]) -> Optional[float]:
    """
    Score theme business impact using Anthropic Claude API.
    
    Args:
        summary: Theme summary text
        segment: Target user segment
        
    Returns:
        Business impact score (1-5), or None if failed
    """
    try:
        import anthropic
    except ImportError:
        logger.error("anthropic package not installed")
        return None
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        logger.error("ANTHROPIC_API_KEY not configured")
        return None
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
        model = get_llm_model()
        
        segment_text = f"Target Segment: {segment}" if segment else "Target Segment: Not specified"
        
        prompt = f"""Estimate business impact (1-5) for this customer feedback theme:

Summary: {summary}
{segment_text}

Respond with ONLY a JSON object (no markdown, no extra text):
{{
  "business_impact": 3.5,
  "reasoning": "Brief explanation"
}}

Scale:
1 = Nice-to-have (cosmetic improvements)
2 = Low-medium (minor improvements)
3 = Medium (moderate improvements, affects workflow)
4 = High (significant issue, affects many users)
5 = Critical (blocks usage, major business impact)"""
        
        logger.info(f"Calling Anthropic API for business impact scoring...")
        
        response = client.messages.create(
            model=model,
            max_tokens=200,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = response.content[0].text
        score = extract_score_from_response(response_text)
        
        if score:
            logger.info(f"Anthropic scored theme: {score}")
        
        return score
    
    except Exception as e:
        logger.error(f"Error calling Anthropic API: {str(e)}")
        return None


def fallback_impact_score(summary: str, segment: Optional[str]) -> float:
    """
    Fallback scoring when LLM unavailable.
    Uses keyword extraction and frequency analysis.
    
    Args:
        summary: Theme summary text
        segment: Target user segment
        
    Returns:
        Business impact score (1-5)
    """
    logger.info("Using fallback business impact scoring")
    
    summary_lower = summary.lower()
    
    # Count keyword matches by severity
    scores = []
    
    # Critical issues (5 points)
    critical_count = sum(1 for kw in CRITICAL_KEYWORDS if kw in summary_lower)
    scores.extend([5.0] * critical_count)
    
    # High impact (4 points)
    high_count = sum(1 for kw in HIGH_KEYWORDS if kw in summary_lower)
    scores.extend([4.0] * high_count)
    
    # Medium impact (3 points)
    medium_count = sum(1 for kw in MEDIUM_KEYWORDS if kw in summary_lower)
    scores.extend([3.0] * medium_count)
    
    # Low impact (2 points)
    low_count = sum(1 for kw in LOW_KEYWORDS if kw in summary_lower)
    scores.extend([2.0] * low_count)
    
    # Calculate average score
    if scores:
        base_score = sum(scores) / len(scores)
    else:
        base_score = 2.5  # Default for no keywords
    
    # Adjust based on segment
    if segment:
        segment_lower = segment.lower()
        # Support/bug reports get +1
        if any(word in segment_lower for word in ["support", "bug", "issue", "error"]):
            base_score = min(5.0, base_score + 0.5)
        # Feature requests get -0.5
        elif any(word in segment_lower for word in ["feature", "request", "enhancement"]):
            base_score = max(1.0, base_score - 0.5)
    
    final_score = round(min(5.0, max(1.0, base_score)), 2)
    logger.info(f"Fallback score calculated: {final_score}")
    
    return final_score


def estimate_business_impact(summary: str, segment: Optional[str] = None) -> float:
    """
    Estimate business impact of a theme (1-5 scale).
    Uses LLM if available, falls back to keyword analysis.
    
    Args:
        summary: Theme summary
        segment: Target user segment (optional)
        
    Returns:
        Business impact score (1-5)
    """
    if not summary or not summary.strip():
        logger.warning("Empty summary provided for scoring")
        return 2.5
    
    # Try LLM first
    provider = get_llm_provider()
    score = None
    
    if provider == "anthropic":
        score = score_with_anthropic(summary, segment)
    else:  # default to openai
        score = score_with_openai(summary, segment)
    
    # Fallback if LLM failed
    if score is None:
        score = fallback_impact_score(summary, segment)
    
    return score


def calculate_priority_score(insight_count: int, business_impact: float) -> float:
    """
    Calculate priority score = frequency * business_impact.
    
    Args:
        insight_count: Number of insights/feedback items
        business_impact: Business impact score (1-5)
        
    Returns:
        Priority score (higher = more important)
    """
    if insight_count <= 0 or business_impact <= 0:
        return 0.0
    
    priority = insight_count * business_impact
    return round(priority, 2)


def score_themes(db_session) -> Dict:
    """
    Score all unscored themes in the database.
    
    Args:
        db_session: Database session
        
    Returns:
        Dictionary with scoring results
    """
    from models import Theme
    
    try:
        # Get all unscored themes
        unscored_themes = db_session.query(Theme).filter(
            Theme.business_impact == None
        ).all()
        
        logger.info(f"Found {len(unscored_themes)} unscored themes")
        
        scored_count = 0
        for theme in unscored_themes:
            # Score the theme
            business_impact = estimate_business_impact(theme.summary, theme.segment)
            priority_score = calculate_priority_score(theme.insight_count, business_impact)
            
            # Update theme
            theme.business_impact = business_impact
            theme.priority_score = priority_score
            theme.scored_at = datetime.utcnow()
            
            scored_count += 1
            logger.info(f"Scored theme '{theme.name}': impact={business_impact}, priority={priority_score}")
        
        if scored_count > 0:
            db_session.commit()
            logger.info(f"Successfully scored {scored_count} themes")
        
        return {
            "status": "success",
            "scored_count": scored_count,
            "total_themes": db_session.query(Theme).count()
        }
    
    except Exception as e:
        db_session.rollback()
        logger.error(f"Error scoring themes: {str(e)}")
        raise


def get_themes_by_priority(db_session) -> Dict[str, List]:
    """
    Get all themes grouped by segment, sorted by priority_score descending.
    
    Args:
        db_session: Database session
        
    Returns:
        Dictionary: segment -> list of themes sorted by priority
    """
    from models import Theme
    
    try:
        # Get all themes ordered by priority_score DESC (nulls last)
        themes = db_session.query(Theme).order_by(
            Theme.priority_score.desc().nullslast(),
            Theme.insight_count.desc()
        ).all()
        
        logger.info(f"Retrieved {len(themes)} themes for report")
        
        # Group by segment
        grouped = {}
        for theme in themes:
            segment = theme.segment or "Unspecified"
            if segment not in grouped:
                grouped[segment] = []
            grouped[segment].append(theme)
        
        # Sort segment keys (Unspecified last)
        sorted_segments = []
        for seg in sorted(grouped.keys()):
            if seg != "Unspecified":
                sorted_segments.append(seg)
        if "Unspecified" in grouped:
            sorted_segments.append("Unspecified")
        
        result = {seg: grouped[seg] for seg in sorted_segments if seg in grouped}
        
        logger.info(f"Grouped {len(themes)} themes into {len(result)} segments")
        
        return result
    
    except Exception as e:
        logger.error(f"Error getting themes by priority: {str(e)}")
        raise
