class Origin:
    """
    Evaluates the geographical origin of the honey.

    Score:
        1 = unsuitable
        3 = less suitable
        5 = suitable
        9 = highly suitable
    """

    @staticmethod
    def evaluate(origin: str) -> float:
        if not origin:
            return 1.0

        origin = origin.lower().strip()

        if origin in {
            "regional",
            "regional gps",
            "regional gps verified",
        }:
            return 9.0

        if origin in {
            "national",
            "domestic",
            "austria",
        }:
            return 5.0

        if origin in {
            "eu",
            "eu mixture",
            "eu mix",
        }:
            return 3.0

        if origin in {
            "eu/non-eu",
            "eu/non-eu mixture",
            "eu and non-eu",
            "eu and non-eu mixture",
        }:
            return 1.0

        return 1.0