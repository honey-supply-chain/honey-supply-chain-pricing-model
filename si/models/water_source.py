from sqlalchemy import Column, Integer, String, Double, ForeignKey

from si.models.base import Base


class WaterSource(Base):
    __tablename__ = "water_source"

    id = Column(Integer, primary_key=True, autoincrement=True)
    distance = Column(Double, nullable=False)
    apiary_mac = Column(String(36), ForeignKey("apiary.mac"), nullable=False)  # Foreign Key zu Apiary

    def __init__(self, distance: float = None, apiary_mac: str = None):
        self.distance = distance
        self.apiary_mac = apiary_mac
