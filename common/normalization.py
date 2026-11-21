def normalize_saaty_score(score: float) -> float:
    """
    Normalizes a Saaty suitability score from the range 1-9
    to the range 0-1 using Min-Max normalization.

    Formula:
        normalized = (score - 1) / (9 - 1)

    Examples:
        1 -> 0.0
        3 -> 0.25
        5 -> 0.5
        9 -> 1.0
    """

    min_score = 1.0
    max_score = 9.0

    if max_score == min_score:
        raise ValueError("Minimum and maximum score must differ.")

    normalized = (score - min_score) / (max_score - min_score)

    return max(0.0, min(1.0, normalized))