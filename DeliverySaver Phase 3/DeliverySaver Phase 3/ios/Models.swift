import Foundation

struct DeliveryDataset: Codable {
    let restaurants: [Restaurant]
}

struct Restaurant: Codable, Identifiable, Hashable {
    let name: String
    let items: [MenuItem]

    var id: String { name }
}

struct MenuItem: Codable, Identifiable, Hashable {
    let name: String
    let prices: [String: PriceBreakdown]

    var id: String { name }
}

struct PriceBreakdown: Codable, Hashable {
    let food: Double?
    let delivery: Double?
    let service: Double?
    let tax: Double?
    let tip: Double?

    var total: Double {
        let subtotal = [food, delivery, service, tax, tip]
            .compactMap { $0 }
            .reduce(0, +)
        return (subtotal * 100).rounded() / 100
    }

    var feeRows: [(title: String, amount: Double)] {
        [
            ("Food", food ?? 0),
            ("Delivery", delivery ?? 0),
            ("Service", service ?? 0),
            ("Tax", tax ?? 0),
            ("Tip", tip ?? 0)
        ]
    }
}

enum Platform: String, CaseIterable, Codable, Identifiable, Hashable {
    case uberEats = "Uber Eats"
    case doorDash = "DoorDash"
    case grubhub = "Grubhub"

    var id: String { rawValue }
}
