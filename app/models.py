# Definice tabulek

from sqlalchemy import Column, Integer, String
from .database import Base

class Task(Base):
    __tablename__ = "tasks"

    # Vlastne tady je vytvareni radku jako v phpmyadmin, kdybych psal primo sql dotazy.
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
