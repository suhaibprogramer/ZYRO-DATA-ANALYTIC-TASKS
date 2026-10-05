# Ride Analytics & Revenue Intelligence Platform
**ZYROO Data Analytics Internship — Final Project**
**Author:** Muhammad Suhaib

## Overview

An end-to-end Business Intelligence project analyzing a ride-hailing operation: from raw trip data to a validated, interactive Power BI dashboard, advanced segment and cancellation-driver analysis, scenario modeling, and business recommendations.

## Project Progress

| Week | Focus |
|---|---|
| Week 2 | Ride demand analysis (date, weekday, location) and customer behavior |
| Week 3 | Revenue analysis and driver performance KPIs |
| Week 4 | Interactive Power BI dashboard (KPIs, charts, filters) |
| Week 5 | Advanced DAX, segmentation, and scenario analysis |
| Week 6 (Final) | Full audit, validation, and presentation-ready final product |

## Dataset

`cleaned_rides.csv` — 120 rides, August 1–30, 2026. Columns: Ride ID, Date, Pickup Location, Drop-off Location, Fare, Payment Method, Ride Status, Rating.

> Note: this dataset does not include Driver ID, Customer ID, Ride Type, hourly timestamp, or Distance — see **Limitations** in the Week 6 report for what that means for scope.

## Key Metrics

| KPI | Value |
|---|---|
| Total Rides | 120 |
| Completed Rides | 96 |
| Cancelled Rides | 24 |
| Total Revenue | Rs 65,427 |
| Average Fare | Rs 681.53 |
| Completion Rate | 80% |
| Cancellation Rate | 20% |
| Average Rating | 3.96 / 5 |

## Dashboard Features

- **Executive KPI row:** Total Rides, Completed, Cancelled, Total Revenue, Average Fare, Completion Rate
- **Demand page:** Rides by date (trend), rides by weekday, top pickup/drop-off locations
- **Revenue page:** Revenue by payment method, revenue by pickup location
- **Operations page:** Cancellation rate by weekday and by location (the project's key finding)
- **Filters:** Date, Ride Status, Pickup Location, Payment Method

## Headline Finding

Cancellations track demand rather than occurring at random: the cancellation rate rises from 0% on the quietest day (Thursday) to 39.1% on the busiest day (Saturday), pointing to a weekend driver-supply shortfall rather than a general reliability issue.

## Business Insights

1. Weekends (Sat+Sun) drive 38% of all ride volume
2. Cancellation rate scales directly with demand — 0% (Thursday) to 39.1% (Saturday)
3. Cancellation rates vary sharply by zone: Gulberg 6.7% vs. Lahore 30.0%
4. Three pickup zones (Johar Town, Model Town, Wapda Town) generate 48% of total revenue
5. Card leads in total revenue through ride volume, not higher per-ride fares
6. Halving the cancellation rate is estimated to recover ~Rs 8,178/month
7. Wallet-paid rides rate slightly lower (3.88) than Cash-paid rides (4.00)

## Recommendations

1. Increase weekend driver availability
2. Treat weekend cancellations as the top operational priority
3. Audit driver supply/service quality in Lahore and Model Town
4. Study and replicate Gulberg's low-cancellation performance
5. Protect driver supply in the top 3 revenue-generating zones
6. Pilot a ~10% weekend peak-pricing surcharge, tested carefully
7. Investigate the rating gap on Wallet-paid rides
8. Add Driver ID and Customer ID to future data collection

*(Full detail, scenario analysis, and evidence for each recommendation is in the Week 5 and Week 6 reports.)*

## Tech Stack

- Power BI Desktop (dashboard, DAX measures)
- Python (pandas) — independent KPI validation and advanced analysis
- GitHub — version control and submission

## How to Reproduce

1. Clone this repository
2. Install dependencies: `pip install pandas`
3. Open the Power BI dashboard file in Power BI Desktop
4. Run the validation script to reproduce the independent KPI check

## Project Status

**Complete.** This project (Weeks 2–6) is finished and submitted. The internship continues with a new project for the remaining weeks.
