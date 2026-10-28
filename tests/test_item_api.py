
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from lost_and_found.database import Base
from lost_and_found.main import app
from lost_and_found.routers.item_router import get_db


TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_function():
    Base.metadata.create_all(bind=test_engine)


def teardown_function():
    Base.metadata.drop_all(bind=test_engine)


def test_create_report_api():
    response = client.post(
        "/reports/",
        json={
            "title": "Tas biru",
            "description": "Tas biru hilang di kampus",
            "category": "Tas",
            "report_type": "lost",
            "location": "Kampus",
        },
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Tas biru"
    assert response.json()["status"] == "pending"


def test_get_reports_api():
    create_response = client.post(
        "/reports/",
        json={
            "title": "Kunci motor",
            "description": "Kunci motor ditemukan",
            "category": "Aksesoris",
            "report_type": "found",
            "location": "Perpustakaan",
        },
    )

    assert create_response.status_code == 201

    response = client.get("/reports/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Kunci motor"


def test_search_reports_api():
    client.post(
        "/reports/",
        json={
            "title": "Dompet hitam",
            "description": "Dompet hilang di kampus",
            "category": "Aksesoris",
            "report_type": "lost",
            "location": "Kampus",
        },
    )

    response = client.get(
        "/reports/search",
        params={"keyword": "dompet"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Dompet hitam"


def test_verify_report_api():
    create_response = client.post(
        "/reports/",
        json={
            "title": "Kartu mahasiswa",
            "description": "Kartu mahasiswa ditemukan",
            "category": "Kartu",
            "report_type": "found",
            "location": "Kantin",
        },
    )

    item_id = create_response.json()["id"]

    response = client.patch(f"/reports/{item_id}/verify")

    assert response.status_code == 200
    assert response.json()["status"] == "verified"
