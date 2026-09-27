## Week 5 — Advanced Business Intelligence & Decision Analytics

Upgrades the Week 4 dashboard into an advanced analytical and decision-support layer. Full write-up: [`reports/week-05-advanced-bi/ZYROO_Week5_Advanced_Analytics_Report.docx`](reports/week-05-advanced-bi/ZYROO_Week5_Advanced_Analytics_Report.docx). Companion workbook with every formula-driven table: [`reports/week-05-advanced-bi/ZYROO_Week5_Advanced_Analytics.xlsx`](reports/week-05-advanced-bi/ZYROO_Week5_Advanced_Analytics.xlsx).

### Data model
One fact table (`rides`, 120 rows, Aug 2026) joined to a dedicated Date Table on `Date`. Three calculated columns support the analysis: `Weekday`, `Route` (Pickup → Drop-off), and `Fare Tier` (Low/Mid/High, split at the 33rd/67th percentile of completed fares). Source data, calculated columns, and measures are kept in separate tables/tabs.

### Major measures (DAX)
`Total Revenue`, `Completed Rides`, `Cancelled Rides`, `Completion Rate`, `Cancellation Rate`, `Average Fare`, `Average Rating`, `Revenue per Completed Ride`, week-over-week revenue change/% change, and location revenue rank/contribution-%. Full DAX library in the workbook's `DAX Measures` tab and in [`python/week5_advanced_analysis.py`](python/week5_advanced_analysis.py) / [`sql/week5_advanced_queries.sql`](sql/week5_advanced_queries.sql), used to validate every measure before it went into Power BI.

### Advanced Power BI features
Drill-through by pickup location, cancellation-rate conditional formatting (red >25%, amber 15–25%, green <15%), a dynamic page title, and revenue/cancellation-view bookmarks on a new "Advanced Analytics" page.

### Key insights
- Cancellation runs at 20.0% overall; **Saturday cancels at 39.1%**, roughly double the weekly average.
- **Johar Town** is the top revenue location (17.3% of revenue) but also runs an above-average 19.0% cancellation rate.
- **Card payments** are both the largest revenue channel (40.4%) and the most reliable (15.6% cancellation); Wallet is the opposite (26.7% of revenue, 24.2% cancellation).
- The top fare tier (33% of completed rides) generates **49.9% of total revenue**.
- Full list of 10 evidence-based insights and 8 recommendations (5 dataset-supported, 3 needing more data) in the report, Sections 13–14.

### Limitations
- No `Driver ID` → driver performance intelligence cannot be built.
- No `Customer ID` → true ride-frequency customer segmentation cannot be built (a fare-tier proxy is used instead, see report Section 7).
- No distance or ride-type column → `Average Distance` and ride-type breakdowns are not available.
- Date only, no timestamp → cancellation/demand analyzed by weekday, not by hour.
- Single calendar month → trend is week-over-week, not month-over-month.
- No cost data → all figures are revenue, not profit/margin.

Full detail: report Section 15.

### Recommendations
1. Prioritize Saturday operations — it accounts for 9 of the month's 24 cancellations.
2. Protect Johar Town specifically — highest revenue share and above-average cancellation.
3. Use Gulberg (lowest cancellation, 6.7%) as an internal operational benchmark.
4. Investigate the Wallet payment flow — highest cancellation rate of the three methods.
5. Track the "High" fare tier separately in reporting — half of revenue from a third of rides.
6. *(Needs more data)* Driver-level actions — requires adding a `Driver ID` field first.
7. *(Needs more data)* Customer retention programs — requires adding a `Customer ID` field first.
8. *(Needs validation)* The ~11.3% estimated revenue uplift in the scenario analysis should be piloted before committing budget.
