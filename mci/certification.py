class Certification:
    """
    Evaluates the certification status of the honey.

    Score:
        1 = no certification
        3 = national quality label
        5 = EU organic certification
        9 = organic association certification
    """

    @staticmethod
    def evaluate(certification: str) -> float:
        if not certification:
            return 1.0

        certification = certification.lower().strip()

        # Organic association certification
        if certification in {
            "association organic",
            "organic association",
            "bio austria",
            "demeter",
            "bioland",
        }:
            return 9.0

        # EU organic certification
        if certification in {
            "eu organic",
            "eu organic certification",
            "organic",
        }:
            return 5.0

        # National quality label
        if certification in {
            "national quality label",
            "quality label",
        }:
            return 3.0

        return 1.0