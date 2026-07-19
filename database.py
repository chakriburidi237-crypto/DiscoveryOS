import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

load_dotenv()

# Use SQLite by default for quick testing (no setup required)
# Switch to PostgreSQL by setting DATABASE_URL in .env
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./discoveryos.db"  # Default: SQLite in current directory
)

# SQLite-specific configuration
engine_kwargs = {}
if DATABASE_URL.startswith("sqlite"):
    # SQLite doesn't support connection pooling well, disable it
    engine_kwargs = {
        "connect_args": {"check_same_thread": False},
    }

engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("DEBUG", "False").lower() == "true",
    **engine_kwargs
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """Dependency for database session injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


