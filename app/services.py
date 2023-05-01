from typing import Dict, List

import httpx
from sqlalchemy.orm import Session

from .config import get_app_settings
from .repository import list_pois
from .schemas import PoiWeather

API_KEY = get_app_settings().WEATHER_API_KEY
FORECAST_DAYS = 2

def list_poi_forecasts(session: Session) -> Dict[str, Dict[str, PoiWeather]]:
    poi_data_list: Dict[str, Dict[str, PoiWeather]] = {}
    pois = list_pois(session)

    for poi in pois:
        resp = httpx.get(f"https://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={poi.location}&days={FORECAST_DAYS}&aqi=no&alerts=no")
        forecast_days = resp.json()['forecast']['forecastday']

        poi_data_list[poi.location] = {
            forecast['date']: PoiWeather(
                temp=forecast['day']['avgtemp_c'],
                humdity=forecast['day']['avghumidity'],
                precipitation=forecast['day']['totalprecip_mm']
            )
            for forecast in forecast_days}
    return poi_data_list
