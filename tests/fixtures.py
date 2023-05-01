from typing import Any

import factory
import faker
import pytest
from app.models import Poi

from .conftest import SessionScoped

fake = faker.Faker()


@pytest.fixture(scope="session")
def poi_factory() -> Any:
    class PoiFactory(factory.alchemy.SQLAlchemyModelFactory):
        id = factory.LazyAttribute(lambda _: fake.uuid4())
        location = factory.Sequence(lambda _: fake.local_latlng()[2])

        class Meta:
            model = Poi
            sqlalchemy_session = SessionScoped
            sqlalchemy_session_persistence = "commit"

    yield PoiFactory
