# DeliverySaver Phase 3

This repository contains the DeliverySaver Phase 3 MVP for comparing delivery apps, surfacing the cheapest option, and exploring timing-based delivery fee savings.

## MVP Scope

- `pandas` for loading and inspecting delivery fee data
- `scikit-learn` for a simple machine learning model
- a historical-average baseline for comparison
- `Streamlit` for a lightweight demo app
- a recommendation layer that returns:
  - order now
  - wait until a lower-fee time

## Project Structure

- `data/` delivery fee observations, including PDF-derived hourly pricing
- `src/` training, baseline, and recommendation logic
- `artifacts/` generated model files and evaluation output
- `train_model.py` root entry point for model training
- `recommend.py` root entry point for quick recommendation testing
- `app.py` root entry point for the Streamlit demo

## Setup

1. Install Python 3.10+.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Train the MVP model:

```bash
python train_model.py
```

4. Launch the Streamlit app:

```bash
streamlit run app.py
```

## Run The UI

From the project folder, start the Streamlit interface with:

```bash
python -m streamlit run app.py
```



## Current Approach

- Baseline model: historical average delivery fee by restaurant, day, and hour
- ML model: random forest regressor using day, hour, minute, and restaurant
- Recommendation engine: compares the current predicted fee with the next few future time slots and suggests waiting only when a lower predicted fee is found
- Delivery optimizer: compares app-level fee breakdowns from the JSON dataset to find the cheapest app per item and per restaurant

## Delivery Optimizer

The repository now also includes a JSON-based optimizer for comparing Uber Eats, DoorDash, and Grubhub prices.

- `optimizer.py` is a simple terminal entry point
- `src/optimizer.py` provides reusable functions for:
  - total cost calculation
  - cheapest option lookup
  - app ranking by item
  - app ranking by restaurant

Example run:

```bash
python optimizer.py
```

## Notes

- The default dataset currently comes from manually entered hourly prices extracted from the project PDF.
- The original synthetic sample dataset is still available for fallback testing in `data/sample_delivery_fees.csv`.
- Real Starship pricing data would improve the usefulness of the recommendations.


