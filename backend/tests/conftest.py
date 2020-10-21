from tempfile import NamedTemporaryFile
from unittest.mock import MagicMock

import pytest

import dms


@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""
    with NamedTemporaryFile() as db_file, NamedTemporaryFile() as s_db_file:
        test_config = {
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + db_file.name,
            'SCHEDULER_DB_URL': 'sqlite:///' + s_db_file.name,
        }
        dms.groups.scheduler._publish_scan_job = MagicMock()
        app = dms.create_app(test_config)

        # Establish an application context before running the tests.
        with app.app_context():
            yield app


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def db(app, request):
    """Session-wide test database."""
    dms.db.app = app
    dms.db.create_all()

    yield dms.db

    dms.db.drop_all()


@pytest.fixture(scope='function')
def scheduler():
    yield dms.groups.scheduler.scheduler
    dms.groups.scheduler.scheduler.remove_all_jobs()


@pytest.fixture(scope='function')
def session(db, scheduler, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)
    db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()
