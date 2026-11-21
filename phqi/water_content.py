from common.suitability import Suitability


class WaterContent:

    @staticmethod
    def evaluate(water_content: float) -> Suitability:
        if water_content > 20:
            return Suitability.UNSUITABLE

        if water_content > 18:
            return Suitability.LESS_SUITABLE

        if water_content >= 16.8:
            return Suitability.SUITABLE

        return Suitability.MORE_SUITABLE