
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
