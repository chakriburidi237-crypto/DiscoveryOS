from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class RawInputBase(BaseModel):
    """Base schema for RawInput."""
    source_type: str
    raw_text: str


class RawInputCreate(BaseModel):
    """Schema for creating RawInput entries."""
    source_type: str = Field(..., description="Source type: interview, survey, or support")
    raw_text: str = Field(..., description="Raw text content")


class RawInputResponse(BaseModel):
    """Schema for RawInput response."""
    id: int
    source_type: str
    raw_text: str
    uploaded_at: datetime

    class Config:
        from_attributes = True


class IngestRequest(BaseModel):
    """Schema for ingest endpoint request."""
    source_type: str = Field(..., description="Source type: interview, survey, or support")
    text: Optional[str] = Field(None, description="Pasted text content")


class IngestResponse(BaseModel):
    """Schema for ingest endpoint response."""
    status: str
    created_rows: List[RawInputResponse]


class HealthResponse(BaseModel):
    """Schema for health check response."""
    status: str
    message: str


class ProcessEmbeddingsResponse(BaseModel):
    """Schema for process-embeddings endpoint response."""
    status: str
    processed_count: int
    total_insights: int


class ClusterSample(BaseModel):
    """Schema for a cluster sample with texts."""
    cluster_id: int
    size: int
    samples: List[str]


class ClusterResponse(BaseModel):
    """Schema for cluster endpoint response."""
    status: str
    num_clusters: int
    cluster_info: List[ClusterSample]


class ThemeResponse(BaseModel):
    """Schema for Theme response."""
    id: int
    name: str
    summary: str
    segment: Optional[str]
    insight_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class ThemeWithScoresResponse(BaseModel):
    """Schema for Theme response with scoring data."""
    id: int
    name: str
    summary: str
    segment: Optional[str]
    insight_count: int
    business_impact: Optional[float]
    priority_score: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True


class ThemesBySegmentResponse(BaseModel):
    """Schema for themes grouped by segment."""
    segment: str
    theme_count: int
    themes: List[ThemeWithScoresResponse]


class LabelThemesRequest(BaseModel):
    """Schema for label-themes endpoint request."""
    llm_provider: Optional[str] = Field(None, description="LLM provider: 'openai' or 'anthropic'")


class LabelThemesResponse(BaseModel):
    """Schema for label-themes endpoint response."""
    status: str
    themes_created: int
    themes: List[ThemeResponse]


class ReportResponse(BaseModel):
    """Schema for report endpoint response with pagination support."""
    status: str
    total_themes: int
    total_available: int = Field(description="Total number of themes available (before pagination)")
    offset: int = Field(description="Number of themes skipped (pagination offset)")
    limit: int = Field(description="Number of themes returned (pagination limit)")
    total_segments: int
    report_timestamp: datetime
    segments: List[ThemesBySegmentResponse]

