from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

import joblib
import pandas as pd

from src.config import BASELINE_PATH, DAY_ORDER, MODEL_PATH


@dataclass
class RecommendationResult:
    current_fee_ml: float
    current_fee_baseline: float
    recommendation: str
    best_time_label: str
    best_fee_ml: float
    savings: float


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


def recommend_order_time(
    day_of_week: str,
    hour: int,
    minute: int,
    restaurant: str,
) -> RecommendationResult:
    model = load_model()
    baseline = load_baseline()

    current_features = make_feature_frame(day_of_week, hour, minute, restaurant)
    current_fee_ml = round(float(model.predict(current_features)[0]), 2)
    current_fee_baseline = round(float(baseline.predict(current_features)[0]), 2)

    best_day = day_of_week
    best_hour = hour
    best_minute = minute
    best_fee_ml = current_fee_ml

    for slot_day, slot_hour, slot_minute in next_time_slots(day_of_week, hour, minute):
        slot_features = make_feature_frame(slot_day, slot_hour, slot_minute, restaurant)
        slot_fee = round(float(model.predict(slot_features)[0]), 2)
        if slot_fee < best_fee_ml:
            best_day = slot_day
            best_hour = slot_hour
            best_minute = slot_minute
            best_fee_ml = slot_fee

    savings = round(current_fee_ml - best_fee_ml, 2)
    best_time_label = f"{best_day} at {best_hour:02d}:{best_minute:02d}"

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
    )


def main() -> None:
    result = recommend_order_time(
        day_of_week="Friday",
        hour=18,
        minute=30,
        restaurant="Comet Cafe",
    )
    print(f"ML predicted current fee: ${result.current_fee_ml:.2f}")
    print(f"Baseline current fee: ${result.current_fee_baseline:.2f}")
    print(result.recommendation)


if __name__ == "__main__":
    main()
