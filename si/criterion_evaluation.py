# criterion_evaluation.py


from common.suitability import Suitability


def evaluate_summer_temperature(temperature: float) -> Suitability:
    if temperature > 38:
        return Suitability.UNSUITABLE
    if 25 <= temperature <= 38:
        return Suitability.MORE_SUITABLE
    return Suitability.SUITABLE


def evaluate_winter_temperature(temperature: float) -> Suitability:
    if 3 <= temperature <= 10:
        return Suitability.MORE_SUITABLE
    if (0 <= temperature < 3) or (10 < temperature <= 12):
        return Suitability.SUITABLE
    return Suitability.LESS_SUITABLE


def evaluate_relative_humidity(relative_humidity: float) -> Suitability:
    if relative_humidity < 15:
        return Suitability.UNSUITABLE
    if relative_humidity <= 40:
        return Suitability.SUITABLE
    return Suitability.MORE_SUITABLE


def evaluate_precipitation_conditions(precipitation_amount: float, dry_days: int) -> Suitability:
    precipitation_score = evaluate_precipitation(precipitation_amount)
    drought_score = evaluate_drought_period(dry_days)
    combined_score = 0.5 * precipitation_score.value + 0.5 * drought_score.value
    return map_numeric_to_suitability(combined_score)


def evaluate_precipitation(precipitation_mm: float) -> Suitability:
    if precipitation_mm < 900 or precipitation_mm > 1600:
        return Suitability.UNSUITABLE
    if (900 <= precipitation_mm < 1100) or (1400 < precipitation_mm <= 1600):
        return Suitability.SUITABLE
    return Suitability.MORE_SUITABLE


def evaluate_drought_period(dry_days: int) -> Suitability:
    if dry_days > 45:
        return Suitability.UNSUITABLE
    if dry_days >= 31:
        return Suitability.LESS_SUITABLE
    if dry_days >= 16:
        return Suitability.SUITABLE
    return Suitability.MORE_SUITABLE


def map_numeric_to_suitability(score: float) -> Suitability:
    if score >= 7.0:
        return Suitability.MORE_SUITABLE
    if score >= 4.0:
        return Suitability.SUITABLE
    if score >= 2.0:
        return Suitability.LESS_SUITABLE
    return Suitability.UNSUITABLE


def evaluate_wind_speed(category_counts: dict[str, float]) -> Suitability:
    total_days = sum(category_counts.values())
    if total_days == 0:
        return Suitability.LESS_SUITABLE

    score = (
                    category_counts.get("OC", 0.0) * 9.0 +
                    category_counts.get("PO", 0.0) * 5.0 +
                    category_counts.get("AC15_30", 0.0) * 3.0 +
                    category_counts.get("AC30", 0.0) * 1.0
            ) / total_days

    return map_numeric_to_suitability(score)

def evaluate_forage(honey_yield_kg: int) -> Suitability:
    if honey_yield_kg < 20:
        return Suitability.UNSUITABLE
    if 20 <= honey_yield_kg < 30:
        return Suitability.LESS_SUITABLE
    if 30 <= honey_yield_kg <= 40:
        return Suitability.SUITABLE
    return Suitability.MORE_SUITABLE


def evaluate_lux(avg_morning_summer_lux: float, avg_midday_summer_lux: float, avg_winter_lux: float) -> Suitability:
    norm_morning = normalize(avg_morning_summer_lux)
    norm_midday = 1.0 - normalize(avg_midday_summer_lux)
    norm_winter = normalize(avg_winter_lux)

    summer_score = norm_morning * 0.4 + norm_midday * 0.6
    combined_score = summer_score * 0.5 + norm_winter * 0.5

    return map_to_ahp_score(combined_score)

def evaluate_water_source(distance_m: float) -> Suitability:
    if distance_m > 700:
        return Suitability.UNSUITABLE
    if 500 <= distance_m <= 700:
        return Suitability.LESS_SUITABLE
    if 200 <= distance_m < 500:
        return Suitability.SUITABLE
    return Suitability.MORE_SUITABLE


def normalize(lux: float) -> float:
    MIN_LUX = 0.0
    MAX_LUX = 100_000.0
    return min(1.0, max(0.0, (lux - MIN_LUX) / (MAX_LUX - MIN_LUX)))


def map_to_ahp_score(norm_score: float) -> Suitability:
    if norm_score >= 0.75:
        return Suitability.MORE_SUITABLE
    if norm_score >= 0.5:
        return Suitability.SUITABLE
    if norm_score >= 0.3:
        return Suitability.LESS_SUITABLE
    return Suitability.UNSUITABLE
