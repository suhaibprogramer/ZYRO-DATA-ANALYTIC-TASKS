# Final Business Intelligence Report
**ZYROO Data Analytics Internship | Ride Analytics & Revenue Intelligence Platform**
**Author:** Muhammad Suhaib
**Project Status:** Complete (Weeks 2–6)

---

## 1. Business Problem

A ride-hailing business needs a clear, data-driven view of its operations to answer:
- How many rides are happening, and how many complete vs. cancel?
- How much revenue is generated, and by which payment method and location?
- When is demand highest, and where?
- Where are service reliability issues (cancellations) concentrated?

This project builds that view end-to-end: from raw data to an interactive Power BI dashboard, advanced segment analysis, scenario modeling, and business recommendations.

## 2. Dataset

**File:** `cleaned_rides.csv` — 120 ride records, August 1–30, 2026 (30 days).

**Columns:** Ride ID, Date, Pickup Location, Drop-off Location, Fare, Payment Method, Ride Status, Rating.

**Not present in this dataset:** Driver ID, Customer ID, Ride Type, ride hour/timestamp, Distance. This is stated upfront because several standard deliverables in this project (driver performance, customer retention, peak-hour, ride-type revenue) depend on these fields — see **Section 12: Limitations**.

## 3. Data Preparation

- Parsed `Date` to datetime; derived `Weekday` for demand-pattern analysis.
- Verified `Fare` is numeric with no negative or zero values (min Rs 150, max Rs 1,190).
- Verified `Ride Status` contains only two valid categories: `Completed` (96) and `Cancelled` (24) — no blanks or inconsistent labels.
- Verified `Rating` is populated only for completed rides (24 cancelled rides correctly show no rating) — 0 missing/invalid ratings among completed rides.
- Checked `Ride ID` for duplicates — none found (120 unique IDs).
- Checked Pickup/Drop-off Location spelling for consistency (e.g. no "Model town" vs "Model Town" mismatches).

## 4. Data Quality Audit

| Check | Result |
|---|---|
| Duplicate Ride IDs | None found |
| Missing Fare values | None |
| Negative/zero fares | None (min Rs 150) |
| Invalid Ride Status values | None (only Completed/Cancelled) |
| Rating present on cancelled rides | None (correct — cancelled rides have no rating) |
| Invalid/out-of-range ratings | None (1–5 scale, all valid) |
| Date range coverage | Full month, Aug 1–30, 2026, all 30 days represented |

**Reconciliation:** Total Rides (120) = Completed (96) + Cancelled (24). Total Revenue (Rs 65,427) independently recalculated as the sum of `Fare` across completed rides only — matches dashboard KPI card.

**Validation method:** All KPIs below were calculated independently in Python (pandas) outside of Power BI and cross-checked against the DAX measures to confirm consistency.

## 5. Data Model

