import Foundation
import SwiftUI

struct ContentView: View {
    @StateObject private var viewModel = DeliveryComparisonViewModel()

    var body: some View {
        TabView {
            CompareView(viewModel: viewModel)
                .tabItem {
                    Label("Compare", systemImage: "chart.bar.fill")
                }

            PlaceholderTabView(
                title: "History",
                systemImage: "clock.arrow.circlepath",
                message: "Saved comparisons will appear here."
            )
            .tabItem {
                Label("History", systemImage: "clock.arrow.circlepath")
            }

            PlaceholderTabView(
                title: "Insights",
                systemImage: "lightbulb",
                message: "Ordering patterns and savings trends will appear here."
            )
            .tabItem {
                Label("Insights", systemImage: "lightbulb")
            }
        }
        .tint(.green)
    }
}

private struct CompareView: View {
    @ObservedObject var viewModel: DeliveryComparisonViewModel

    var body: some View {
        ZStack {
            Color(.systemGroupedBackground)
                .ignoresSafeArea()

            ScrollView {
                VStack(alignment: .leading, spacing: 20) {
                    HeaderView()

                    if let errorMessage = viewModel.errorMessage {
                        MessageCard(
                            title: "Data unavailable",
                            message: errorMessage,
                            systemImage: "exclamationmark.triangle.fill",
                            tint: .orange
                        )
                    }

                    if viewModel.hasData {
                        RestaurantSelectorView(viewModel: viewModel)
                        ItemSelectorView(viewModel: viewModel)
                        BestOptionSection(bestOption: viewModel.bestOption)
                        PlatformComparisonSection(
                            totals: viewModel.platformTotals,
                            cheapestPlatform: viewModel.bestOption?.cheapest.platform
                        )
                    } else if viewModel.errorMessage == nil {
                        MessageCard(
                            title: "No restaurants",
                            message: "Add restaurants to delivery_data.json to start comparing.",
                            systemImage: "tray",
                            tint: .secondary
                        )
                    }
                }
                .padding(.horizontal, 20)
                .padding(.top, 18)
                .padding(.bottom, 28)
            }
        }
    }
}

private struct HeaderView: View {
    var body: some View {
        HStack(alignment: .center, spacing: 14) {
            ZStack {
                RoundedRectangle(cornerRadius: 8, style: .continuous)
                    .fill(Color.green)

                Image(systemName: "bag.fill")
                    .font(.title2.weight(.semibold))
                    .foregroundColor(.white)
            }
            .frame(width: 54, height: 54)

            VStack(alignment: .leading, spacing: 4) {
                Text("DeliverySaver")
                    .font(.largeTitle.weight(.bold))
                    .foregroundColor(.primary)

                Text("Compare delivery totals before you order.")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }
        }
        .frame(maxWidth: .infinity, alignment: .leading)
    }
}

private struct RestaurantSelectorView: View {
    @ObservedObject var viewModel: DeliveryComparisonViewModel

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            SectionTitle("Restaurant")

            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 12) {
                    ForEach(viewModel.restaurants) { restaurant in
                        let isSelected = restaurant.id == viewModel.selectedRestaurant?.id

                        Button {
                            viewModel.selectRestaurant(restaurant)
                        } label: {
                            VStack(alignment: .leading, spacing: 8) {
                                Text(restaurant.name)
                                    .font(.headline)
                                    .foregroundColor(.primary)
                                    .lineLimit(2)

                                Text("\(restaurant.items.count) items")
                                    .font(.caption.weight(.medium))
                                    .foregroundColor(isSelected ? .green : .secondary)
                            }
                            .frame(width: 150, minHeight: 70, alignment: .leading)
                            .padding(14)
                            .background(
                                RoundedRectangle(cornerRadius: 8, style: .continuous)
                                    .fill(isSelected ? Color.green.opacity(0.14) : Color(.secondarySystemGroupedBackground))
                            )
                            .overlay(
                                RoundedRectangle(cornerRadius: 8, style: .continuous)
                                    .stroke(isSelected ? Color.green : Color(.separator), lineWidth: isSelected ? 1.5 : 0.5)
                            )
                        }
                        .buttonStyle(.plain)
                    }
                }
                .padding(.vertical, 2)
            }
        }
    }
}

