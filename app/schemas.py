from pydantic import BaseModel

from .models import PoiId


class PoiBase(BaseModel):
    location: str

class PoiOut(PoiBase):
    id: PoiId

    class Config:
        orm_mode = True

class PoiWeather(BaseModel):
    temp: float
    humdity: int
    precipitation: float
