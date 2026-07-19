from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum, LargeBinary, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()



class SourceType(str, enum.Enum):
    """Source type enumeration."""
    interview = "interview"
    survey = "survey"
    support = "support"


class RawInput(Base):
    """
    Table for storing raw input chunks.
    Each row represents a single chunk of text from an uploaded source.
    """
    __tablename__ = "raw_inputs"

    id = Column(Integer, primary_key=True, index=True)
    source_type = Column(SQLEnum(SourceType), nullable=False)
    raw_text = Column(Text, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    insights = relationship("Insight", back_populates="raw_input", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<RawInput(id={self.id}, source_type={self.source_type}, uploaded_at={self.uploaded_at})>"


class Theme(Base):
    """
    Table for storing labeled themes/categories from clustered insights.
    Each row represents a theme identified by the LLM.
    """
    __tablename__ = "themes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    summary = Column(Text, nullable=False)
    segment = Column(String(255), nullable=True)  # e.g., "product managers", "end users"
    insight_count = Column(Integer, default=0, nullable=False)
    business_impact = Column(Float, nullable=True, index=True)  # 1-5 scale, null if not yet scored
    priority_score = Column(Float, nullable=True, index=True)  # insight_count * business_impact
    scored_at = Column(DateTime, nullable=True)  # When the theme was scored
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    insights = relationship("Insight", back_populates="theme", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Theme(id={self.id}, name={self.name}, insight_count={self.insight_count}, priority_score={self.priority_score})>"


class Insight(Base):
    """
    Table for storing extracted insights from raw inputs.
    Each row represents an insight/analysis of a raw input chunk.
    """
    __tablename__ = "insights"

    id = Column(Integer, primary_key=True, index=True)
    raw_input_id = Column(Integer, ForeignKey("raw_inputs.id"), nullable=False)
    extracted_text = Column(Text, nullable=True)
    embedding = Column(LargeBinary, nullable=True)  # Store embedding vectors as binary
    theme_id = Column(Integer, ForeignKey("themes.id"), nullable=True)  # Foreign key to Theme

    # Relationships
    raw_input = relationship("RawInput", back_populates="insights")
    theme = relationship("Theme", back_populates="insights")

    def __repr__(self):
        return f"<Insight(id={self.id}, raw_input_id={self.raw_input_id}, theme_id={self.theme_id})>"
