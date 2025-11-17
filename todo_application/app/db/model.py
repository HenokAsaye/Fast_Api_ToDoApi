from sqlalchemy import Column, Integer, String, Boolean
from .database import Base
from datetime import datetime





class TodoModel(Base):
    __tablename__ ="todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)
    due_date = Column(String, nullable=True)
    created_at = Column(String, default=datetime.now)    
    updated_at = Column(String, default=datetime.now, onupdate=datetime.now)