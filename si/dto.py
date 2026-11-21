from datetime import date


class DailyRainSummary:
    def __init__(self, day: date, total_rain: float):
        self.day = day
        self.total_rain = total_rain

    def __repr__(self):
        return f"DailyRainSummary(day={self.day}, total_rain={self.total_rain})"
