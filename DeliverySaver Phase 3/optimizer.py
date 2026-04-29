from src.optimizer import cheapest_app_per_item, cheapest_option, format_currency, load_optimizer_dataset, rank_apps


def print_restaurant_report(dataset: dict, restaurant_name: str) -> None:
    overall_best = cheapest_option(dataset, restaurant_name)
    overall_rankings = rank_apps(dataset, restaurant_name)
    item_winners = cheapest_app_per_item(dataset, restaurant_name)

    print(f"Restaurant: {restaurant_name}")
    print(
        f"Best overall app: {overall_best['app']} "
        f"({format_currency(overall_best['total_cost'])} across the sampled menu)"
    )
    print("App ranking:")
    for index, ranking in enumerate(overall_rankings, start=1):
        print(f"  {index}. {ranking['app']} - {format_currency(ranking['total_cost'])}")

    print("Cheapest app by item:")
    for winner in item_winners:
        print(
            f"  - {winner['item']}: {winner['app']} "
            f"at {format_currency(winner['total_cost'])}"
        )
    print()


def main() -> None:
    dataset = load_optimizer_dataset()

    print("Delivery App Optimizer")
    print("This report finds the cheapest app for each restaurant and each item.")
    print()

    for restaurant in dataset["restaurants"]:
        print_restaurant_report(dataset, restaurant["name"])


if __name__ == "__main__":
    main()
