from phqi.water_content import WaterContent
from phqi.hmf import HMF
from phqi.invertase import Invertase
from phqi.equal_weighting import EqualWeighting
from common.normalization import normalize_saaty_score


class PHQIIteration2:

    def calculate(
        self,
        water_content: float,
        hmf: float,
        invertase: float,
        naturally_enzyme_weak: bool
    ) -> float:

        water_score = WaterContent.evaluate(water_content)
        hmf_score = HMF.evaluate(hmf)

        invertase_score = Invertase.evaluate(
            invertase,
            naturally_enzyme_weak
        )

        scores = [
            water_score,
            hmf_score,
            invertase_score
        ]

        if any(normalize_saaty_score(score.value) == 0.0 for score in scores):
            return 0.0

        return EqualWeighting.calculate(scores)