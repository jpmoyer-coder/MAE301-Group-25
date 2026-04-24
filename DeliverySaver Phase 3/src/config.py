from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "fee_trends_from_pdf.csv"
ARTIFACTS_DIR = BASE_DIR / "artifacts"
MODEL_PATH = ARTIFACTS_DIR / "delivery_fee_model.joblib"
BASELINE_PATH = ARTIFACTS_DIR / "baseline_lookup.joblib"
METRICS_PATH = ARTIFACTS_DIR / "metrics.txt"

DAY_ORDER = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
