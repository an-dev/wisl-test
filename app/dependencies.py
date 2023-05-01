
from typing import Generator

from sqlalchemy.orm import Session

from .db import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Create SQLAlchemy session isntance."""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
