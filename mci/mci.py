from common.normalization import normalize_saaty_score
from mci.award import Award
from mci.certification import Certification
from mci.origin import Origin
from mci.sort import Sort


class MCI:
    """
    Market Criteria Index (MCI).

    The weights are derived from the empirically determined
    price effects of the individual criteria.
    """

    VARIETY_PRICE_EFFECT = 16.12
    ORIGIN_PRICE_EFFECT = 39.10
    CERTIFICATION_PRICE_EFFECT = 13.55
    AWARD_PRICE_EFFECT = 15.00

    TOTAL_PRICE_EFFECT = (
        VARIETY_PRICE_EFFECT
        + ORIGIN_PRICE_EFFECT
        + CERTIFICATION_PRICE_EFFECT
        + AWARD_PRICE_EFFECT
    )

    VARIETY_WEIGHT = VARIETY_PRICE_EFFECT / TOTAL_PRICE_EFFECT
    ORIGIN_WEIGHT = ORIGIN_PRICE_EFFECT / TOTAL_PRICE_EFFECT
    CERTIFICATION_WEIGHT = CERTIFICATION_PRICE_EFFECT / TOTAL_PRICE_EFFECT
    AWARD_WEIGHT = AWARD_PRICE_EFFECT / TOTAL_PRICE_EFFECT

    def calculate(
        self,
        variety: str,
        origin: str,
        certification: str,
        award: str,
    ) -> float:

        variety_score = Sort.evaluate(variety)
        origin_score = Origin.evaluate(origin)
        certification_score = Certification.evaluate(certification)
        award_score = Award.evaluate(award)

        weighted_raw_score = (
            self.VARIETY_WEIGHT * variety_score
            + self.ORIGIN_WEIGHT * origin_score
            + self.CERTIFICATION_WEIGHT * certification_score
            + self.AWARD_WEIGHT * award_score 
        )

        return normalize_saaty_score(weighted_raw_score)