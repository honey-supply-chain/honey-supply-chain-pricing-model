from typing import Optional

from si.models.criterion import Criterion


class CriterionRepository:
    def __init__(self, db_session):
        self.db = db_session

    def find_by_name(self, name: str) -> Optional[Criterion]:
        return self.db.query(Criterion).filter(Criterion.name == name).first()

    def find_all(self):
        return self.db.query(Criterion).all()
