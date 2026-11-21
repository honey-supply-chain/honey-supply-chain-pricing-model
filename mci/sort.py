class Sort:
    """
    Evaluates the botanical variety of the honey.

    Score:
        1 = unsuitable
        5 = suitable
        9 = highly suitable
    """

    @staticmethod
    def evaluate(variety: str) -> float:
        if not variety:
            return 1.0

        variety = variety.lower().strip()

        # Mixed blossom honey
        if variety in {
            "mixed blossom honey",
            "mixed blossom",
            "mixed honey",
        }:
            return 1.0

        # Premium varieties
        premium_varieties = {
            "fir",
            "fir honey",
            "heather",
            "heather honey",
            "alpine rose",
            "alpine rose honey",
        }

        if variety in premium_varieties:
            return 9.0

        # Other clearly identified varietal honeys
        return 5.0