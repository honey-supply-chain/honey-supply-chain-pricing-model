from si.models.apiary import Apiary
from si.models.water_source import WaterSource


class WaterSourceRepository:
    def __init__(self, db_session):
        self.db = db_session

    def find_by_apiary(self, apiary: Apiary) -> WaterSource | None:
        return self.db.query(WaterSource).filter(WaterSource.apiary_mac == apiary.mac).first()
