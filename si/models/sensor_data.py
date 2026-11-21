from sqlalchemy import (
    Column, Integer, String, Float, DateTime
)
from si.models.base import Base



class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime)
    temperature = Column(Float)
    humidity = Column(Float)
    rain = Column(Float)
    light_intensity = Column(Float)
    wind_speed = Column(Float)
    wind_direction = Column(Float)
    pressure = Column(Float)
    station = Column(String)
    weight = Column(Float)
    brood_temperature = Column(Float)
