from common.db import SessionLocal
from si.ahp_user_service import AhpUserService
from si.criterion_evaluation import (
    evaluate_summer_temperature,
    evaluate_winter_temperature,
    evaluate_relative_humidity,
    evaluate_precipitation_conditions,
    evaluate_wind_speed,
    evaluate_forage,
    evaluate_lux,
    evaluate_water_source,
    Suitability
)


from si.evaluation_runner import EvaluationRunner
from si.repository.apiary_repository import ApiaryRepository
from si.repository.criterion_repository import CriterionRepository
from si.repository.normalization_parameter_repository import NormalizationParameterRepository
from si.repository.pairwise_comparison_repository import PairwiseComparisonRepository
from si.repository.sensor_data_repository import SensorDataRepository
from si.repository.user_repository import UserRepository
from si.repository.water_source_repository import WaterSourceRepository
from si.sensor_aggregation_service import SensorAggregationService


def calculate_overall_score(scores: list[Suitability]) -> float:
    max_score = Suitability.MORE_SUITABLE.value
    total = sum(score.value for score in scores)
    normalized = total / (len(scores) * max_score)
    return round(normalized, 2)


def main():
    summer_temp = 30
    winter_temp = 5
    humidity = 35
    precipitation = 1200
    dry_days = 20
    wind_data = {
        "OC": 40.0,
        "PO": 30.0,
        "AC15_30": 20.0,
        "AC30": 10.0
    }
    distance = 150
    honey_yield = 35
    lux_morning = 30000
    lux_midday = 80000
    lux_winter = 10000

    scores = [
        evaluate_summer_temperature(summer_temp),
        evaluate_winter_temperature(winter_temp),
        evaluate_relative_humidity(humidity),
        evaluate_precipitation_conditions(precipitation, dry_days),
        evaluate_wind_speed(wind_data),
        evaluate_forage(honey_yield),
        evaluate_lux(lux_morning, lux_midday, lux_winter),
        evaluate_water_source(distance)
    ]

    final_score = calculate_overall_score(scores)
    print("Bewertungs-Score:", final_score)
    db = SessionLocal()
    try:
        criterion_repo = CriterionRepository(db)
        comparison_repo = PairwiseComparisonRepository(db)
        normalization_repo = NormalizationParameterRepository(db)
        user_repo = UserRepository(db)
        sensor_data_repo = SensorDataRepository(db);
        apiary_repo = ApiaryRepository(db)
        water_source_repo = WaterSourceRepository(db)

        sensor_agg_service = SensorAggregationService(sensor_data_repo, water_source_repo)
        ahp_service = AhpUserService(criterion_repo, comparison_repo, normalization_repo)
        evaluation_runner = EvaluationRunner(sensor_agg_service, ahp_service, user_repo, apiary_repo, db)

        user_id = 1
        station = "Bienenstand_6"
        year = 2024
        mac = "0eddd296-1275-40e5-9b2a-ea9c34aa5b60"

        score = evaluation_runner.evaluate_station(user_id, station, year, mac)
        print(f"Gesamtscore für Station '{station}': {score:.4f}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
