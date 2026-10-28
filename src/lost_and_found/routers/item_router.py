
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Literal
from lost_and_found.database import SessionLocal
from lost_and_found.schemas.item import ItemReportCreate, ItemReportResponse
from lost_and_found.services.item_service import ItemService


router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ItemReportResponse, status_code=201)
def create_report(
    item_data: ItemReportCreate,
    db: Session = Depends(get_db),
):
    service = ItemService(db)
    return service.create_report(item_data)


@router.get("/", response_model=list[ItemReportResponse])
def get_reports(db: Session = Depends(get_db)):
    service = ItemService(db)
    return service.get_reports()

@router.get("/search", response_model=list[ItemReportResponse])
def search_reports(
    keyword: str | None = Query(default=None, min_length=1),
    report_type: Literal["lost", "found"] | None = None,
    db: Session = Depends(get_db),
):
    service = ItemService(db)
    return service.search_reports(
        keyword=keyword,
        report_type=report_type,
    )

@router.patch("/{item_id}/verify", response_model=ItemReportResponse)
def verify_report(
    item_id: int,
    db: Session = Depends(get_db),
):
    service = ItemService(db)
    item = service.verify_report(item_id)

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Laporan barang tidak ditemukan",
        )

    return item