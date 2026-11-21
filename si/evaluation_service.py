from si.models.evaluation import Evaluation
from datetime import datetime

from si.repository.evaluation_repository import EvaluationRepository


class EvaluationService:
    def __init__(self, db_session):
        self.repository = EvaluationRepository(db_session)

    def save_evaluation(self, score_details: dict[str, dict[str, float]], total_score: float, apiary) -> Evaluation:
        
        def get_score(criterion, score_type):
            return score_details.get(criterion, {}).get(score_type, 0.0)

        evaluation = Evaluation()
        evaluation.date = datetime.utcnow()
        evaluation.total = total_score

        evaluation.honey_harvest = get_score("honey_harvest", "normalized_score")
        evaluation.summer_temperature = get_score("summer_temperature", "normalized_score")
        evaluation.winter_temperature = get_score("winter_temperature", "normalized_score")
        evaluation.light_intensity = get_score("lightintensity", "normalized_score")
        evaluation.wind_speed = get_score("wind_speed", "normalized_score")
        evaluation.humidity = get_score("humidity", "normalized_score")
        evaluation.precipitation = get_score("precipitation", "normalized_score")
        evaluation.water_source = get_score("water_source", "normalized_score")

        evaluation.weighted_honey_harvest = get_score("honey_harvest", "weighted_score")
        evaluation.weighted_summer_temperature = get_score("summer_temperature", "weighted_score")
        evaluation.weighted_winter_temperature = get_score("winter_temperature", "weighted_score")
        evaluation.weighted_light_intensity = get_score("lightintensity", "weighted_score")
        evaluation.weighted_wind_speed = get_score("wind_speed", "weighted_score")
        evaluation.weighted_humidity = get_score("humidity", "weighted_score")
        evaluation.weighted_precipitation = get_score("precipitation", "weighted_score")
        evaluation.weighted_water_source = get_score("water_source", "weighted_score")

        evaluation.apiary = apiary

        return self.repository.add(evaluation)
