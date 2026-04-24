import streamlit as st

from src.config import BASELINE_PATH, METRICS_PATH, MODEL_PATH
from src.data_utils import load_aggregate_data
from src.recommend import recommend_order_time
from src.train_model import train_models


def ensure_models() -> dict[str, float]:
    if not MODEL_PATH.exists() or not BASELINE_PATH.exists():
        return train_models()

    metrics = {"ml_mae": None, "baseline_mae": None}
    if METRICS_PATH.exists():
        for line in METRICS_PATH.read_text(encoding="utf-8").splitlines():
            if line.startswith("ML MAE:"):
                metrics["ml_mae"] = float(line.split(": ", 1)[1])
            if line.startswith("Baseline MAE:"):
                metrics["baseline_mae"] = float(line.split(": ", 1)[1])
    return metrics


def main() -> None:
    st.set_page_config(page_title="DeliverySaver Phase 3", page_icon="ðŸš€")

    st.title("DeliverySaver Phase 3")
    st.write(
        "This MVP treats the observed Friday fee curve as an all-days aggregate pattern and recommends whether to order now or wait for a cheaper time."
    )

    data = load_aggregate_data()
    metrics = ensure_models()

    st.subheader("Model Comparison")
    col1, col2 = st.columns(2)
    col1.metric("ML MAE", "N/A" if metrics["ml_mae"] is None else f"{metrics['ml_mae']:.4f}")
    col2.metric(
        "Baseline MAE",
        "N/A" if metrics["baseline_mae"] is None else f"{metrics['baseline_mae']:.4f}",
    )

    st.subheader("Observed Fee Data")
    st.dataframe(data, use_container_width=True)

    st.subheader("Recommendation Demo")
    day_of_week = st.selectbox("Day of week", options=data["day_of_week"].drop_duplicates().tolist())
    hour = st.selectbox("Hour", options=sorted(data["hour"].unique().tolist()))
    minute = st.selectbox("Minute", options=sorted(data["minute"].unique().tolist()))
    restaurant = st.selectbox("Restaurant", options=sorted(data["restaurant"].unique()))

    if st.button("Get Recommendation"):
        result = recommend_order_time(
            day_of_week=day_of_week,
            hour=hour,
            minute=minute,
            restaurant=restaurant,
        )
        st.success(result.recommendation)

        col1, col2, col3 = st.columns(3)
        col1.metric("Current Fee", f"${result.current_fee_ml:.2f}")
        col2.metric("Baseline Fee", f"${result.current_fee_baseline:.2f}")
        col3.metric("Potential Savings", f"${result.savings:.2f}")

        if result.data_source == "observed":
            st.caption("The current fee came directly from the aggregate hourly fee data for this exact time.")
        else:
            st.caption("The current fee came from the trained model because no exact CSV row matched this input.")

        st.write(f"Best time in the next 3 hours: **{result.best_time_label}**")
        st.write(f"Predicted fee at that time: **${result.best_fee_ml:.2f}**")

    st.subheader("Retrain Models")
    if st.button("Retrain from Current CSV"):
        updated_metrics = train_models()
        st.success("Models retrained successfully.")
        st.write(
            f"Updated metrics: ML MAE = {updated_metrics['ml_mae']:.4f}, "
            f"Baseline MAE = {updated_metrics['baseline_mae']:.4f}"
        )


if __name__ == "__main__":
    main()

