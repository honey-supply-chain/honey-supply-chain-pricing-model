from datetime import datetime

from si.repository.water_source_repository import WaterSourceRepository


class SensorAggregationService:
    def __init__(self, repository, water_source_repository: WaterSourceRepository):
        self.repository = repository
        self.water_source_repository = water_source_repository

    def get_average_of_daily_max_temperatures(self, station: str, start: datetime, end: datetime) -> float:
        results = self.repository.find_daily_max_temperatures(station, start, end)
        values = [r[1] if r[1] is not None else 0 for r in results]
        return sum(values) / len(values) if values else 0.0

    def get_average_winter_temperature(self, station: str, year: int) -> float:
        jan_feb_start = datetime(year, 1, 1, 0, 0, 0)
        jan_feb_end = datetime(year, 3, 1, 0, 0, 0)
        oct_dec_start = datetime(year, 10, 1, 0, 0, 0)
        oct_dec_end = datetime(year + 1, 1, 1, 0, 0, 0)

        jan_feb_avg = self._average_daily_temperature(station, jan_feb_start, jan_feb_end)
        oct_dec_avg = self._average_daily_temperature(station, oct_dec_start, oct_dec_end)
        return (jan_feb_avg + oct_dec_avg) / 2.0

    def _average_daily_temperature(self, station: str, start: datetime, end: datetime) -> float:
        results = self.repository.find_daily_average_temperature(station, start, end)
        values = [r[1] if r[1] is not None else 0 for r in results]
        return sum(values) / len(values) if values else 0.0

    def get_average_humidity(self, station: str, start: datetime, end: datetime) -> float:
        results = self.repository.find_daily_average_humidity(station, start, end)
        values = [r[1] if r[1] is not None else 0 for r in results]
        return sum(values) / len(values) if values else 0.0

    def get_total_precipitation(self, station: str, start: datetime, end: datetime) -> float:
        results = self.repository.find_daily_precipitation(station, start, end)
        return sum(r[1] if r[1] is not None else 0 for r in results)

    def get_dry_days(self, station: str, start: datetime, end: datetime) -> int:
        daily_rain_list = self.repository.find_daily_rain_sums(station, start, end)
        return self._get_longest_dry_period(daily_rain_list)

    @staticmethod
    def _get_longest_dry_period(daily_rain_list) -> int:
        max_streak = 0
        current_streak = 0
        for day in daily_rain_list:
            if day.total_rain < 0.1:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0
        return max_streak

    def get_wind_category_day_counts(self, station: str, start: datetime, end: datetime) -> dict[str, float]:
        list_ = self.repository.find_wind_category_day_counts(station, start, end)
        result = {}
        for entry in list_:
            if len(entry) >= 2 and isinstance(entry[0], str) and isinstance(entry[1], (int, float)):
                category = entry[0]
                count = float(entry[1])
                result[category] = count
        return result

    def get_avg_morning_summer_lux(self, station: str, start: datetime, end: datetime) -> float:
        avg = self.repository.get_avg_morning_summer_lux(station, start, end)
        return avg if avg is not None else 0.0

    def get_avg_midday_summer_lux(self, station: str, start: datetime, end: datetime) -> float:
        avg = self.repository.get_avg_midday_summer_lux(station, start, end)
        return avg if avg is not None else 0.0

    def get_avg_winter_lux(self, station: str, year: int) -> float:
        from datetime import datetime

        start_jan_mar = datetime(year, 1, 1, 0, 0, 0)
        end_jan_mar = datetime(year, 3, 31, 23, 59, 59)

        start_oct_dec = datetime(year, 10, 1, 0, 0, 0)
        end_oct_dec = datetime(year, 12, 31, 23, 59, 59)

        jan_mar_avg = self.repository.get_avg_winter_lux(station, year, start_jan_mar, end_jan_mar)
        oct_dec_avg = self.repository.get_avg_winter_lux(station, year, start_oct_dec, end_oct_dec)

        has_jan_mar = jan_mar_avg is not None
        has_oct_dec = oct_dec_avg is not None

        if has_jan_mar and has_oct_dec:
            return (jan_mar_avg + oct_dec_avg) / 2.0
        elif has_jan_mar:
            return jan_mar_avg
        elif has_oct_dec:
            return oct_dec_avg
        else:
            return 0.0

    def get_honey_harvest(self, station: str, start: datetime, end: datetime) -> float:
        weights = self.repository.find_weights_between(station, start, end)
        if not weights:
            return 0.0
        return self._calculate_honey_harvest(weights)

    def _calculate_honey_harvest(self, weights: list) -> float:
        total_harvest = 0.0
        last_weight = weights[0].weight

        for i in range(1, len(weights)):
            current = weights[i].weight
            diff = current - last_weight

            if diff > 3:
                total_harvest -= diff
                print(f"Zarge aufgesetzt: {diff} , Timestamp: {weights[i].time}")
            elif diff < -5.0:
                print(f"Honig entnommen: {-diff} , Timestamp: {weights[i].time}")
                total_harvest += -diff

            last_weight = current

        return total_harvest

    def get_water_source_distance(self, apiary) -> float:
        water_source = self.water_source_repository.find_by_apiary(apiary)
        return water_source.distance if water_source else 0.0

    def build_sensor_input_map(self, station: str, year: int, apiary) -> dict:
        from datetime import datetime

        def get_date(y, m, d):
            return datetime(y, m, d)

        map_ = {}

        mai_start = get_date(year, 5, 1)
        august_end = get_date(year, 8, 31)

        jahr_start = get_date(year, 1, 1)
        jahr_end = get_date(year, 12, 31)

        tracht_start = get_date(year, 4, 1)
        tracht_end = get_date(year, 8, 1)

        map_["summer_temperature"] = {
            "summer_temperature": self.get_average_of_daily_max_temperatures(station, mai_start, august_end)}
        map_["winter_temperature"] = {
            "winter_temperature": self.get_average_winter_temperature(station, year)}
        map_["humidity"] = {"humidity": self.get_average_humidity(station, jahr_start, jahr_end)}
        map_["precipitation"] = {
            "precipitation": self.get_total_precipitation(station, jahr_start, jahr_end),
            "dry_days": float(self.get_dry_days(station, jahr_start, jahr_end))
        }
        map_["wind_speed"] = self.get_wind_category_day_counts(station, jahr_start, jahr_end)
        map_["water_source"] = {"water_source": self.get_water_source_distance(apiary)}
        map_["lightintensity"] = {
            "lux_morgens_sommer": self.get_avg_morning_summer_lux(station, mai_start, august_end),
            "lux_mittags_sommer": self.get_avg_midday_summer_lux(station, mai_start, august_end),
            "lux_winter": self.get_avg_winter_lux(station, year)
        }
        map_["honey_harvest"] = {"honey_harvest": self.get_honey_harvest(station, tracht_start, tracht_end)}

        return map_
