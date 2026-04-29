from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

import joblib
import pandas as pd

from src.config import BASELINE_PATH, DATA_PATH, DAY_ORDER, MODEL_PATH
from src.data_utils import load_aggregate_data


@dataclass
class RecommendationResult:
    current_fee_ml: float
    current_fee_baseline: float
    recommendation: str
    best_time_label: str
    best_fee_ml: float
    savings: float
    data_source: str


def format_best_time_label(best_day: str, best_hour: int, best_minute: int, requested_day: str) -> str:
    """Format the recommendation as an aggregate daily time, not a weekday-specific label."""
    time_label = f"{best_hour:02d}:{best_minute:02d}"
    if best_day == requested_day:
        return time_label
    return f"next day at {time_label}"


def load_model(model_path: Path = MODEL_PATH):
    if not model_path.exists():
        raise FileNotFoundError(
            f"Model not found at {model_path}. Run `python train_model.py` first."
        )
    return joblib.load(model_path)


def load_baseline(baseline_path: Path = BASELINE_PATH):
    if not baseline_path.exists():
        raise FileNotFoundError(
            f"Baseline model not found at {baseline_path}. Run `python train_model.py` first."
        )
    return joblib.load(baseline_path)


def load_data(data_path: Path = DATA_PATH) -> pd.DataFrame:
    return load_aggregate_data(data_path)


def make_feature_frame(day_of_week: str, hour: int, minute: int, restaurant: str) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "day_of_week": day_of_week,
                "hour": hour,
                "minute": minute,
                "restaurant": restaurant,
            }
        ]
    )


def next_time_slots(day_of_week: str, hour: int, minute: int, horizon_hours: int = 3) -> list[tuple[str, int, int]]:
    start_index = DAY_ORDER.index(day_of_week)
    start_dt = datetime(2026, 1, 5 + start_index, hour, minute)

    slots = []
    for step in range(1, horizon_hours * 4 + 1):
        future_dt = start_dt + timedelta(minutes=15 * step)
        slots.append((future_dt.strftime("%A"), future_dt.hour, future_dt.minute))
    return slots


def find_observed_fee(
    df: pd.DataFrame,
    day_of_week: str,
    hour: int,
    minute: int,
    restaurant: str,
) -> float | None:
    match = df[
        (df["day_of_week"] == day_of_week)
        & (df["hour"] == hour)
        & (df["minute"] == minute)
        & (df["restaurant"] == restaurant)
    ]
    if match.empty:
        return None
    return round(float(match.iloc[0]["delivery_fee"]), 2)


def recommend_order_time(
    day_of_week: str,
    hour: int,
    minute: int,
    restaurant: str,
) -> RecommendationResult:
    df = load_data()
    model = load_model()
    baseline = load_baseline()

    current_features = make_feature_frame(day_of_week, hour, minute, restaurant)
    current_fee_baseline = round(float(baseline.predict(current_features)[0]), 2)
    observed_current_fee = find_observed_fee(df, day_of_week, hour, minute, restaurant)

    if observed_current_fee is not None:
        current_fee_ml = observed_current_fee
        data_source = "observed"
    else:
        current_fee_ml = round(float(model.predict(current_features)[0]), 2)
        data_source = "model"

    best_day = day_of_week
    best_hour = hour
    best_minute = minute
    best_fee_ml = current_fee_ml

    for slot_day, slot_hour, slot_minute in next_time_slots(day_of_week, hour, minute):
        observed_slot_fee = find_observed_fee(df, slot_day, slot_hour, slot_minute, restaurant)
        if observed_slot_fee is not None:
            slot_fee = observed_slot_fee
        else:
            slot_features = make_feature_frame(slot_day, slot_hour, slot_minute, restaurant)
            slot_fee = round(float(model.predict(slot_features)[0]), 2)
        if slot_fee < best_fee_ml:
            best_day = slot_day
            best_hour = slot_hour
            best_minute = slot_minute
            best_fee_ml = slot_fee

    savings = round(current_fee_ml - best_fee_ml, 2)
    best_time_label = format_best_time_label(best_day, best_hour, best_minute, day_of_week)

    if savings > 0.1:
        recommendation = f"Wait until {best_time_label} for a lower predicted fee."
    else:
        recommendation = "Order now. A meaningfully cheaper fee was not found in the next 3 hours."

    return RecommendationResult(
        current_fee_ml=current_fee_ml,
        current_fee_baseline=current_fee_baseline,
        recommendation=recommendation,
        best_time_label=best_time_label,
        best_fee_ml=best_fee_ml,
        savings=savings,
        data_source=data_source,
    )


def main() -> None:
    result = recommend_order_time(
        day_of_week="Friday",
        hour=18,
        minute=0,
        restaurant="Starship Aggregate",
    )
    print(f"ML predicted current fee: ${result.current_fee_ml:.2f}")
    print(f"Baseline current fee: ${result.current_fee_baseline:.2f}")
    print(result.recommendation)


if __name__ == "__main__":
    main()
