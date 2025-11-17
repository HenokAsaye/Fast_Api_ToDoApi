from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict, field_validator



class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=120)
    description: Optional[str] = Field(None, max_length=1000)
    completed: bool = False
    due_date: Optional[datetime] = None

    @field_validator("title", mode="before")
    def _strip_title(cls, v: str) -> str:
        return v.strip() if isinstance(v, str) else v

    @field_validator("description", mode="before")
    def _strip_description(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if isinstance(v, str) else v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
                "due_date": "2025-11-20T18:00:00Z",
            }
        }
    )

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=120)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None

    @field_validator("title", "description", mode="before")
    def _strip_strings(cls, v):
        return v.strip() if isinstance(v, str) else v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Buy groceries and snacks",
                "completed": True,
            }
        }
    )

class TodoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    due_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

class PageMeta(BaseModel):
    page: int
    size: int
    total: int
    pages: int


class TodoPage(BaseModel):
    items: List[TodoRead]
    meta: PageMeta

class Message(BaseModel):
    detail: str

