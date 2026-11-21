from qi import QI


def main():
    qi = QI()

    result = qi.calculate(
        phqi=5.0,
        mci=6.0,
        si=8.0,
    )

    print(f"QI: {result:.4f}")
    print(f"PHQI weight: {qi.weights[0]:.10f}")
    print(f"MCI weight: {qi.weights[1]:.10f}")
    print(f"SI weight: {qi.weights[2]:.10f}")


if __name__ == "__main__":
    main()