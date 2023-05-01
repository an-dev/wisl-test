from typing import NewType
from uuid import uuid4

from sqlalchemy import Column, String

from app.db import Base

PoiId = NewType('PoiId', str)
_PoiId = String(36)

def _str_uuid() -> str:
    return str(uuid4())

class Poi(Base):
    __tablename__ = "point_of_interests"

    id = Column(_PoiId, primary_key=True, default=_str_uuid)
    location = Column(String(50), nullable=False, unique=True)
