from mci import MCI


def main():
    mci = MCI()

    result = mci.calculate(
        variety="fir honey",
        origin="regional gps verified",
        certification="bio austria",
        award="gold",
    )

    print(f"MCI: {result:.4f}")


if __name__ == "__main__":
    main()