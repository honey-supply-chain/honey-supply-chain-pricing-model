from typing import List


from si.models.pairwise_comparison import PairwiseComparison
from si.models.user import User


class PairwiseComparisonRepository:
    def __init__(self, db_session):
        self.db = db_session

    def find_all_by_user(self, user: User) -> List[PairwiseComparison]:
        return self.db.query(PairwiseComparison).filter(PairwiseComparison.user_id == user.id).all()
