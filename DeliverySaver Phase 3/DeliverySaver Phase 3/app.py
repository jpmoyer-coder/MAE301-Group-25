from datetime import datetime

import streamlit as st

import optimizer
from src.config import DAY_ORDER
from src.recommend import recommend_order_time


APP_TITLE = "Delivery Price Optimizer"
APP_DESCRIPTION = (
    "Compare Uber Eats, DoorDash, and Grubhub for a single menu item and find the cheapest option instantly."
)


@st.cache_data
def load_dataset() -> dict:
    return optimizer.load_optimizer_dataset()


def get_restaurant_names(dataset: dict) -> list[str]:
    return [restaurant["name"] for restaurant in dataset.get("restaurants", [])]


def get_restaurant(dataset: dict, restaurant_name: str) -> dict | None:
    for restaurant in dataset.get("restaurants", []):
        if restaurant.get("name") == restaurant_name:
            return restaurant
    return None


def get_item_names(restaurant: dict | None) -> list[str]:
    if not restaurant:
        return []
    return [item["name"] for item in restaurant.get("items", [])]


def render_css() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(251, 113, 133, 0.14), transparent 26%),
                linear-gradient(180deg, #fffaf5 0%, #fff7ed 100%);
        }
        .block-container {
            max-width: 1100px;
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }
        .hero-card {
            border-radius: 24px;
            border: 1px solid rgba(148, 163, 184, 0.16);
            box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
        }
        .hero-card {
            background: rgba(255, 255, 255, 0.95);
            padding: 1.4rem;
            margin-bottom: 1rem;
        }
        .eyebrow {
            font-size: 0.78rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #ea580c;
            margin-bottom: 0.35rem;
        }
        .hero-title {
            font-size: 2rem;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 0.35rem;
        }
        .hero-copy {
            color: #475569;
            line-height: 1.5;
        }
        h1, h2, h3, h4, h5, h6,
        p, li, label,
        [data-testid="stMarkdownContainer"],
        [data-testid="stText"],
        [data-testid="stCaptionContainer"],
        [data-testid="stMetricLabel"],
        [data-testid="stMetricValue"],
        [data-testid="stMetricDelta"],
        .stSelectbox label,
        .stSlider label {
            color: #0f172a;
        }
        .stSelectbox label,
        .stSlider label,
        [data-testid="stCaptionContainer"] {
            color: #64748b !important;
        }
        .best-card,
        .best-card div,
        .best-card span,
        .best-card p {
            color: #ffffff !important;
        }
        .best-card .card-label {
            color: #fdba74 !important;
        }
        div[data-baseweb="select"] > div {
            background: #292a34 !important;
            color: #f8fafc !important;
        }
        div[data-baseweb="select"] span {
            color: #f8fafc !important;
        }
        div[data-baseweb="select"] svg {
            fill: #f8fafc !important;
        }
        .feature-card {
            border-radius: 24px;
            border: 1px solid rgba(148, 163, 184, 0.16);
            box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
            padding: 1.2rem 1.3rem;
            margin-bottom: 1rem;
        }
        .best-card {
            background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
            color: #ffffff;
        }
        .light-card {
            background: rgba(255, 255, 255, 0.95);
            color: #0f172a;
        }
        .card-label {
            font-size: 0.78rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #fdba74;
            margin-bottom: 0.35rem;
        }
        .light-card .card-label {
            color: #ea580c;
        }
        .card-title {
            font-size: 1.8rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
        }
        .card-price {
            font-size: 1.1rem;
            font-weight: 700;
            margin-bottom: 0.45rem;
        }
        .card-copy {
            line-height: 1.5;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.75rem;
            margin: 0.9rem 0 0.7rem 0;
        }
        .stat-box {
            border-radius: 16px;
            padding: 0.75rem 0.85rem;
            background: rgba(15, 23, 42, 0.06);
        }
        .stat-label {
            font-size: 0.72rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #64748b;
            margin-bottom: 0.2rem;
        }
        .stat-value {
            font-size: 1.35rem;
            font-weight: 800;
            color: #0f172a;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="eyebrow">Delivery Intelligence</div>
            <div class="hero-title">{APP_TITLE}</div>
            <div class="hero-copy">{APP_DESCRIPTION}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_best_option(best_option: dict, rankings: list[dict]) -> None:
    savings = 0.0
    if len(rankings) > 1:
        savings = round(rankings[1]["total_cost"] - best_option["total_cost"], 2)

    st.markdown(
        f"""
        <div class="feature-card best-card">
            <div class="card-label">Best Option</div>
            <div class="card-title">{best_option["app"]}</div>
            <div class="card-price">{optimizer.format_currency(best_option["total_cost"])}</div>
            <div class="card-copy">Saves {optimizer.format_currency(savings)} versus the next cheapest app.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_timing_recommendation(timing_result, selected_day: str, selected_hour: int) -> None:
    st.markdown(
        f"""
        <div class="feature-card light-card">
            <div class="card-label">Starship Timing Recommendation</div>
            <div class="card-copy"><strong>Selected order time:</strong> {selected_day} at {selected_hour:02d}:00</div>
            <div class="card-copy" style="margin-top:0.45rem;">{timing_result.recommendation}</div>
            <div class="stats-grid">
                <div class="stat-box">
                    <div class="stat-label">Current Fee</div>
                    <div class="stat-value">{optimizer.format_currency(timing_result.current_fee_ml)}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Best Time Fee</div>
                    <div class="stat-value">{optimizer.format_currency(timing_result.best_fee_ml)}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Timing Savings</div>
                    <div class="stat-value">{optimizer.format_currency(timing_result.savings)}</div>
                </div>
            </div>
            <div class="card-copy">
                Best order window in the next 3 hours: <strong>{timing_result.best_time_label}</strong>.
                Based on the Starship aggregate hourly fee pattern.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_combined_summary(best_option: dict, rankings: list[dict], timing_result) -> None:
    platform_savings = 0.0
    if len(rankings) > 1:
        platform_savings = round(rankings[1]["total_cost"] - best_option["total_cost"], 2)

    if timing_result.savings > 0.1:
        timing_copy = (
            f"If timing is flexible, wait until <strong>{timing_result.best_time_label}</strong> "
            f"to target about <strong>{optimizer.format_currency(timing_result.savings)}</strong> "
            "in extra Starship fee savings."
        )
    else:
        timing_copy = "Timing does not meaningfully improve the Starship fee in the next 3 hours, so ordering now is reasonable."

    st.markdown(
        f"""
        <div class="feature-card light-card">
            <div class="card-label">Combined Recommendation</div>
            <div class="card-copy">
                Use <strong>{best_option['app']}</strong> for this item at
                <strong>{optimizer.format_currency(best_option['total_cost'])}</strong>.
            </div>
            <div class="card-copy" style="margin-top:0.6rem;">{timing_copy}</div>
            <div class="card-copy" style="margin-top:0.6rem;">
                Platform savings: <strong>{optimizer.format_currency(platform_savings)}</strong>
                versus the next cheapest app.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_platform_card(column, ranking: dict, best_app: str) -> None:
    breakdown = ranking.get("breakdown", {})
    with column:
        with st.container(border=True):
            top_left, top_right = st.columns([2, 1])
            with top_left:
                st.subheader(ranking["app"])
            with top_right:
                if ranking["app"] == best_app:
                    st.success("Cheapest")

            st.metric("Total", optimizer.format_currency(ranking["total_cost"]))
            st.caption("Price breakdown")
            st.write(f"Food: {optimizer.format_currency(breakdown.get('food', 0.0))}")
            st.write(f"Delivery: {optimizer.format_currency(breakdown.get('delivery', 0.0))}")
            st.write(f"Service: {optimizer.format_currency(breakdown.get('service', 0.0))}")
            st.write(f"Tax: {optimizer.format_currency(breakdown.get('tax', 0.0))}")
            st.write(f"Tip: {optimizer.format_currency(breakdown.get('tip', 0.0))}")


def render_platform_comparison(rankings: list[dict], best_app: str) -> None:
    st.subheader("Price Comparison")
    cols = st.columns(len(rankings), gap="medium")
    for col, ranking in zip(cols, rankings):
        render_platform_card(col, ranking, best_app)


def render_rankings(rankings: list[dict]) -> None:
    st.subheader("Platform Ranking")
    for idx, ranking in enumerate(rankings, start=1):
        st.write(f"{idx}. {ranking['app']} - {optimizer.format_currency(ranking['total_cost'])}")


def render_placeholders() -> None:
    left, right = st.columns(2, gap="medium")
    with left:
        st.subheader("History")
        st.caption("Placeholder for recent comparisons and saved price checks.")
    with right:
        st.subheader("Insights")
        st.caption("Placeholder for trends, multi-item carts, and recommendation summaries.")


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, page_icon="🍔", layout="wide")
    render_css()
    render_header()

    try:
        dataset = load_dataset()
    except FileNotFoundError:
        st.error("The JSON dataset file could not be found.")
        return
    except Exception as exc:
        st.error(f"Unable to load dataset: {exc}")
        return

    restaurant_names = get_restaurant_names(dataset)
    if not restaurant_names:
        st.warning("No restaurants were found in the JSON dataset.")
        return

    controls_col, best_col = st.columns([1.2, 0.9], gap="large")

    with controls_col:
        st.subheader("Build Your Comparison")
        selected_restaurant = st.selectbox("Restaurant", options=restaurant_names)
        restaurant = get_restaurant(dataset, selected_restaurant)
        item_names = get_item_names(restaurant)

        if not item_names:
            st.warning("No items are available for the selected restaurant.")
            return

        selected_item = st.selectbox("Item", options=item_names)

        today_name = datetime.now().strftime("%A")
        default_day = DAY_ORDER.index(today_name) if today_name in DAY_ORDER else 0
        st.subheader("Starship Timing")
        day_of_week = st.selectbox("Day of week", options=DAY_ORDER, index=default_day)
        hour = st.slider(
            "Preferred order hour",
            min_value=9,
            max_value=22,
            value=18,
            help="This changes the Starship timing recommendation based on the hourly fee pattern.",
        )
        st.caption(f"Currently evaluating Starship timing for {day_of_week} at {hour:02d}:00.")

    try:
        rankings = optimizer.rank_apps(dataset, selected_restaurant, selected_item)
        best = optimizer.cheapest_option(dataset, selected_restaurant, selected_item)
        timing_result = recommend_order_time(
            day_of_week=day_of_week,
            hour=hour,
            minute=0,
            restaurant="Starship Aggregate",
        )
    except ValueError as exc:
        st.error(str(exc))
        return
    except FileNotFoundError as exc:
        st.error(str(exc))
        return
    except Exception as exc:
        st.error(f"Unable to compute comparison: {exc}")
        return

    if not rankings:
        st.warning("No platform pricing data is available for that selection.")
        return

    with best_col:
        render_best_option(best, rankings)
        st.write("")
        render_timing_recommendation(timing_result, day_of_week, hour)

    st.write("")
    summary_left, summary_right = st.columns(2, gap="large")
    with summary_left:
        render_combined_summary(best, rankings, timing_result)
    with summary_right:
        st.subheader("What Changes With Time")
        st.write(
            "The platform comparison stays the same for the selected item, but the Starship section changes as you move the hour slider."
        )
        st.caption(
            "If timing savings are low, ordering now is fine. If timing savings increase, waiting may lower the delivery fee signal."
        )

    st.write("")
    render_platform_comparison(rankings, best["app"])

    st.write("")
    render_rankings(rankings)

    st.write("")
    render_placeholders()


if __name__ == "__main__":
    main()
