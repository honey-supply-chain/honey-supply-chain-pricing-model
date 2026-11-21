from sqlalchemy import func, and_, cast, text, extract, or_
from sqlalchemy.types import Date
from datetime import datetime

from si.models.sensor_data import SensorData
from si.dto import DailyRainSummary


class SensorDataRepository:

    def __init__(self, db_session):
        self.db = db_session

    def find_daily_max_temperatures(self, station: str, start: datetime, end: datetime):
        result = (
            self.db.query(
                func.date(SensorData.time).label("date"),
                func.max(SensorData.temperature).label("max_temp")
            )
            .filter(
                and_(
                    SensorData.station == station,
                    SensorData.time >= start,
                    SensorData.time <= end
                )
            )
            .group_by(func.date(SensorData.time))
            .all()
        )
        return result

    def find_daily_average_temperature(self, station: str, start: datetime, end: datetime):
        result = (
            self.db.query(
                func.date(SensorData.time).label("date"),
                func.avg(SensorData.temperature).label("avg_temp")
            )
            .filter(
                and_(
                    SensorData.station == station,
                    SensorData.time >= start,
                    SensorData.time <= end
                )
            )
            .group_by(func.date(SensorData.time))
            .all()
        )
        return result

    def find_daily_average_humidity(self, station: str, start: datetime, end: datetime):
        result = (
            self.db.query(
                func.date(SensorData.time).label("date"),
                func.avg(SensorData.humidity).label("avg_humidity")
            )
            .filter(
                and_(
                    SensorData.station == station,
                    SensorData.time >= start,
                    SensorData.time <= end
                )
            )
            .group_by(func.date(SensorData.time))
            .all()
        )
        return result

    def find_daily_precipitation(self, station: str, start: datetime, end: datetime) -> list[tuple[datetime, float]]:
        results = (
            self.db.query(
                cast(SensorData.time, Date).label('day'),
                func.sum(SensorData.rain).label('total_rain')
            )
            .filter(
                SensorData.station == station,
                SensorData.time.between(start, end)
            )
            .group_by(cast(SensorData.time, Date))
            .order_by(cast(SensorData.time, Date))
            .all()
        )
        return results

    def find_daily_rain_sums(self, station: str, start: datetime, end: datetime) -> list[DailyRainSummary]:
        rows = (
            self.db.query(
                cast(SensorData.time, Date).label('day'),
                func.sum(SensorData.rain).label('total_rain')
            )
            .filter(
                SensorData.station == station,
                SensorData.time.between(start, end)
            )
            .group_by(cast(SensorData.time, Date))
            .order_by(cast(SensorData.time, Date))
            .all()
        )
        return [DailyRainSummary(day=row.day, total_rain=row.total_rain) for row in rows]

    def find_wind_category_day_counts(self, station: str, start: datetime, end: datetime) -> list[tuple[str, int]]:
        sql = text("""
            SELECT
                category,
                COUNT(*) AS day_count
            FROM (
                SELECT
                    day,
                    CASE
                        WHEN max_wind_speed * 3.6 < 10 THEN 'OC'
                        WHEN max_wind_speed * 3.6 < 15 THEN 'PO'
                        WHEN max_wind_speed * 3.6 < 30 THEN 'AC15_30'
                        ELSE 'AC30'
                    END AS category
                FROM (
                    SELECT
                        DATE(time) AS day,
                        MAX(wind_speed) AS max_wind_speed
                    FROM sensor_data
                    WHERE station = :station
                      AND time BETWEEN :start AND :end
                    GROUP BY DATE(time)
                ) AS daily_max
            ) AS categorized
            GROUP BY category
        """)

        result = self.db.execute(sql, {
            "station": station,
            "start": start,
            "end": end
        }).fetchall()

        return result

    def get_avg_morning_summer_lux(self, station: str, start: datetime, end: datetime) -> float | None:
        result = (
            self.db.query(func.avg(SensorData.light_intensity))
            .filter(
                SensorData.station == station,
                SensorData.time.between(start, end),
                extract('hour', SensorData.time).between(6, 11),
                extract('month', SensorData.time).between(6, 8)
            )
            .scalar()
        )
        return result

    def get_avg_midday_summer_lux(self, station: str, start: datetime, end: datetime) -> float | None:
        result = (
            self.db.query(func.avg(SensorData.light_intensity))
            .filter(
                SensorData.station == station,
                SensorData.time.between(start, end),
                extract('hour', SensorData.time).between(12, 15),
                extract('month', SensorData.time).between(6, 8)
            )
            .scalar()
        )
        return result

    def get_avg_winter_lux(self, station: str, year: int, start: datetime, end: datetime) -> float:
        result = (
            self.db.query(func.avg(SensorData.light_intensity))
            .filter(
                SensorData.station == station,
                or_(
                    and_(
                        func.extract('month', SensorData.time).between(1, 3),
                        func.extract('year', SensorData.time) == year
                    ),
                    and_(
                        func.extract('month', SensorData.time).between(10, 12),
                        func.extract('year', SensorData.time) == year
                    )
                ),
                SensorData.time.between(start, end)
            )
            .scalar()
        )
        return result

    def find_weights_between(self, station: str, start: datetime, end: datetime) -> list[SensorData]:
        results = (
            self.db.query(SensorData)
            .filter(
                SensorData.station == station,
                SensorData.time.between(start, end)
            )
            .order_by(SensorData.time.asc())
            .all()
        )
        return results

    def get_all_sensor_data_for_station(self, station: str) -> list[SensorData]:
        """
        Ruft alle Sensordaten für eine spezifische Station ab, ohne zeitliche Begrenzung.
        # ... (docstring) ...
        """
        results = (
            self.db.query(SensorData)
            .filter(SensorData.station == station)
            .order_by(SensorData.time.asc())
            .all()
        )
        return results
