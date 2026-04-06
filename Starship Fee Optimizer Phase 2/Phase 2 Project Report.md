# Phase 2 - MVP Progress Report & Technical Demonstration
## Starship Delivery Fee Optimization

**Group Members:** Muhssen Ahmed, Matthew Dankwerth, Isaac Mejia, and Joseph Moyer

---

## 1. Restated MVP

Our MVP is a prototype that helps students in Tempe decide the cheapest time to place a Starship food delivery order. The system is intended to take the current day and time as input and return a recommendation such as:

- "Now is a good time to order."
- "Wait until time X for a better price."

The purpose of the MVP is to reduce delivery costs for students by identifying pricing patterns and recommending lower-cost ordering windows.

---

## 2. Problem Overview

During long study hours, many college students and others in Tempe become hungry but may not have access to a kitchen or enough time to leave campus and get food. Starship delivery robots offer a convenient solution, but delivery prices fluctuate throughout the day. These fluctuations are difficult to track manually, especially for busy students.

For students on limited budgets, even a small delivery fee difference can matter over time. Our project aims to make these pricing changes easier to understand and use for decision-making.

---

## 3. Progress Made So Far

At this stage, our team has completed the Phase 1 proposal and narrowed the project into a more concrete MVP. We have identified the target user, the core problem, the intended output, and the main risks.

### Current completed progress
- Completed the Phase 1 written proposal
- Submitted the video pitch
- Defined the main user problem
- Defined the MVP output
- Identified possible data sources
- Identified major risks and open questions
- Considered a nanoGPT-based technical direction

### Evidence of progress
The current project work includes:
- project concept definition
- MVP scoping
- technical idea selection
- identification of data and feasibility concerns

At this point, the strongest progress is in project design and technical planning rather than full implementation.

---

## 4. What Already Works

The following parts of the project are currently clear and functioning at the planning level:

- The user problem has been clearly identified.
- The target user is clearly defined as students and other users in Tempe who rely on Starship delivery.
- The MVP has been narrowed to a simple recommendation task.
- The expected user interaction is defined:
  - input: current day and time
  - output: recommendation to order now or wait
- The team has identified likely data collection paths:
  - public repositories such as Kaggle
  - Starship-related pricing observations
  - possible synthetic data for early testing

---

## 5. What Does Not Yet Work

The following components are not yet complete:

- No confirmed real-world pricing dataset has been collected yet
- No trained model has been implemented yet
- No benchmark results are available yet
- No working prototype interface has been demonstrated yet
- No comparison has yet been made between a GPT-style approach and simpler prediction methods

This means the main Phase 2 bottleneck is still implementation and data collection.

---

## 6. Main Technical Risks / Open Bottlenecks

Our project currently faces several important technical risks.

### 1. Data availability
The biggest challenge is obtaining enough Starship delivery fee data to train and evaluate a model. Public datasets may not exist, and pricing may need to be logged manually.

### 2. Unknown pricing factors
Starship may change delivery fees using variables we cannot observe directly, such as:
- demand
- weather
- restaurant volume
- delivery distance
- time of day
- campus events
- promotions

This may make prediction difficult.

### 3. Model choice
Our original idea was to use a nanoGPT-based model, but the project may be better suited to a simpler prediction model such as regression, classification, or time-based averaging. One open question is whether a GPT-style approach is actually the best fit.

### 4. Feasibility within course timeline
Because the course timeline is short, our team must keep the scope realistic. A recommendation system based on historical fee patterns may be more feasible than a fully advanced AI product.

---

## 7. AI Baseline Analysis

One Phase 2 requirement for agent / AI projects is to identify what a strong general-purpose AI system still cannot do well for the target task.

A general-purpose AI model such as ChatGPT can explain possible reasons why delivery prices change, but it cannot accurately predict Starship delivery fee fluctuations for Tempe without task-specific local data. This means that generic AI knowledge alone is not enough for our project.

Our project therefore requires:
- task-specific fee observations
- structured time-based inputs
- a prediction or recommendation pipeline based on actual price patterns

This is where our project adds value beyond a general chatbot.

---

## 8. Planned Technical Approach

Our original technical concept was a nanoGPT-style language model trained on pricing data. After reflecting on the problem more carefully, we now see that the project may be better framed as a prediction/recommendation task.

Our updated technical plan is to compare the following:

### Baseline approach
A simple historical average model that estimates likely fees based on:
- day of week
- time of day

### Possible ML approach
A supervised model that predicts whether:
- current fee is low
- waiting may lead to a lower fee
- prices are likely to increase or decrease in the next time window

### User-facing recommendation layer
Regardless of the model type, the final output to the user will remain simple:
- order now
- wait until a better time

This keeps the MVP practical and aligned with the course requirements.

---

## 9. Development Process and Iteration

One of the biggest lessons so far is that our original project idea was more ambitious than our current data and timeline allow. In Phase 1, we proposed a nanoGPT-style model, but in Phase 2 we recognized that success depends more on reliable data collection and measurable prediction than on language generation alone.

This design adjustment is an important part of our progress. It shows that the team is refining the project based on feasibility, not just sticking to the original idea without evaluation.

---

## 10. Failure Cases and Current Limitations

At the current stage, our main failure cases are not model prediction errors yet, but project-level limitations:

- lack of real delivery fee data
- unclear pricing logic from Starship
- uncertain usefulness of a GPT-style model for this task
- limited ability to validate results without a larger dataset

These limitations are important because they shape what can realistically be achieved by Phase 3.

---

## 11. Deliverables in `/phase2/`

Our `/phase2/` folder is intended to contain:

- `README.md`
  Explanation of current progress, setup, and next steps

- `data/`
  Collected or sample pricing observations

- `notebooks/`
  Exploratory analysis and model testing

- `src/`
  Code for prediction and recommendation logic

- `artifacts/`
  Screenshots, logs, outputs, and benchmark visuals

At the current moment, the project is still in the setup and planning stage, and additional implementation work is needed before these sections are fully populated.

---

## 12. What Will Be Completed Before Phase 3

Before the final MVP phase, our team plans to complete the following:

1. collect or construct a usable pricing dataset
2. clean and organize the data
3. implement a baseline prediction method
4. test at least one ML-based approach
5. compare results between methods
6. generate a recommendation output for users
7. document what works and what still fails

---

## 13. Conclusion

Our Phase 2 progress shows that the project idea is still promising, but the most important challenge is turning the idea into a working data-driven system. So far, our team has made meaningful progress in defining the problem, clarifying the MVP, and identifying the technical risks and bottlenecks.

The main insight from this phase is that the success of the project depends less on building a complex GPT-style model and more on obtaining useful pricing data and selecting a practical prediction method. For Phase 3, our goal is to transform this planning work into a functioning prototype that can recommend cheaper ordering times for students using Starship delivery.

---

## 14. Phase 1 Video Link

[Starship Delivery Optimization Video Pitch](https://youtu.be/KP9nV6aq5xk?si=D3TgKda-ChAOl87Y)
