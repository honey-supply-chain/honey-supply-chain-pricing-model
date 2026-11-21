class Ahp:

    @staticmethod
    def normalize_matrix(matrix):
        size = len(matrix)
        column_sums = [0.0] * size
        normalized = [[0.0] * size for _ in range(size)]

        # Spaltensummen berechnen
        for j in range(size):
            for i in range(size):
                column_sums[j] += matrix[i][j]

        # Normalisieren
        for i in range(size):
            for j in range(size):
                if column_sums[j] == 0:
                    normalized[i][j] = 0
                else:
                    normalized[i][j] = matrix[i][j] / column_sums[j]

        return normalized

    @staticmethod
    def calculate_weights(normalized_matrix):
        size = len(normalized_matrix)
        weights = [0.0] * size

        for i in range(size):
            total = sum(normalized_matrix[i])
            weights[i] = total / size

        print("\nAHP-Gewichtungen:")
        print("-" * 40)

        for i, weight in enumerate(weights):
            print(f"Kriterium {i + 1}: {weight:.10f} ({weight * 100:.6f} %)")

        print("-" * 40)
        print(f"Summe: {sum(weights):.10f}")
        print(f"Summe: {sum(weights) * 100:.6f} %")

        return weights

    @staticmethod
    def print_vector(vector, labels):
        for label, value in zip(labels, vector):
            print(f"{label}: {value:.4f}")

    @staticmethod
    def compute_consistency_ratio(matrix, weights):
        n = len(matrix)
        if n < 3:
            print("Konsistenzprüfung nicht sinnvoll für n < 3")
            return 0.0

        lambdas = []
        for i in range(n):
            row_sum = 0.0
            for j in range(n):
                row_sum += matrix[i][j] * weights[j]
            if weights[i] == 0:
                raise ValueError(f"Gewicht an Index {i} ist 0, Division durch 0 nicht möglich.")
            lambdas.append(row_sum / weights[i])

        lambda_max = sum(lambdas) / n
        ci = (lambda_max - n) / (n - 1)

        ri_values = [0.0, 0.0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41]
        ri = ri_values[n - 1] if (n - 1) < len(ri_values) else 1.41

        cr = ci / ri
        return cr


def test_ahp():
    matrix = [
        [1, 2, 3],
        [0.5, 1, 4],
        [1 / 3, 0.25, 1]
    ]
    labels = ['Kriterium1', 'Kriterium2', 'Kriterium3']

    ahp = Ahp()
    normalized = ahp.normalize_matrix(matrix)
    weights = ahp.calculate_weights(normalized)

    print("Normalized matrix:")
    for row in normalized:
        print(["{:.4f}".format(x) for x in row])

    print("\nGewichte:")
    ahp.print_vector(weights, labels)

    cr = ahp.compute_consistency_ratio(matrix, weights)
    print(f"\nConsistency Ratio: {cr:.4f}")


if __name__ == "__main__":
    test_ahp()
