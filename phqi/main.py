from phqi.phqi import PHQI

def main():

    phqi = PHQI()

    score = phqi.calculate(
        water_content=16.5,
        hmf=8.0,
        invertase=70.0,
        naturally_enzyme_weak=False
    )

    print(f"PHQI: {score:.2f}")


if __name__ == "__main__":
    main()