private struct ItemSelectorView: View {
    @ObservedObject var viewModel: DeliveryComparisonViewModel

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            SectionTitle("Menu item")

            if let restaurant = viewModel.selectedRestaurant {
                LazyVStack(spacing: 10) {
                    ForEach(restaurant.items) { item in
                        let isSelected = item.id == viewModel.selectedItem?.id

                        Button {
                            viewModel.selectItem(item)
                        } label: {
                            HStack(spacing: 12) {
                                VStack(alignment: .leading, spacing: 5) {
                                    Text(item.name)
                                        .font(.headline)
                                        .foregroundColor(.primary)

                                    if let lowestTotal = viewModel.lowestTotal(for: item) {
                                        Text("From \(lowestTotal.currencyString)")
                                            .font(.subheadline)
                                            .foregroundColor(.secondary)
                                    }
                                }

                                Spacer()

                                Image(systemName: isSelected ? "checkmark.circle.fill" : "circle")
                                    .font(.title3)
                                    .foregroundColor(isSelected ? .green : .secondary)
                            }
                            .padding(14)
                            .background(
                                RoundedRectangle(cornerRadius: 8, style: .continuous)
                                    .fill(Color(.secondarySystemGroupedBackground))
                            )
                            .overlay(
                                RoundedRectangle(cornerRadius: 8, style: .continuous)
                                    .stroke(isSelected ? Color.green : Color.clear, lineWidth: 1.5)
                            )
                        }
                        .buttonStyle(.plain)
                    }
                }
            }
        }
    }
}

private struct BestOptionSection: View {
    let bestOption: BestOption?

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            SectionTitle("Best option")

            if let bestOption, let total = bestOption.cheapest.total {
                VStack(alignment: .leading, spacing: 14) {
                    HStack(alignment: .top) {
                        Label(bestOption.cheapest.platform.rawValue, systemImage: "sparkles")
                            .font(.title3.weight(.bold))
                            .foregroundColor(.green)

                        Spacer()

                        Text(total.currencyString)
                            .font(.title2.weight(.bold))
                            .monospacedDigit()
                    }

                    HStack(spacing: 12) {
                        MetricPill(title: "Savings", value: bestOption.savings.currencyString)
                        MetricPill(title: "Compared with", value: bestOption.highest.platform.rawValue)
                    }
                }
                .padding(16)
                .background(
                    RoundedRectangle(cornerRadius: 8, style: .continuous)
                        .fill(Color.green.opacity(0.15))
                )
                .overlay(
                    RoundedRectangle(cornerRadius: 8, style: .continuous)
                        .stroke(Color.green.opacity(0.65), lineWidth: 1)
                )
            } else {
                MessageCard(
                    title: "No platform prices",
                    message: "This item does not have comparable platform data.",
                    systemImage: "questionmark.circle",
                    tint: .secondary
                )
            }
        }
    }
}

private struct PlatformComparisonSection: View {
    let totals: [PlatformTotal]
    let cheapestPlatform: Platform?

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            SectionTitle("Platform comparison")

            LazyVStack(spacing: 12) {
                ForEach(totals) { total in
                    PlatformTotalCard(
                        total: total,
                        isCheapest: total.platform == cheapestPlatform
                    )
                }
            }
        }
    }
}

private struct PlatformTotalCard: View {
    let total: PlatformTotal
    let isCheapest: Bool

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack(alignment: .center) {
                Label(total.platform.rawValue, systemImage: total.platform.systemImage)
                    .font(.headline)
                    .foregroundColor(total.platform.tint)

                Spacer()

                if isCheapest {
                    Text("Cheapest")
                        .font(.caption.weight(.bold))
                        .padding(.horizontal, 10)
                        .padding(.vertical, 5)
                        .foregroundColor(.green)
                        .background(
                            Capsule()
                                .fill(Color.green.opacity(0.14))
                        )
                }
            }

