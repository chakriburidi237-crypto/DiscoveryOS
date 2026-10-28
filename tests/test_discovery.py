import pytest
from schemas import PriorityScoreRequest, ThemeCreate
from scoring import calculate_priority_score

def test_scoring_algorithm():
    score = calculate_priority_score(
        impact=8,
        urgency=7,
        confidence=0.85,
        effort=3
    )
    assert 1.0 <= score <= 10.0
    assert score > 5.0  # High impact + low effort should yield high score

def test_schema_validation():
    theme = ThemeCreate(
        title="Enterprise Single Sign-On",
        description="Customers requesting SAML/Okta integration",
        segment="Enterprise",
        impact=9,
        urgency=8
    )
    assert theme.title == "Enterprise Single Sign-On"
    assert theme.segment == "Enterprise"
