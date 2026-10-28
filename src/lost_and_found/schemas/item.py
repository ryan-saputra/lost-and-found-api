
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ItemReportCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    description: str = Field(min_length=1)
    category: str = Field(min_length=1, max_length=50)
    report_type: Literal["lost", "found"]
    location: str = Field(min_length=1, max_length=150)


class ItemReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    category: str
    report_type: str
    location: str
    status: str
    created_at: datetime
