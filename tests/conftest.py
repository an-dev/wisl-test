import logging

import pytest
from alembic import command, script  # type: ignore
from alembic.config import Config
from app.config import get_app_settings
from app.dependencies import get_db
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, orm

logger = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = get_app_settings().TEST_DATABASE_URI
SessionScoped = orm.scoped_session(orm.sessionmaker())
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# It's a scoped_session, and now is the time to configure it.
SessionScoped.configure(bind=engine)

def _migrate_db() -> None:
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", "alembic")

    directory = script.ScriptDirectory.from_config(alembic_cfg)
    logger.debug("Current head is %r", directory.get_heads())

    # Overrwrite existing sqlalchemy URL with our own.
    alembic_cfg.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)
    # Given we start with an empty database we start at base.
    # Stamping this sets up the internal Alembic table that is used for
    # versioning in migrations.
    logger.debug("Stamping as current version.")
    command.stamp(alembic_cfg, "base")

    # Upgrade to head.
    command.upgrade(alembic_cfg, "head")

_migrate_db()


@pytest.fixture(scope="session")
def scoped_db():
    try:
        db = SessionScoped()
        yield db
    finally:
        db.rollback()
        db.close()


@pytest.fixture(scope="session")
def api_client():
    client = TestClient(app)
    client.app.dependency_overrides[  # type: ignore[attr-defined]
        get_db
    ] = lambda: SessionScoped()
    return client


# Import our other fixtures.
pytest_plugins = [
    "tests.fixtures",
]
