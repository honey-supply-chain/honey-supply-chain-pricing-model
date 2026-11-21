class PriceModel:

    ALPHA = 0.80

    @staticmethod
    def calculate_multiplier(qi: float) -> float:
        if not 0.0 <= qi <= 1.0:
            raise ValueError("QI must be between 0 and 1.")

        return 1.0 + PriceModel.ALPHA * qi

    @staticmethod
    def calculate_price(
        floor_price: float,
        qi: float
    ) -> float:

        if floor_price < 0:
            raise ValueError(
                "Floor price must not be negative."
            )

        multiplier = PriceModel.calculate_multiplier(qi)

        return floor_price * multiplier