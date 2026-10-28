
from unittest.mock import Mock

from lost_and_found.schemas.item import ItemReportCreate
from lost_and_found.services.item_service import ItemService


def test_create_report():
    repository = Mock()
    service = ItemService(repository)

    item_data = ItemReportCreate(
        title="Dompet hitam",
        description="Dompet hilang di kampus",
        category="Aksesoris",
        report_type="lost",
        location="Kampus",
    )

    expected_result = Mock()
    repository.create.return_value = expected_result

    result = service.create_report(item_data)

    repository.create.assert_called_once_with(item_data)
    assert result is expected_result


def test_get_reports():
    repository = Mock()
    service = ItemService(repository)

    expected_result = [Mock(), Mock()]
    repository.get_all.return_value = expected_result

    result = service.get_reports()

    repository.get_all.assert_called_once_with()
    assert result is expected_result


def test_search_reports():
    repository = Mock()
    service = ItemService(repository)

    expected_result = [Mock()]
    repository.search.return_value = expected_result

    result = service.search_reports(
        keyword="dompet",
        report_type="lost",
    )

    repository.search.assert_called_once_with(
        keyword="dompet",
        report_type="lost",
    )
    assert result is expected_result


def test_verify_report():
    repository = Mock()
    service = ItemService(repository)

    expected_result = Mock()
    repository.verify.return_value = expected_result

    result = service.verify_report(1)

    repository.verify.assert_called_once_with(1)
    assert result is expected_result


class FakeItemRepository:
    """Repository pengganti untuk menguji kontrak ItemService."""

    def __init__(self):
        self.items = []
        self.next_id = 1

    def create(self, item_data):
        item = {
            "id": self.next_id,
            "title": item_data.title,
            "report_type": item_data.report_type,
            "status": "pending",
        }
        self.items.append(item)
        self.next_id += 1
        return item

    def get_all(self):
        return self.items

    def search(self, keyword=None, report_type=None):
        results = self.items

        if keyword:
            keyword_lower = keyword.lower()
            results = [
                item for item in results
                if keyword_lower in item["title"].lower()
            ]

        if report_type:
            results = [
                item for item in results
                if item["report_type"] == report_type
            ]

        return results

    def verify(self, item_id):
        for item in self.items:
            if item["id"] == item_id:
                item["status"] = "verified"
                return item

        return None


def test_service_works_with_replacement_repository():
    repository = FakeItemRepository()
    service = ItemService(repository)

    item_data = ItemReportCreate(
        title="Dompet hitam",
        description="Dompet hilang di kampus",
        category="Aksesoris",
        report_type="lost",
        location="Kampus",
    )

    created_item = service.create_report(item_data)

    assert created_item["id"] == 1
    assert created_item["status"] == "pending"

    reports = service.get_reports()
    assert len(reports) == 1

    search_results = service.search_reports(
        keyword="dompet",
        report_type="lost",
    )
    assert len(search_results) == 1

    verified_item = service.verify_report(1)
    assert verified_item["status"] == "verified"

    assert service.verify_report(999) is None
