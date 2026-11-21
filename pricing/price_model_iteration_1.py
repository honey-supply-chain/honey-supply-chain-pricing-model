class PriceModel:

    BASELINE_QI = 0.50
    SCALING_FACTOR = 1.60

    @staticmethod
    def calculate_multiplier(qi: float) -> float:
        if not 0.0 <= qi <= 1.0:
            raise ValueError("QI must be between 0 and 1.")

        return (
            1.0
            + PriceModel.SCALING_FACTOR
            * (qi - PriceModel.BASELINE_QI)
        )

    @staticmethod
    def calculate_price(base_price: float, qi: float) -> float:
        if base_price < 0:
            raise ValueError("Base price must not be negative.")

        multiplier = PriceModel.calculate_multiplier(qi)

        return base_price * multiplier