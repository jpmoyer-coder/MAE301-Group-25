from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from src.baseline import HistoricalAverageBaseline
from src.config import BASELINE_PATH, DATA_PATH, METRICS_PATH, MODEL_PATH


FEATURE_COLUMNS = ["day_of_week", "hour", "minute", "restaurant"]
TARGET_COLUMN = "delivery_fee"


def load_data(data_path: Path = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(data_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def build_pipeline() -> Pipeline:
    categorical_features = ["day_of_week", "restaurant"]
    numeric_features = ["hour", "minute"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical_features),
            ("numeric", "passthrough", numeric_features),
        ]
    )

    model = RandomForestRegressor(n_estimators=200, random_state=42)

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )


def train_models(
    data_path: Path = DATA_PATH,
    model_path: Path = MODEL_PATH,
    baseline_path: Path = BASELINE_PATH,
) -> dict[str, float]:
    df = load_data(data_path)
    features = df[FEATURE_COLUMNS]
    target = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=0.2, random_state=42
    )

    ml_pipeline = build_pipeline()
    ml_pipeline.fit(X_train, y_train)
    ml_predictions = ml_pipeline.predict(X_test)
    ml_mae = mean_absolute_error(y_test, ml_predictions)

    baseline_training_frame = X_train.copy()
    baseline_training_frame[TARGET_COLUMN] = y_train.to_numpy()
    baseline_model = HistoricalAverageBaseline().fit(baseline_training_frame)
    baseline_predictions = baseline_model.predict(X_test)
    baseline_mae = mean_absolute_error(y_test, baseline_predictions)

    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(ml_pipeline, model_path)
    joblib.dump(baseline_model, baseline_path)

    metrics = {
        "ml_mae": round(float(ml_mae), 4),
        "baseline_mae": round(float(baseline_mae), 4),
    }
    METRICS_PATH.write_text(
        "\n".join(
            [
                "Starship Delivery Fee Optimization Metrics",
                f"ML MAE: {metrics['ml_mae']}",
                f"Baseline MAE: {metrics['baseline_mae']}",
            ]
        ),
        encoding="utf-8",
    )

    return metrics


def main() -> None:
    metrics = train_models()
    print(f"ML model saved to {MODEL_PATH}")
    print(f"Baseline lookup saved to {BASELINE_PATH}")
    print(f"ML MAE: {metrics['ml_mae']:.4f}")
    print(f"Baseline MAE: {metrics['baseline_mae']:.4f}")


if __name__ == "__main__":
    main()
