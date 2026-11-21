from dataclasses import dataclass


@dataclass
class DailyRainSummary:
    day: str
    total_rain: float
