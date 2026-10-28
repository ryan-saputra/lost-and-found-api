
from sqlalchemy.orm import Session

from lost_and_found.models.item import ItemReport
from lost_and_found.repositories.item_repository import ItemRepository
from lost_and_found.schemas.item import ItemReportCreate


class ItemService:
    def __init__(self, session: Session):
        self.repository = ItemRepository(session)

    def create_report(self, item_data: ItemReportCreate) -> ItemReport:
        return self.repository.create(item_data)

    def get_reports(self) -> list[ItemReport]:
        return self.repository.get_all()

    def search_reports(
        self,
        keyword: str | None = None,
        report_type: str | None = None,
    ) -> list[ItemReport]:
        return self.repository.search(
            keyword=keyword,
            report_type=report_type,
        )

    def verify_report(self, item_id: int) -> ItemReport | None:
        return self.repository.verify(item_id)