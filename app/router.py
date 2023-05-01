from typing import Callable, Dict, List

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.routing import APIRoute
from sqlalchemy.orm import Session

from .common import raise_exception
from .dependencies import get_db
from .errors import DuplicatePoi, PoiNotFound
from .models import PoiId
from .repository import create_poi, delete_poi, list_pois
from .schemas import PoiBase, PoiOut, PoiWeather
from .services import list_poi_forecasts


class ErrorRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        route_handler = super().get_route_handler()

        async def _route_handler(request: Request) -> Response:  # type: ignore
            try:
                return await route_handler(request)
            except DuplicatePoi:
                raise_exception(
                    status.HTTP_400_BAD_REQUEST,
                    "Point of interest with that location already exists.",
                )
            except PoiNotFound:
                raise_exception(
                    status.HTTP_404_NOT_FOUND,
                    "Point of interest not found.",
                )

        return _route_handler

router = APIRouter(route_class=ErrorRoute)


@router.get("/", status_code=status.HTTP_200_OK)
async def poi_list(
    db: Session = Depends(get_db),
) -> List[PoiOut]:
    pois = list_pois(session=db)
    return [PoiOut.from_orm(p) for p in pois]


@router.post("/",status_code=status.HTTP_201_CREATED)
def poi_create(
    poi: PoiBase,
    db: Session = Depends(get_db),
) -> PoiOut:
    poi = create_poi(poi.location, session=db)
    return PoiOut.from_orm(poi)

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def poi_delete(
    poiId: PoiId,
    db: Session = Depends(get_db),
) -> None:
    delete_poi(poiId, session=db)


@router.get("/forecasts/", status_code=status.HTTP_200_OK)
def poi_list_forecasts(
    db: Session = Depends(get_db),
) -> Dict[str, Dict[str, PoiWeather]]:
    return list_poi_forecasts(session=db)
