import Combine
import Foundation

struct PlatformTotal: Identifiable, Hashable {
    let platform: Platform
    let breakdown: PriceBreakdown?

    var id: String { platform.id }
    var total: Double? { breakdown?.total }
    var isAvailable: Bool { breakdown != nil }
}

struct BestOption: Hashable {
    let cheapest: PlatformTotal
    let highest: PlatformTotal

    var savings: Double {
        guard let cheapestTotal = cheapest.total, let highestTotal = highest.total else {
            return 0
        }
        return max(0, ((highestTotal - cheapestTotal) * 100).rounded() / 100)
    }
}

@MainActor
final class DeliveryComparisonViewModel: ObservableObject {
    @Published private(set) var restaurants: [Restaurant] = []
    @Published private(set) var errorMessage: String?

    @Published var selectedRestaurantID: String? {
        didSet {
            guard selectedRestaurantID != oldValue else { return }
            alignSelectedItemWithRestaurant()
        }
    }

    @Published var selectedItemID: String?

    let platforms = Platform.allCases

    init(loadImmediately: Bool = true) {
        if loadImmediately {
            loadData()
        }
    }

    var hasData: Bool {
        !restaurants.isEmpty
    }

    var selectedRestaurant: Restaurant? {
        guard let selectedRestaurantID else {
            return restaurants.first
        }
        return restaurants.first { $0.id == selectedRestaurantID } ?? restaurants.first
    }

    var selectedItem: MenuItem? {
        guard let restaurant = selectedRestaurant else {
            return nil
        }

        guard let selectedItemID else {
            return restaurant.items.first
        }

        return restaurant.items.first { $0.id == selectedItemID } ?? restaurant.items.first
    }

    var platformTotals: [PlatformTotal] {
        guard let item = selectedItem else {
            return platforms.map { PlatformTotal(platform: $0, breakdown: nil) }
        }

        return platforms.map { platform in
            PlatformTotal(platform: platform, breakdown: item.prices[platform.rawValue])
        }
    }

    var bestOption: BestOption? {
        let availableTotals = platformTotals.filter { $0.total != nil }
        guard
            let cheapest = availableTotals.min(by: { ($0.total ?? .greatestFiniteMagnitude) < ($1.total ?? .greatestFiniteMagnitude) }),
            let highest = availableTotals.max(by: { ($0.total ?? 0) < ($1.total ?? 0) })
        else {
            return nil
        }

        return BestOption(cheapest: cheapest, highest: highest)
    }

    func loadData() {
        do {
            guard let url = Bundle.main.url(forResource: "delivery_data", withExtension: "json") else {
                throw DataLoadingError.missingBundleResource
            }

            let data = try Data(contentsOf: url)
            let dataset = try JSONDecoder().decode(DeliveryDataset.self, from: data)

            restaurants = dataset.restaurants
            errorMessage = nil
            selectedRestaurantID = restaurants.first?.id
            alignSelectedItemWithRestaurant()
        } catch {
            restaurants = []
            selectedRestaurantID = nil
            selectedItemID = nil
            errorMessage = error.localizedDescription
        }
    }

    func selectRestaurant(_ restaurant: Restaurant) {
        selectedRestaurantID = restaurant.id
    }

    func selectItem(_ item: MenuItem) {
        selectedItemID = item.id
    }

    func lowestTotal(for item: MenuItem) -> Double? {
        platforms
            .compactMap { item.prices[$0.rawValue]?.total }
            .min()
    }

    private func alignSelectedItemWithRestaurant() {
        guard let restaurant = selectedRestaurant else {
            selectedItemID = nil
            return
        }

        if let selectedItemID, restaurant.items.contains(where: { $0.id == selectedItemID }) {
            return
        }

        selectedItemID = restaurant.items.first?.id
    }
}

private enum DataLoadingError: LocalizedError {
    case missingBundleResource

    var errorDescription: String? {
        switch self {
        case .missingBundleResource:
            return "delivery_data.json was not found in the app bundle."
        }
    }
}
