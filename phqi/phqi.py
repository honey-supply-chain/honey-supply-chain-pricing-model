from common.suitability import Suitability
from phqi.water_content import WaterContent
from phqi.hmf import HMF
from phqi.invertase import Invertase
from phqi.equal_weighting import EqualWeighting


class PHQI:

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

        return EqualWeighting.calculate(scores)