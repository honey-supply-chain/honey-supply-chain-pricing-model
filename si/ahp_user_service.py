from typing import Dict, List

from common.normalization import normalize_saaty_score
from si.ahp import Ahp
from si.evaluation_service import EvaluationService
from si.models.criterion import Criterion
from si.models.pairwise_comparison import PairwiseComparison
from si.models.user import User
from si.repository.criterion_repository import CriterionRepository
from si.repository.normalization_parameter_repository import NormalizationParameterRepository
from si.repository.pairwise_comparison_repository import PairwiseComparisonRepository

from si.criterion_evaluation import (
    evaluate_summer_temperature,
    evaluate_winter_temperature,
    evaluate_relative_humidity,
    evaluate_precipitation_conditions,
    evaluate_wind_speed,
    evaluate_forage,
    evaluate_lux,
    evaluate_water_source,
)


class AhpUserService:
    def __init__(self, criterion_repo: CriterionRepository,
                 comparison_repo: PairwiseComparisonRepository,
                 normalization_repo: NormalizationParameterRepository):
        self.criterion_repo = criterion_repo
        self.comparison_repo = comparison_repo
        self.normalization_repo = normalization_repo

    def run_ahp_with_sensor_data_for_user_and_station(self, user: User, station_name: str,
                                                      sensor_data: Dict[str, Dict[str, float]]) -> float:
        criteria: List[Criterion] = self.criterion_repo.find_all()
        n = len(criteria)

        if n == 0:
            print(f"Keine Kriterien für User {user.username}")
            return 0.0

        matrix = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
        comparisons: List[PairwiseComparison] = self.comparison_repo.find_all_by_user(user)

        for comp in comparisons:
            i = criteria.index(comp.criterionA)
            j = criteria.index(comp.criterionB)
            if i != -1 and j != -1:
                matrix[i][j] = comp.importance
                matrix[j][i] = 1.0 / comp.importance

        labels = [c.name for c in criteria]

        normalized = Ahp.normalize_matrix(matrix)
        weights = Ahp.calculate_weights(normalized)
        Ahp.print_vector(weights, labels)

        cr = Ahp.compute_consistency_ratio(matrix, weights)
        print(f"User: {user.username} → Konsistenzverhältnis CR: {cr:.4f} {'✓ Konsistent' if cr < 0.1 else '✗ Nicht konsistent'}")
        if cr >= 0.1:
            print("Warnung: Die Kriterienvergleichsmatrix ist nicht konsistent genug!")

        gewichtungen = {label: weights[i] for i, label in enumerate(labels)}

        bewertung = 0.0
        score_details = {}
        for criterion in labels:
            gewicht = gewichtungen.get(criterion, 0.0)
            ahp_score = self.evaluate_with_criteration_evaluation(criterion, sensor_data)
            normalized_score = normalize_saaty_score(ahp_score)
            weighted_score = gewicht * normalized_score
            bewertung += weighted_score

            score_details[criterion] = {
                "normalized_score": normalized_score,
                "weighted_score": weighted_score
            }

        print(f"Station {station_name} – Bewertung: {bewertung:.4f}")
        return bewertung, score_details

    def normalize(self, criterion_name: str, value: float) -> float:
        criterion = self.criterion_repo.find_by_name(criterion_name)
        if not criterion:
            return value

        param = self.normalization_repo.find_by_criterion(criterion)
        if not param or param.min_value is None or param.max_value is None:
            return value

        min_val = param.min_value
        max_val = param.max_value

        if max_val == min_val:
            return 0.0

        normalized = (value - min_val) / (max_val - min_val)
        return max(0.0, min(1.0, normalized))

    def evaluate_with_criteration_evaluation(self, criterion: str,
                                             sensordaten: Dict[str, Dict[str, float]]) -> int:
        inner_map = sensordaten.get(criterion, {})

        match criterion.lower():
            case "summer_temperature":
                return evaluate_summer_temperature(inner_map.get("summer_temperature", 0.0)).value

            case "winter_temperature":
                return evaluate_winter_temperature(inner_map.get("winter_temperature", 0.0)).value

            case "humidity":
                return evaluate_relative_humidity(inner_map.get("humidity", 0.0)).value

            case "precipitation":
                niederschlag = inner_map.get("precipitation", 0.0)
                trockentage = int(inner_map.get("dry_days", 0.0))
                return evaluate_precipitation_conditions(niederschlag, trockentage).value

            case "wind_speed":
                return evaluate_wind_speed(inner_map).value

            case "water_source":
                return evaluate_water_source(inner_map.get("water_source", 0.0)).value

            case "honey_harvest":
                return evaluate_forage(int(inner_map.get("honey_harvest", 0.0))).value

            case "lightintensity":
                return evaluate_lux(
                    inner_map.get("lux_morgens_sommer", 0.0),
                    inner_map.get("lux_mittags_sommer", 0.0),
                    inner_map.get("lux_winter", 0.0)
                ).value

            case _:
                default_value = next(iter(inner_map.values()), 0.0)
                return self.normalize(criterion, default_value)

