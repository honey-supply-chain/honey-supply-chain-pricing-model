from si.evaluation_service import EvaluationService


class EvaluationRunner:
    def __init__(self, sensor_aggregation_service, ahp_user_service, user_repository, apiary_repository, db_session):
        self.sensor_aggregation_service = sensor_aggregation_service
        self.ahp_user_service = ahp_user_service
        self.user_repository = user_repository
        self.apiary_repository = apiary_repository
        self.db_session = db_session

    def evaluate_station(self, user_id: int, station: str, year: int, mac: str) -> float:
        user = self.user_repository.find_by_id(user_id)
        apiary = self.apiary_repository.find_by_mac(mac)
        if not user:
            raise Exception("User not found")

        sensor_data = self.sensor_aggregation_service.build_sensor_input_map(station, year, apiary)

        for criterion, values in sensor_data.items():
            print(f"Kriterium: {criterion}")
            for sub_key, value in values.items():
                print(f"  {sub_key}: {value}")

        bewertung, score_details = self.ahp_user_service.run_ahp_with_sensor_data_for_user_and_station(user, station, sensor_data)

        service = EvaluationService(self.db_session)
        service.save_evaluation(score_details, bewertung, apiary)
        return bewertung
