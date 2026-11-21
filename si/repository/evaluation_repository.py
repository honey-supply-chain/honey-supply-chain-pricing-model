# evaluation_repository.py

from sqlalchemy.orm import Session
from typing import Optional, List
from si.models.evaluation import Evaluation


class EvaluationRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def add(self, evaluation: Evaluation) -> Evaluation:
        self.db.add(evaluation)
        self.db.commit()
        self.db.refresh(evaluation)
        return evaluation

    def find_all(self) -> List[Evaluation]:
        return self.db.query(Evaluation).all()

    def find_by_id(self, evaluation_id: int) -> Optional[Evaluation]:
        return self.db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
