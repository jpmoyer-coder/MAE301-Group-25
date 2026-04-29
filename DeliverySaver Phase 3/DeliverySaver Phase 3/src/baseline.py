import pandas as pd


class HistoricalAverageBaseline:
    """Simple fallback model based on historical averages."""

    def __init__(self) -> None:
        self.lookup = {}
        self.restaurant_lookup = {}
        self.global_mean = 0.0

    def fit(self, df: pd.DataFrame) -> "HistoricalAverageBaseline":
        grouped = (
            df.groupby(["restaurant", "day_of_week", "hour"])["delivery_fee"]
            .mean()
            .round(2)
        )
        self.lookup = grouped.to_dict()
        self.restaurant_lookup = (
            df.groupby("restaurant")["delivery_fee"].mean().round(2).to_dict()
        )
        self.global_mean = round(float(df["delivery_fee"].mean()), 2)
        return self

    def predict(self, features: pd.DataFrame) -> list[float]:
        predictions = []
        for row in features.to_dict(orient="records"):
            key = (row["restaurant"], row["day_of_week"], row["hour"])
            value = self.lookup.get(
                key,
                self.restaurant_lookup.get(row["restaurant"], self.global_mean),
            )
            predictions.append(round(float(value), 2))
        return predictions
