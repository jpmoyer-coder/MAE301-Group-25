# Starship Delivery Fee Optimization

**Group Members:** Muhssen Ahmed, Matthew Dankwerth, Isaac Mejia, and Joseph Moyer

## Problem Statement

During long study hours, many college students and others in Tempe become hungry but lack convenient access to a kitchen or the time to travel to a restaurant. To address this problem, Starship Technologies has developed autonomous food delivery bots that deliver food to users. However, delivery prices fluctuate by several dollars throughout the day, and tracking the factors that drive these price changes is difficult for busy students.

For many students, even a small price difference can have a meaningful impact on a monthly budget, which is often already constrained.

## Proposed AI-Powered Solution

To address this problem for students in Tempe, we propose designing an AI-powered language model trained to predict fluctuations in Starship delivery prices throughout the day. The goal is to help students maximize savings by identifying the nearest time frame for the best possible pricing.

## Initial Technical Concept

The initial technical concept is a nano-GPT model based on Andrej Karpathy’s work. It will be trained on delivery pricing data to identify patterns in price fluctuations and generate useful recommendations for users.

## Scope for Minimum Viable Product (MVP)

Over the course of six weeks, our goal is to develop a functioning prototype that can reliably recommend the cheapest time to order with Starship. A user will be able to input the current time and day and receive a response such as:

- “Now is a good time to order.”
- “Wait until time X for a better price.”

## Risks and Open Questions

Current questions surrounding the project include:

- Where to source the pricing data
- What factors Starship uses to adjust delivery prices
- How practical a GPT-based solution will be for end users

Without knowledge of all relevant pricing factors, anomalies may appear that the model cannot fully account for.

## Planned Data Sources

We plan to search repositories such as Kaggle and investigate whether Starship provides any relevant data on its website. We may also generate synthetic data after learning more about the algorithm governing delivery prices.
