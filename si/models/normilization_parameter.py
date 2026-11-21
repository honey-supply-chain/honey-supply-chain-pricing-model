from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from si.models.base import Base


class NormalizationParameter(Base):
    __tablename__ = "normalization_parameter"

    id = Column(Integer, primary_key=True, autoincrement=True)

    criterion_id = Column(Integer, ForeignKey("criterion.id"), unique=True, nullable=False)
    criterion = relationship("Criterion", uselist=False)

    minValue = Column(Float)
    maxValue = Column(Float)
