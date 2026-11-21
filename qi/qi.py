import numpy as np


class QI:
    """
    Aggregated Quality Index (QI).

    The QI combines the three quality dimensions:
        - PHQI: Physicochemical Honey Quality Index
        - MCI: Market Criteria Index
        - SI: Site Index

    The weights are derived from the AHP pairwise comparison matrix.
    """

    COMPARISON_MATRIX = np.array([
        [1,   2,   3],
        [1/2, 1,   2],
        [1/3, 1/2, 1]
    ], dtype=float)

    def __init__(self):
        self.weights = self._calculate_weights()

    def _calculate_weights(self) -> np.ndarray:
        """
        Calculates the AHP weights using column normalization
        followed by row mean calculation.

        Returns:
            A numpy array containing the weights for:
            [PHQI, MCI, SI].
        """

        column_sums = self.COMPARISON_MATRIX.sum(axis=0)

        normalized_matrix = (
            self.COMPARISON_MATRIX / column_sums
        )

        weights = normalized_matrix.mean(axis=1)

        return weights

    def calculate(
        self,
        phqi: float,
        mci: float,
        si: float,
    ) -> float:
        """
        Calculates the aggregated Quality Index.

        Args:
            phqi: Physicochemical Honey Quality Index.
            mci: Market Criteria Index.
            si: Site Index.

        Returns:
            The aggregated Quality Index.
        """

        phqi_weight = self.weights[0]
        mci_weight = self.weights[1]
        si_weight = self.weights[2]

        qi = (
            phqi_weight * phqi
            + mci_weight * mci
            + si_weight * si
        )

        return qi