import json
from pathlib import Path


DATASET_PATH = Path(__file__).resolve().parent.parent / "delivery_optimizer_dataset.json"


def load_optimizer_dataset(dataset_path: Path = DATASET_PATH) -> dict:
    with dataset_path.open("r", encoding="utf-8") as dataset_file:
        return json.load(dataset_file)


def calculate_total_cost(price_breakdown: dict[str, float]) -> float:
    return round(float(sum(price_breakdown.values())), 2)


def format_currency(value: float) -> str:
    return f"${value:.2f}"


def _get_restaurant(dataset: dict, restaurant_name: str) -> dict:
    for restaurant in dataset["restaurants"]:
        if restaurant["name"].lower() == restaurant_name.lower():
            return restaurant
    raise ValueError(f"Restaurant '{restaurant_name}' was not found in the dataset.")


def _get_item(restaurant: dict, item_name: str) -> dict:
    for item in restaurant["items"]:
        if item["name"].lower() == item_name.lower():
            return item
    raise ValueError(f"Item '{item_name}' was not found for restaurant '{restaurant['name']}'.")


def rank_apps(dataset: dict, restaurant_name: str, item_name: str | None = None) -> list[dict]:
    restaurant = _get_restaurant(dataset, restaurant_name)

    if item_name is not None:
        item = _get_item(restaurant, item_name)
        rankings = []
        for app_name, price_breakdown in item["prices"].items():
            rankings.append(
                {
                    "app": app_name,
                    "restaurant": restaurant["name"],
                    "item": item["name"],
                    "total_cost": calculate_total_cost(price_breakdown),
                    "breakdown": price_breakdown,
                }
            )
        return sorted(rankings, key=lambda entry: entry["total_cost"])

    app_totals: dict[str, dict] = {}
    for item in restaurant["items"]:
        for app_name, price_breakdown in item["prices"].items():
            item_total = calculate_total_cost(price_breakdown)
            if app_name not in app_totals:
                app_totals[app_name] = {
                    "app": app_name,
                    "restaurant": restaurant["name"],
                    "items_compared": [],
                    "total_cost": 0.0,
                }
            app_totals[app_name]["items_compared"].append(
                {"item": item["name"], "total_cost": item_total}
            )
            app_totals[app_name]["total_cost"] += item_total

    rankings = list(app_totals.values())
    for ranking in rankings:
        ranking["total_cost"] = round(float(ranking["total_cost"]), 2)
    return sorted(rankings, key=lambda entry: entry["total_cost"])


def cheapest_option(dataset: dict, restaurant_name: str, item_name: str | None = None) -> dict:
    rankings = rank_apps(dataset, restaurant_name, item_name)
    return rankings[0]


def cheapest_app_per_item(dataset: dict, restaurant_name: str) -> list[dict]:
    restaurant = _get_restaurant(dataset, restaurant_name)
    cheapest_items = []

    for item in restaurant["items"]:
        best_option = cheapest_option(dataset, restaurant["name"], item["name"])
        cheapest_items.append(best_option)

    return cheapest_items
