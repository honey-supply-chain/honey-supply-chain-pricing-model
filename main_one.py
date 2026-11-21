from common.db import SessionLocal

from si.ahp_user_service import AhpUserService
from si.evaluation_runner import EvaluationRunner
from si.repository.apiary_repository import ApiaryRepository
from si.repository.criterion_repository import CriterionRepository
from si.repository.normalization_parameter_repository import (
    NormalizationParameterRepository
)
from si.repository.pairwise_comparison_repository import (
    PairwiseComparisonRepository
)
from si.repository.sensor_data_repository import SensorDataRepository
from si.repository.user_repository import UserRepository
from si.repository.water_source_repository import WaterSourceRepository
from si.sensor_aggregation_service import SensorAggregationService

from phqi import PHQI
from mci import MCI
from qi import QI

from pricing.price_model_iteration_1 import PriceModel


def calculate_si(
    db,
    user_id: int,
    station: str,
    year: int,
    mac: str,
) -> float:
    """
    Calculates the Site Index (SI) using real sensor data
    and the AHP configuration stored in the database.
    """

    criterion_repo = CriterionRepository(db)
    comparison_repo = PairwiseComparisonRepository(db)
    normalization_repo = NormalizationParameterRepository(db)
    user_repo = UserRepository(db)
    sensor_data_repo = SensorDataRepository(db)
    apiary_repo = ApiaryRepository(db)
    water_source_repo = WaterSourceRepository(db)

    sensor_aggregation_service = SensorAggregationService(
        sensor_data_repo,
        water_source_repo
    )

    ahp_service = AhpUserService(
        criterion_repo,
        comparison_repo,
        normalization_repo
    )

    evaluation_runner = EvaluationRunner(
        sensor_aggregation_service,
        ahp_service,
        user_repo,
        apiary_repo,
        db
    )

    return evaluation_runner.evaluate_station(
        user_id,
        station,
        year,
        mac
    )


def calculate_phqi(
    water_content: float,
    hmf: float,
    invertase: float,
    naturally_enzyme_weak: bool,
) -> float:
    """
    Calculates the Physicochemical Honey Quality Index (PHQI).
    """

    phqi = PHQI()

    return phqi.calculate(
        water_content=water_content,
        hmf=hmf,
        invertase=invertase,
        naturally_enzyme_weak=naturally_enzyme_weak,
    )


def calculate_mci(
    variety: str,
    origin: str,
    certification: str,
    award: str,
) -> float:
    """
    Calculates the Market Criteria Index (MCI).
    """

    mci = MCI()

    return mci.calculate(
        variety=variety,
        origin=origin,
        certification=certification,
        award=award,
    )


def calculate_qi(
    phqi_score: float,
    mci_score: float,
    si_score: float,
) -> float:
    """
    Calculates the aggregated Quality Index (QI).

    PHQI, MCI and SI are normalized to the range 0-1
    before aggregation.
    """

    qi = QI()

    return qi.calculate(
        phqi=phqi_score,
        mci=mci_score,
        si=si_score,
    )


def main():
    """
    Executes the complete quality index and price calculation.

    1. Calculate SI from real sensor data.
    2. Calculate PHQI from laboratory measurements.
    3. Calculate MCI from market-related criteria.
    4. Aggregate SI, PHQI and MCI into the QI.
    5. Calculate the quality-based price multiplier.
    6. Calculate the final price.
    """

    # =============================================
    # INPUT DATA
    # =============================================

    # SI configuration
    user_id = 1
    station = "Bienenstand_6"
    year = 2024
    mac = "0eddd296-1275-40e5-9b2a-ea9c34aa5b60"

    # PHQI configuration
    water_content = 23
    hmf = 80
    invertase = 10.0
    naturally_enzyme_weak = False

    # MCI configuration
    variety = "fir honey"
    origin = "regional gps verified"
    certification = ""
    award = "no award"

    # Pricing configuration
    base_price = 5.00

    # =============================================
    # DATABASE
    # =============================================

    db = SessionLocal()

    try:
        # =============================================
        # CALCULATE SI
        # =============================================

        si_score = calculate_si(
            db=db,
            user_id=user_id,
            station=station,
            year=year,
            mac=mac,
        )

        # =============================================
        # CALCULATE PHQI
        # =============================================

        phqi_score = calculate_phqi(
            water_content=water_content,
            hmf=hmf,
            invertase=invertase,
            naturally_enzyme_weak=naturally_enzyme_weak,
        )

        # =============================================
        # CALCULATE MCI
        # =============================================

        mci_score = calculate_mci(
            variety=variety,
            origin=origin,
            certification=certification,
            award=award,
        )

        # =============================================
        # CALCULATE QI
        # =============================================

        qi_score = calculate_qi(
            phqi_score=phqi_score,
            mci_score=mci_score,
            si_score=si_score,
        )

        # =============================================
        # CALCULATE PRICE
        # =============================================

        # Calculate the quality-based price multiplier
        multiplier = PriceModel.calculate_multiplier(qi_score)

        # Calculate the final price
        final_price = PriceModel.calculate_price(
            base_price=base_price,
            qi=qi_score,
        )

        # =============================================
        # DISPLAY RESULTS
        # =============================================

        print()
        print("=" * 45)
        print("QUALITY INDEX RESULTS")
        print("=" * 45)
        print(f"Station:    {station}")
        print(f"Year:       {year}")
        print()
        print(f"SI:         {si_score:.4f}")
        print(f"PHQI:       {phqi_score:.4f}")
        print(f"MCI:        {mci_score:.4f}")
        print(f"QI:         {qi_score:.4f}")
        print()
        print("PRICE MODEL")
        print("-" * 45)
        print(f"Base price: {base_price:.2f} EUR")
        print(f"Multiplier:  {multiplier:.4f}")
        print(f"Final price: {final_price:.2f} EUR")
        print("=" * 45)

    finally:
        db.close()


if __name__ == "__main__":
    main()