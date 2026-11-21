from common.suitability import Suitability


class Invertase:

    @staticmethod
    def evaluate(
            invertase: float,
            naturally_enzyme_weak: bool
    ) -> Suitability:

        if naturally_enzyme_weak:
            if invertase < 45:
                return Suitability.UNSUITABLE

            return Suitability.MORE_SUITABLE

        if invertase < 64:
            return Suitability.UNSUITABLE

        if invertase < 85:
            return Suitability.SUITABLE

        return Suitability.MORE_SUITABLE