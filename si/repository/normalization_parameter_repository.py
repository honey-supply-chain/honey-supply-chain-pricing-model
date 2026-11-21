from typing import Optional

from si.models.criterion import Criterion
from si.models.normilization_parameter import NormalizationParameter


class NormalizationParameterRepository:
    def __init__(self, db_session):
        self.db = db_session

    def find_by_criterion(self, criterion: Criterion) -> Optional[NormalizationParameter]:
        return self.db.query(NormalizationParameter).filter(
            NormalizationParameter.criterion_id == criterion.id
        ).first()
