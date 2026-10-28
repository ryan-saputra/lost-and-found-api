
from sqlalchemy import select
from sqlalchemy.orm import Session

from lost_and_found.models.item import ItemReport
from lost_and_found.schemas.item import ItemReportCreate


class ItemRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, item_data: ItemReportCreate) -> ItemReport:
        item = ItemReport(**item_data.model_dump())
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def get_all(self) -> list[ItemReport]:
        statement = select(ItemReport).order_by(ItemReport.id.desc())
        return list(self.session.scalars(statement).all())

    def get_by_id(self, item_id: int) -> ItemReport | None:
        return self.session.get(ItemReport, item_id)

    def verify(self, item_id: int) -> ItemReport | None:
        item = self.get_by_id(item_id)

        if item is None:
            return None

        item.status = "verified"
        self.session.commit()
        self.session.refresh(item)

        return item
    
    def search(
        self,
        keyword: str | None = None,
        report_type: str | None = None,
    ) -> list[ItemReport]:
        statement = select(ItemReport)

        if keyword:
            search_pattern = f"%{keyword}%"
            statement = statement.where(
                ItemReport.title.ilike(search_pattern)
                | ItemReport.description.ilike(search_pattern)
                | ItemReport.location.ilike(search_pattern)
            )

        if report_type:
            statement = statement.where(
                ItemReport.report_type == report_type
            )

        statement = statement.order_by(ItemReport.id.desc())
        return list(self.session.scalars(statement).all())
