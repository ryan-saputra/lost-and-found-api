from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from lost_and_found.database import Base
from lost_and_found.repositories.item_repository import ItemRepository
from lost_and_found.schemas.item import ItemReportCreate


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


def setup_function():
    Base.metadata.create_all(bind=test_engine)


def teardown_function():
    Base.metadata.drop_all(bind=test_engine)


def test_create_report():
    db = TestingSessionLocal()

    try:
        repository = ItemRepository(db)

        item_data = ItemReportCreate(
            title="Dompet hitam",
            description="Dompet hilang di kampus",
            category="Aksesoris",
            report_type="lost",
            location="Kampus",
        )

        result = repository.create(item_data)

        assert result.id is not None
        assert result.title == "Dompet hitam"
        assert result.report_type == "lost"
        assert result.status == "pending"
    finally:
        db.close()


def test_search_report_by_keyword():
    db = TestingSessionLocal()

    try:
        repository = ItemRepository(db)

        item_data = ItemReportCreate(
            title="Dompet hitam",
            description="Dompet hilang di kampus",
            category="Aksesoris",
            report_type="lost",
            location="Kampus",
        )

        repository.create(item_data)

        results = repository.search(keyword="dompet")

        assert len(results) == 1
        assert results[0].title == "Dompet hitam"
    finally:
        db.close()


def test_verify_report():
    db = TestingSessionLocal()

    try:
        repository = ItemRepository(db)

        item_data = ItemReportCreate(
            title="Dompet hitam",
            description="Dompet hilang di kampus",
            category="Aksesoris",
            report_type="lost",
            location="Kampus",
        )

        item = repository.create(item_data)
        result = repository.verify(item.id)

        assert result is not None
        assert result.status == "verified"
    finally:
        db.close()

def test_search_report_by_type():
    db = TestingSessionLocal()

    try:
        repository = ItemRepository(db)

        lost_item = ItemReportCreate(
            title="Dompet hitam",
            description="Dompet hilang di kampus",
            category="Aksesoris",
            report_type="lost",
            location="Kampus",
        )

        found_item = ItemReportCreate(
            title="Kunci motor",
            description="Kunci motor ditemukan",
            category="Aksesoris",
            report_type="found",
            location="Perpustakaan",
        )

        repository.create(lost_item)
        repository.create(found_item)

        results = repository.search(report_type="lost")

        assert len(results) == 1
        assert results[0].title == "Dompet hitam"
        assert results[0].report_type == "lost"
    finally:
        db.close()