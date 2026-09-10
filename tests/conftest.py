import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app


TEST_DATABASE_URL = os.getenv(
	"TEST_DATABASE_URL",
	"postgresql://devops_user:devops_password@localhost:5432/devops_test_db",
)

engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
	autocommit=False,
	autoflush=False,
	bind=engine,
)


@pytest.fixture(autouse=True)
def setup_database():
	Base.metadata.create_all(bind=engine)

	yield

	Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
	db = TestingSessionLocal()

	try:
		yield db
	finally:
		db.close()


@pytest.fixture
def client(db_session):
	def override_get_db():
		try:
			yield db_session
		finally:
			pass

	app.dependency_overrides[get_db] = override_get_db

	yield TestClient(app)

	app.dependency_overrides.clear()
