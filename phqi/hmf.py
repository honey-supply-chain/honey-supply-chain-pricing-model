from common.suitability import Suitability


class HMF:

    @staticmethod
    def evaluate(hmf: float) -> Suitability:
        if hmf > 40:
            return Suitability.UNSUITABLE

        if hmf > 15:
            return Suitability.LESS_SUITABLE

        if hmf > 10:
            return Suitability.SUITABLE

        return Suitability.MORE_SUITABLE