from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from si.models.base import Base


class PairwiseComparison(Base):
    __tablename__ = "pairwise_comparison"

    id = Column(Integer, primary_key=True, autoincrement=True)

    criteriona_id = Column(Integer, ForeignKey("criterion.id"), nullable=False)
    criterionb_id = Column(Integer, ForeignKey("criterion.id"), nullable=False)
    importance = Column(Float, nullable=False)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    # Relationships
    criterionA = relationship("Criterion", foreign_keys=[criteriona_id])
    criterionB = relationship("Criterion", foreign_keys=[criterionb_id])
    user = relationship("User")

    def __init__(self, user, criterionA, criterionB, importance):
        self.criterionA = criterionA
        self.criterionB = criterionB
        self.importance = importance
        self.user = user
