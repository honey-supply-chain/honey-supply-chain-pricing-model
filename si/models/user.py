from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from si.models.base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    prename = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)

    apiaries = relationship("Apiary", back_populates="user")
