from sqlalchemy import Column, Integer, String, Double, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from si.models.base import Base


class Evaluation(Base):
    __tablename__ = "evaluation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime)
    total = Column(Double, nullable=False)
    honey_harvest = Column(Double, nullable=False)
    summer_temperature = Column(Double, nullable=False)
    winter_temperature = Column(Double, nullable=False)
    light_intensity = Column(Double, nullable=False)
    wind_speed = Column(Double, nullable=False)
    humidity = Column(Double, nullable=False)
    precipitation = Column(Double, nullable=False)
    water_source = Column(Double, nullable=False)
    weighted_honey_harvest = Column(Double, nullable=False)
    weighted_summer_temperature = Column(Double, nullable=False)
    weighted_winter_temperature = Column(Double, nullable=False)
    weighted_light_intensity = Column(Double, nullable=False)
    weighted_wind_speed = Column(Double, nullable=False)
    weighted_humidity = Column(Double, nullable=False)
    weighted_precipitation = Column(Double, nullable=False)
    weighted_water_source = Column(Double, nullable=False)

    apiary_mac = Column(String(36), ForeignKey('apiary.mac'), nullable=False)
    apiary = relationship("Apiary", back_populates="evaluations")
