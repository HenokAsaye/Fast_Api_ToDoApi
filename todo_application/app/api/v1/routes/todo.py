from typing import Tuple
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from todo_application.app.schemas.todo_schemas import (
    TodoCreate,
    TodoUpdate,
    TodoRead,
    TodoPage,
    PageMeta,
    Message,
)
from todo_application.app.db.database import get_db
from todo_application.app.core.config import get_settings
from todo_application.app.core.security import get_current_user
from todo_application.app.service import todo_service

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("/", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
def create_todo(
    payload: TodoCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    todo = todo_service.create_todo(db, payload, owner_id=user_id)
    return todo


@router.get("/{todo_id}", response_model=TodoRead)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    todo = todo_service.get_todo(db, todo_id, owner_id=user_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.get("/", response_model=TodoPage)
def list_todos(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1),
    q: str | None = Query(None, description="Filter by title/description"),
    completed: bool | None = Query(None),
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    settings = get_settings()
    size = min(size, settings.PAGE_SIZE_MAX)
    items, total = todo_service.list_todos(
        db, owner_id=user_id, page=page, size=size, q=q, completed=completed
    )
    pages = (total + size - 1) // size if size else 0
    return TodoPage(items=items, meta=PageMeta(page=page, size=size, total=total, pages=pages))


@router.patch("/{todo_id}", response_model=TodoRead)
def update_todo(
    todo_id: int,
    payload: TodoUpdate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    todo = todo_service.update_todo(db, todo_id, payload, owner_id=user_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.delete("/{todo_id}", response_model=Message, status_code=status.HTTP_200_OK)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    deleted = todo_service.delete_todo(db, todo_id, owner_id=user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Todo not found")
    return Message(detail="Todo deleted")