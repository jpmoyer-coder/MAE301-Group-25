from pathlib import Path

import pandas as pd

from src.config import DATA_PATH, DAY_ORDER


def load_aggregate_data(data_path: Path = DATA_PATH) -> pd.DataFrame:
    """Load the observed fee curve and treat it as an all-days aggregate pattern."""
    df = pd.read_csv(data_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    expanded_frames = []
    base_date = pd.Timestamp("2026-01-05")

    for day_index, day_name in enumerate(DAY_ORDER):
        day_frame = df.copy()
        day_frame["day_of_week"] = day_name
        day_frame["timestamp"] = day_frame.apply(
            lambda row: base_date
            + pd.Timedelta(days=day_index, hours=int(row["hour"]), minutes=int(row["minute"])),
            axis=1,
        )
        expanded_frames.append(day_frame)

    return pd.concat(expanded_frames, ignore_index=True)