            if let breakdown = total.breakdown, let totalValue = total.total {
                HStack(alignment: .firstTextBaseline) {
                    Text("Total")
                        .font(.subheadline.weight(.medium))
                        .foregroundColor(.secondary)

                    Spacer()

                    Text(totalValue.currencyString)
                        .font(.title3.weight(.bold))
                        .monospacedDigit()
                }

                Divider()

                VStack(spacing: 8) {
                    ForEach(breakdown.feeRows) { row in
                        FeeRow(title: row.title, amount: row.amount)
                    }
                }
            } else {
                Text("Price data unavailable")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    .frame(maxWidth: .infinity, alignment: .leading)
            }
        }
        .padding(16)
        .background(
            RoundedRectangle(cornerRadius: 8, style: .continuous)
                .fill(Color(.secondarySystemGroupedBackground))
        )
        .overlay(
            RoundedRectangle(cornerRadius: 8, style: .continuous)
                .stroke(isCheapest ? Color.green : Color.clear, lineWidth: 1.5)
        )
    }
}

private struct FeeRow: View {
    let title: String
    let amount: Double

    var body: some View {
        HStack {
            Text(title)
                .font(.subheadline)
                .foregroundColor(.secondary)

            Spacer()

            Text(amount.currencyString)
                .font(.subheadline.weight(.medium))
                .monospacedDigit()
                .foregroundColor(.primary)
        }
    }
}

private struct MetricPill: View {
    let title: String
    let value: String

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(title)
                .font(.caption.weight(.semibold))
                .foregroundColor(.secondary)

            Text(value)
                .font(.subheadline.weight(.bold))
                .foregroundColor(.primary)
                .lineLimit(1)
                .minimumScaleFactor(0.78)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(12)
        .background(
            RoundedRectangle(cornerRadius: 8, style: .continuous)
                .fill(Color(.systemBackground).opacity(0.72))
        )
    }
}

private struct SectionTitle: View {
    let title: String

    init(_ title: String) {
        self.title = title
    }

    var body: some View {
        Text(title)
            .font(.headline.weight(.bold))
            .foregroundColor(.primary)
    }
}

private struct MessageCard: View {
    let title: String
    let message: String
    let systemImage: String
    let tint: Color

    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            Image(systemName: systemImage)
                .font(.title3)
                .foregroundColor(tint)

            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(.headline)
                    .foregroundColor(.primary)

                Text(message)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }
        }
        .padding(16)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(
            RoundedRectangle(cornerRadius: 8, style: .continuous)
                .fill(Color(.secondarySystemGroupedBackground))
        )
    }
}

private struct PlaceholderTabView: View {
    let title: String
    let systemImage: String
    let message: String

    var body: some View {
        ZStack {
            Color(.systemGroupedBackground)
                .ignoresSafeArea()

            VStack(spacing: 14) {
                Image(systemName: systemImage)
                    .font(.system(size: 38, weight: .semibold))
                    .foregroundColor(.green)

                Text(title)
                    .font(.title2.weight(.bold))

                Text(message)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    .multilineTextAlignment(.center)
            }
            .padding(24)
        }
    }
}

private extension Platform {
    var systemImage: String {
        switch self {
        case .uberEats:
            return "bag.fill"
        case .doorDash:
            return "car.fill"
        case .grubhub:
            return "fork.knife"
        }
    }

    var tint: Color {
        switch self {
        case .uberEats:
            return Color(.label)
        case .doorDash:
            return .red
        case .grubhub:
            return .orange
        }
    }
}

private extension Double {
    var currencyString: String {
        formatted(.currency(code: "USD").precision(.fractionLength(2)))
    }
}
