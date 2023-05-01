from typing import List

from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from .errors import DuplicatePoi, PoiNotFound
from .models import Poi, PoiId


def list_pois(session: Session) -> List[Poi]:
    return session.query(Poi).all()

def create_poi(
    location: str,
    *,
    session: Session
) -> Poi:
    try:
        poi = Poi(location=location)
        session.add(poi)
        session.commit()
    except IntegrityError:
        raise DuplicatePoi()
    return poi


def delete_poi(
    poiId: PoiId,
    *,
    session: Session
) -> None:
    try:
        poi = session.query(Poi).filter(Poi.id == poiId).one()
        poi.delete()
        session.commit()
    except NoResultFound:
        raise PoiNotFound()
    return
