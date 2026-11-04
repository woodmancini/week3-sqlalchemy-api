import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from application import create_app
from database import get_db

# tmp_path is a built-in pytest fixture that automatically creates a
# unique temporary directory for each test run. It returns this directory 
# as a standard Python pathlib.Path object, which makes it easy to create and manipulate temporary files
# handles clean-up automatically

@pytest.fixture
def app_factory(tmp_path):
    engine = create_engine(
        f"sqlite:///{tmp_path / 'test.db'}", # works because tmp_path is a pathlib.Path object
        connect_args={"check_same_thread": False},
    )
    sessions = sessionmaker(bind=engine)
    apps = []

    def make_app():
        app = create_app(engine)

        # yields a Session. local generator function that acts as the mock
        # database dependency for api routes
        def override_db():
            # with statement ensures the connection closes after request finishes
            with sessions() as session:
                yield session

        # FastAPI feature that intercepts any route asking for your regular get_db
        # connection and silently swaps it out with override_db
        app.dependency_overrides[get_db] = override_db
        apps.append(app)
        return app

    # yields a FastAPI instance
    yield make_app
    for app in apps:
            app.dependency_overrides.clear()
    engine.dispose()

# "Factory as a Fixture" pattern
@pytest.fixture
def client(app_factory):
    with TestClient(app_factory()) as test_client:
        yield test_client

# 1: client depends on app_factory, so it runs the app_factory first (this is a pytest thing)
# 2: app_factory creates the test database engine, and yields make_app function object
# 3: TestClient(app_factory()) - this now calls make_app, which was yielded by app_factory and passed in to client()
# 4: make_app returns app (the fastapi instance), which is then wrapped in TestClient
# 5: yield test_client - client() fixture hands this client to the actual test function
# 6: yield session - creates a test database session to replace regular get_db dependency 
# 7: fixtures resume in reverse order: client cleans up the TestClient, then app_factory clears dependency overrides
# and destroys the database engine.