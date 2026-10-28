
from typing import Protocol

from lost_and_found.models.item import ItemReport
from lost_and_found.schemas.item import ItemReportCreate


class ItemRepositoryInterface(Protocol):
    def create(self, item_data: ItemReportCreate) -> ItemReport:
        ...

    def get_all(self) -> list[ItemReport]:
        ...

    def search(
        self,
        keyword: str | None = None,
        report_type: str | None = None,
    ) -> list[ItemReport]:
        ...

    def verify(self, item_id: int) -> ItemReport | None:
        ...
