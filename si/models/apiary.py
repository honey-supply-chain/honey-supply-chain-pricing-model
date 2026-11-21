from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from si.models.base import Base  # deine Base-Klasse

class Apiary(Base):
    __tablename__ = "apiary"

    mac = Column(String(36), primary_key=True, nullable=False, unique=True)
    name = Column(String)
    user_id = Column(String, ForeignKey("user.id"))  # Passe ggf. den Tabellennamen & Spaltentyp an

    user = relationship("User", back_populates="apiaries")  # vorausgesetzt User hat "apiaries" definiert
    evaluations = relationship("Evaluation", back_populates="apiary")
