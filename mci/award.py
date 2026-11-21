class Award:
    """
    Evaluates the award received by the honey.

    Score:
        1 = no award
        3 = bronze
        5 = silver
        9 = gold
    """

    @staticmethod
    def evaluate(award: str) -> float:
        if not award:
            return 1.0

        award = award.lower().strip()

        if award in {
            "gold",
            "gold medal",
            "gold award",
        }:
            return 9.0

        if award in {
            "silver",
            "silver medal",
            "silver award",
        }:
            return 5.0

        if award in {
            "bronze",
            "bronze medal",
            "bronze award",
        }:
            return 3.0

        return 1.0