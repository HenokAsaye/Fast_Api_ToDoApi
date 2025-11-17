from datetime import datetime
from sqlalchemy.orm import Session
from todo_application.app.db.model import TodoModel
from todo_application.app.schemas.todo_schemas import TodoCreate, TodoUpdate


class TodoService:
    def __init__(self,db:Session):
        self.db = db
    def create_todo(self,to_do_create:TodoCreate) -> TodoModel:
        db_todo = TodoModel(title=to_do_create.title,description=to_do_create.description,completed=to_do_create.completed,due_date=to_do_create.due_date)
        self.db.add(db_todo)
        self.db.commit()
        self.db.refresh(db_todo)
        return db_todo
    
    def get_todo(self,todo_id:int) -> TodoModel | None:
        return self.db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    def get_all_todos(self,skip:int=0, limit:int =100) -> list[TodoModel]:
        return self.db.query(TodoModel).offset(skip).limit(limit).all()
    def update_todo(self,todo_id:int,to_update:TodoUpdate) -> TodoModel|None:
        db_todo = self.get_todo(todo_id=todo_id)
        if not db_todo:
            return None
        else:
            db_todo.title = to_update.title
            db_todo.description = to_update.description
            db_todo.completed = to_update.completed
            db_todo.due_date = to_update.due_date
            db_todo.updated_at = datetime.now()
            self.db.commit()
            self.db.refresh(db_todo)
            return db_todo
    def delete_todo(self,todo_id:int) -> bool:
        db_todo =self.get_todo(todo_id = todo_id)
        if not db_todo:
            return False
        self.db.delete(db_todo)
        self.db.commit()
        return True