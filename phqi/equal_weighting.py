from common.normalization import normalize_saaty_score
from common.suitability import Suitability


class EqualWeighting:

    @staticmethod
    def calculate(scores: list[Suitability]) -> float:
        if not scores:
            raise ValueError("No suitability scores were provided.")

        normalized_scores = [
            normalize_saaty_score(score.value)
            for score in scores
        ]

        return sum(normalized_scores) / len(normalized_scores)