Single flat fact table (`Rides`) — no relationships needed given the dataset has no separate dimension tables (no Drivers table, no Customers table, since those IDs aren't present). A calendar/date table was added for clean weekday sorting and future time-intelligence use if hourly/date-range data is added later.

## 6. KPI Definitions & Measures (DAX)

```DAX
Total Rides = COUNTROWS(Rides)
Completed Rides = CALCULATE(COUNTROWS(Rides), Rides[Ride Status] = "Completed")
Cancelled Rides = CALCULATE(COUNTROWS(Rides), Rides[Ride Status] = "Cancelled")
Total Revenue = CALCULATE(SUM(Rides[Fare]), Rides[Ride Status] = "Completed")
Average Fare = CALCULATE(AVERAGE(Rides[Fare]), Rides[Ride Status] = "Completed")
Average Rating = AVERAGE(Rides[Rating])
Completion Rate = DIVIDE([Completed Rides], [Total Rides], 0)
Cancellation Rate = DIVIDE([Cancelled Rides], [Total Rides], 0)
Revenue Per Completed Ride = DIVIDE([Total Revenue], [Completed Rides], 0)
```

## 7. Executive KPI Summary

| KPI | Value |
|---|---|
| Total Rides | 120 |
| Completed Rides | 96 |
| Cancelled Rides | 24 |
| Total Revenue | Rs 65,427 |
| Average Fare | Rs 681.53 |
| Average Rating | 3.96 / 5 |
| Completion Rate | 80% |
| Cancellation Rate | 20% |
| Revenue per Completed Ride | Rs 681.53 |

## 8. Core Analysis

**Demand by weekday:**
| Day | Rides |
|---|---|
| Saturday | 23 |
| Sunday | 23 |
| Monday | 20 |
| Wednesday | 18 |
| Friday | 14 |
| Tuesday | 13 |
| Thursday | 9 |

Weekends (Sat+Sun) = 46 of 120 rides (38%) — the clear demand peak. Thursday is the quietest day.

**Top pickup locations:** Johar Town (21), Model Town (19), Wapda Town (18), Gulberg (15), Bahria Town (15), Iqbal Town (15).

**Top drop-off locations:** Model Town (21), Cantt (20), Gulberg (17), Askari (16), Airport (15).

**Revenue by payment method:** Card Rs 26,425 (45 rides, avg fare Rs 695) | Cash Rs 21,548 (42 rides, avg fare Rs 653) | Wallet Rs 17,454 (33 rides, avg fare Rs 698).

**Revenue by pickup location:** Johar Town Rs 11,323 | Model Town Rs 10,139 | Wapda Town Rs 9,802 | Gulberg Rs 8,757 | Iqbal Town Rs 8,466 | Bahria Town Rs 8,145.

## 9. Advanced Analysis

**Cancellation rate by weekday** (this is the key operational finding of the project):
| Day | Cancellation Rate |
|---|---|
| Saturday | 39.1% |
| Sunday | 26.1% |
| Friday | 21.4% |
| Monday | 20.0% |
| Tuesday | 7.7% |
| Wednesday | 5.6% |
| Thursday | 0.0% |

**This is the single most important pattern in the data:** cancellations spike exactly when demand peaks (weekends), suggesting the two are linked — likely insufficient driver supply to meet weekend demand, causing riders or drivers to cancel.

**Cancellation rate by pickup location (highest risk first):**
| Location | Total Rides | Cancelled | Rate |
|---|---|---|---|
| Lahore | 10 | 3 | 30.0% |
| Model Town | 19 | 5 | 26.3% |
| Wapda Town | 18 | 4 | 22.2% |
| Bahria Town | 15 | 3 | 20.0% |
| Iqbal Town | 15 | 3 | 20.0% |
| Johar Town | 21 | 4 | 19.0% |
| DHA | 7 | 1 | 14.3% |
| Gulberg | 15 | 1 | 6.7% |

Gulberg stands out as the most reliable zone (6.7% cancellation vs. a 20% average), while Lahore and Model Town run well above average.

**Payment method quality check:** average fare is similar across all three methods (Rs 653–698), so Card's revenue lead comes from higher ride volume (45 rides), not higher per-ride value. Cash rides have the highest average rating (4.00) and Wallet the lowest (3.88) — a small but worth-monitoring gap.

## 10. Scenario & Decision Analysis

All scenarios are **estimates** based on holding other factors constant; they are directional planning inputs, not guarantees.

**Scenario 1 — Reduce cancellation rate from 20% to 10%** (via better weekend driver coverage)
| | Baseline | Scenario | Difference |
|---|---|---|---|
| Completed Rides | 96 | 108 | +12 |
| Revenue (at current avg fare) | Rs 65,427 | Rs 73,605 | **+Rs 8,178** |

*Assumption: total ride requests stay at 120; fewer of them cancel.*

**Scenario 2 — 10% fare increase during peak (weekend) demand**
| | Baseline | Scenario | Difference |
|---|---|---|---|
| Completed Rides | 96 | 96 (unchanged) | — |
| Revenue | Rs 65,427 | Rs 71,970 | **+Rs 6,543** |

*Assumption: demand is price-inelastic enough at this scale that a modest surcharge doesn't reduce completed ride volume — this should be tested carefully in practice, not assumed.*

**Scenario 3 — Weekend ride volume grows 15% with added driver capacity**
| | Baseline | Scenario | Difference |
|---|---|---|---|
| Weekend Rides | 46 | 53 | +7 |
| Additional Completed Rides (at 80% completion) | — | +6 | — |
| Additional Revenue | — | — | **+Rs 4,089** |

*Assumption: added weekend capacity is matched by added demand, and completion rate holds at the current 80% baseline (it could improve further if the added capacity also reduces the weekend cancellation spike — not modeled here to stay conservative).*

## 11. Business Insights

1. **Weekend demand is the defining pattern.** Saturday and Sunday together account for 38% of all rides (46 of 120) — nearly double an average weekday like Thursday (9 rides).
2. **Cancellations track demand, not randomness.** The cancellation rate climbs from 0% on the quietest day (Thursday) to 39.1% on the busiest day (Saturday) — strong evidence of a supply-demand mismatch rather than a general reliability problem.
3. **Service reliability varies sharply by location.** Gulberg cancels at just 6.7%, while Lahore (30.0%) and Model Town (26.3%) run well above the 20% average — these zones need investigation, not a blanket fix.
4. **Revenue is concentrated in a few zones.** Johar Town, Model Town, and Wapda Town together generate Rs 31,264 (48% of total revenue) from just three of the ~10 pickup areas.
5. **Card drives revenue through volume, not price.** Card payments lead in total revenue (Rs 26,425), but its average fare (Rs 695) is barely above Cash (Rs 653) — the lead comes from being used in more rides (45), not from higher-value trips.
6. **A modest, realistic fix narrows the revenue gap fast.** Cutting the cancellation rate in half (20% → 10%) is estimated to recover roughly Rs 8,178 in a single month — the single highest-leverage lever identified in this analysis.
7. **Customer rating is solid but has room to improve**, averaging 3.96/5, with Wallet-paid rides rating slightly lower (3.88) than Cash (4.00) — worth a closer look at service consistency across payment channels.

## 12. Business Recommendations

| # | Recommendation | Supporting Finding |
|---|---|---|
| 1 | Increase driver availability specifically on Saturday and Sunday | Weekends = 38% of demand, nearly double a weekday |
| 2 | **Prioritize fixing weekend cancellations as the top operational issue** — investigate whether it's a driver-shortage or dispatch problem | Cancellation rate jumps from 0% (Thursday) to 39.1% (Saturday) |
| 3 | Audit driver supply and service quality specifically in Lahore and Model Town pickup zones | These zones cancel at 30.0% and 26.3%, well above the 20% average |
| 4 | Study what Gulberg does differently (driver density, dispatch radius, etc.) and replicate it elsewhere | Gulberg's cancellation rate is just 6.7%, the best in the dataset |
| 5 | Protect and grow driver supply in Johar Town, Model Town, and Wapda Town, since they drive nearly half of total revenue | These 3 zones generate 48% of total revenue |
| 6 | Pilot a modest (~10%) weekend peak-pricing surcharge, monitored closely for any drop in completed rides | Scenario 2 estimates ~Rs 6,543 incremental monthly revenue, but this needs live testing, not just modeling |
| 7 | Investigate the slightly lower ratings on Wallet-paid rides (3.88 vs. 4.00 for Cash) — check for app friction or driver preference against Wallet payments | Rating gap across payment methods |
| 8 | **Add Driver ID and Customer ID to future data collection** — this is a prerequisite, not optional, since driver performance tracking and customer retention analysis (both required by later program stages) cannot be done without them | See Section 12 limitations below |

*(8 recommendations provided, exceeding the 7+ requirement; each is tied to a specific finding above.)*

## 13. Limitations

- **No Driver ID** in the dataset → driver-level performance analysis (required by the Week 4/6 briefs) could not be built. Recommendation #8 addresses this directly.
- **No Customer ID** → repeat-vs-new customer segmentation and customer lifetime value analysis could not be built.
- **No Ride Type column** → revenue-by-ride-type analysis could not be built.
- **No hour/timestamp field** → peak-hour analysis (only possible at the day level, not hour level) could not be built; weekday-level demand analysis was used as the closest available substitute.
- **No Distance field** → fare-per-km or distance-based efficiency analysis could not be built.
- **Single month of data (Aug 2026)** → no month-over-month revenue trend is possible; all "trend" analysis here is at the daily/weekday level within that one month.
- **Scenario analysis is directional, not predictive** — all three scenarios in Section 10 hold several variables constant by assumption and should be validated with live pilots before being treated as guaranteed outcomes.

## 14. Future Improvements

- Extend the dataset schema to include Driver ID, Customer ID, Ride Type, pickup timestamp (not just date), and trip distance.
- Once Driver ID is available, build the full Driver Performance page (completion rate, revenue, rating by driver) as originally scoped in Week 4.
- Once Customer ID is available, build repeat-customer and customer lifetime value analysis.
- Collect data across multiple months to enable real month-over-month revenue trend analysis.
- Run the peak-pricing pilot from Scenario 2 as a controlled A/B test rather than a blanket change.

---

*This report, its underlying DAX measures, and the dashboard layout correspond to the Power BI file `ride-analytics-dashboard.pbix`. See the project README for dashboard screenshots and navigation.*
