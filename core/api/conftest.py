import pytest

from api import create_app
from api.common.database import db_session, init_db, drop_db

HEADERS = {
    'content-type': 'application/json',
    '_secure_key': '0a3de3a519d423c3e12b6a9bfe964c7deaa94d6553e9f50b9a6e3e26e14f147b'
}


@pytest.fixture(scope='session')
def app(request):
    app = create_app()

    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)

    return app


@pytest.fixture(scope='session')
def test_client(app, request):
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
    init_db()

    def teardown():
        db_session.close()
        db_session.remove()
        drop_db()

    request.addfinalizer(teardown)
