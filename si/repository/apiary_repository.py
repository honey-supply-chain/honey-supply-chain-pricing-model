from si.models.apiary import Apiary
from sqlalchemy.orm import Session
from typing import Optional


class ApiaryRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def find_by_mac(self, mac: str) -> Optional[Apiary]:
        return self.db.query(Apiary).filter(Apiary.mac == mac).first()

    def add(self, apiary: Apiary) -> Apiary:
        self.db.add(apiary)
        self.db.commit()
        self.db.refresh(apiary)
        return apiary
