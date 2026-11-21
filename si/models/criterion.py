from sqlalchemy import Column, Integer, String
from si.models.base import Base


class Criterion(Base):
    __tablename__ = "criterion"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    def __init__(self, name: str = None):
        self.name = name
