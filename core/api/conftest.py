import os

import pytest

from api import create_app
from api.common.database import db_session, init_db, drop_db

HEADERS = {
    'content-type': 'application/json',
    '_secure_key': os.environ.get('SECURE_API_KEY')
}


@pytest.fixture(scope='session')
def app(request):
    """
    Create new application.
    Establish a context so all application parts
    are properly functioning.
    """
    app = create_app()

    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)

    return app


@pytest.fixture(scope='session')
def test_client(app, request):
    """
    Init flask's test client.
    """
    client = app.test_client()
    client.__enter__()

    request.addfinalizer(
        lambda: client.__exit__(None, None, None)
    )

    return client


@pytest.fixture(scope='session')
def session(request):
    def teardown():
        """
        For testing purposes the `flush` is sufficient.
        Flask middleware is not available in test environment,
        therefore records are not comitted to the database.
        In order to override this behaviour, adapt the
        `commit_session` middleware here.
        """
        db_session.remove()

    request.addfinalizer(teardown)

    return db_session


@pytest.fixture(scope='session')
def custom_headers():
    return HEADERS


@pytest.fixture(scope="session", autouse=True)
def database_management(request):
    """
    Create database before running the first test.
    Drop the database after running the last test.
    """
    init_db()

    def teardown():
        db_session.close()
        db_session.remove()
        drop_db()

    request.addfinalizer(teardown)
