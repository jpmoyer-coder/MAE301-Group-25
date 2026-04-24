# DeliverySaver Phase 3 - MVP Report

## 1. Executive Summary

Many users overpay when ordering food because delivery platforms often show different total costs for the same item. The final price can vary due to differences in food markup, delivery fees, service fees, taxes, and tipping assumptions. Without a direct comparison, users may choose a platform that is more expensive than necessary.

This MVP addresses that problem with a comparison and optimization tool. It loads structured pricing data, calculates the full order total for each platform, ranks the options, and highlights the cheapest choice for the user.

The MVP currently performs single-item comparison across platforms. A user selects one restaurant and one item, and the system shows the total cost on Uber Eats, DoorDash, and Grubhub, identifies the cheapest option, and reports the savings compared with the next best alternative.

## 2. User & Use Case

### Persona

A cost-conscious food delivery user who regularly orders meals online and wants to avoid overpaying across delivery apps.

### Usage Scenario

A student wants to order a burrito bowl from Chipotle. Instead of checking multiple apps manually, they open the optimizer, choose `Chipotle`, select `Burrito Bowl`, and instantly see the total price on each platform. The app identifies the cheapest platform and shows how much money the student saves by choosing it.

## 3. System Design

The MVP uses a simple three-part architecture:

- a structured JSON dataset that stores restaurant, item, and platform fee data
- `optimizer.py`, which performs deterministic cost calculations and comparisons
- a Streamlit UI in `app.py`, which provides the interactive user experience

Computation happens in the Python optimizer layer. The UI does not perform pricing logic itself; it imports and reuses the existing optimizer functions to load data, calculate totals, rank platforms, and determine the cheapest option.

```text
+-----------------------------+
| delivery_optimizer_dataset  |
| .json                       |
+-------------+---------------+
              |
              v
+-----------------------------+
| optimizer.py                |
| - load JSON                 |
| - calculate totals          |
| - rank platforms            |
| - find cheapest option      |
+-------------+---------------+
              |
              v
+-----------------------------+
| app.py (Streamlit UI)       |
| - restaurant selector       |
| - item selector             |
| - comparison display        |
| - best option summary       |
+-----------------------------+
```

## 4. Data

The dataset is a structured JSON file containing restaurants, items, and platform-specific pricing breakdowns.

Each item stores pricing for multiple platforms using these fields:

- `food`
- `delivery`
- `service`
- `tax`
- `tip`

These values are summed to compute the final total cost shown to the user.

Current limitations of the data:

- it is static rather than real-time
- it is synthetic or manually curated rather than pulled from live services
- it only represents a small sample of restaurants and menu items

To scale this system, the same structure could be populated from real delivery APIs, scraping pipelines, or scheduled backend data collection jobs. That would allow the optimizer to compare live prices instead of fixed sample values.

## 5. Models

This MVP does not use machine learning models.

Instead, it uses a deterministic optimization engine. The system calculates exact totals from known fee components and then compares those totals directly to determine the cheapest platform.

Machine learning could be added later for advanced features such as:

- price prediction across time
- personalized platform recommendations
- expected savings forecasting
- delivery fee trend analysis

## 6. Evaluation

### Quantitative

The main quantitative evaluation is correctness of total-cost calculation and platform comparison. For each item:

- the total for each platform should equal the sum of `food + delivery + service + tax + tip`
- the reported cheapest platform should match the minimum of those totals
- the savings value should correctly reflect the difference between the cheapest and next cheapest option

### Qualitative

The main qualitative evaluation criteria are:

- usability of the interface
- clarity of the pricing breakdown
- usefulness of the recommendation

### Example Output Interpretation

If the system shows:

- DoorDash: `$20.31`
- Uber Eats: `$22.59`
- Grubhub: `$22.73`

then the correct interpretation is:

- DoorDash is the cheapest option
- the user should choose DoorDash for that item
- the user saves `$2.28` versus the next cheapest option

## 7. Limitations & Risks

- Static data means the system does not reflect live market prices.
- The MVP does not personalize recommendations for individual users.
- Delivery pricing can vary over time due to promotions, surge pricing, or location differences.
- There is no API integration, so the tool depends on manually prepared data.
- Dataset assumptions may bias results toward certain platforms if the sample prices are not representative.

## 8. Next Steps

- Add real API integrations for live pricing data
- Extend the optimizer to support multi-item cart optimization
- Add user profiles and personalization
- Add historical tracking and pricing insights
- Deploy as a mobile app or hosted web application

