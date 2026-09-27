"""
ZYROO Data Analytics Internship - Week 5
Advanced Business Intelligence & Decision Analytics
-----------------------------------------------------
Validation script: reproduces every KPI, DAX-equivalent measure, and
segment table used in the Week 5 report and Power BI dashboard.

Run:  python week5_advanced_analysis.py
Input: data/cleaned_rides.csv (Ride ID, Date, Pickup Location,
       Drop-off Location, Fare, Payment Method, Ride Status, Rating)

This script is the source of truth used to validate the DAX measures
before they were written into Power BI. Every number here should match
the "KPI Summary" / "Weekday Analysis" / "Location Analysis" / etc.
tabs of ZYROO_Week5_Advanced_Analytics.xlsx exactly.
"""

import pandas as pd

DATA_PATH = "data/cleaned_rides.csv"   # adjust path if run from elsewhere


def load_data(path=DATA_PATH):
    df = pd.read_csv(path, parse_dates=["Date"])
    df["Weekday"] = df["Date"].dt.day_name()
    df["Week"] = df["Date"].dt.isocalendar().week
    df["Route"] = df["Pickup Location"] + " -> " + df["Drop-off Location"]
    return df


def data_quality_report(df):
    print("=== DATA QUALITY REVIEW ===")
    print(f"Total rows: {len(df)}")
    print(f"Duplicate Ride IDs: {df['Ride ID'].duplicated().sum()}")
    print(f"Missing keys (any column): {df[['Ride ID','Date','Pickup Location','Drop-off Location']].isnull().sum().sum()}")
    print(f"Negative/zero fares: {(df['Fare'] <= 0).sum()}")
    print(f"Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")
    print(f"Ride Status values: {df['Ride Status'].unique().tolist()}")
    print(f"Missing ratings: {df['Rating'].isnull().sum()} "
          f"(should equal cancelled-ride count: {(df['Ride Status']=='Cancelled').sum()})")
    print()


def kpi_summary(df):
    completed = df[df["Ride Status"] == "Completed"]
    cancelled = df[df["Ride Status"] == "Cancelled"]

    total_rides = len(df)
    completed_rides = len(completed)
    cancelled_rides = len(cancelled)
    total_revenue = completed["Fare"].sum()

    kpis = {
        "Total Rides": total_rides,
        "Completed Rides": completed_rides,
        "Cancelled Rides": cancelled_rides,
        "Completion Rate": completed_rides / total_rides,
        "Cancellation Rate": cancelled_rides / total_rides,
        "Total Revenue": total_revenue,
        "Average Fare (Completed)": completed["Fare"].mean(),
        "Average Rating": completed["Rating"].mean(),
        "Revenue per Completed Ride": total_revenue / completed_rides,
    }
    print("=== CORE KPI SUMMARY ===")
    for k, v in kpis.items():
        print(f"{k:32s}: {v:,.2f}" if isinstance(v, float) else f"{k:32s}: {v}")
    print()
    return kpis


def weekday_analysis(df):
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    g = df.groupby("Weekday").agg(
        total=("Ride ID", "count"),
        cancelled=("Ride Status", lambda x: (x == "Cancelled").sum()),
        revenue=("Fare", lambda x: x[df.loc[x.index, "Ride Status"] == "Completed"].sum()),
    ).reindex(order)
    g["cancel_rate"] = g["cancelled"] / g["total"]
    print("=== WEEKDAY ANALYSIS ===")
    print(g)
    print()
    return g


def weekly_trend(df):
    total_revenue = df.loc[df["Ride Status"] == "Completed", "Fare"].sum()
    g = df.groupby("Week").agg(
        total=("Ride ID", "count"),
        completed=("Ride Status", lambda x: (x == "Completed").sum()),
        cancelled=("Ride Status", lambda x: (x == "Cancelled").sum()),
        revenue=("Fare", lambda x: x[df.loc[x.index, "Ride Status"] == "Completed"].sum()),
    )
    g["cancel_rate"] = g["cancelled"] / g["total"]
    g["revenue_change"] = g["revenue"].diff()
    g["revenue_pct_change"] = g["revenue"].pct_change()
    print("=== WEEK-OVER-WEEK TREND ===")
    print(g)
    print(f"(Total revenue check: {total_revenue:,})")
    print()
    return g


def location_analysis(df):
    total_revenue = df.loc[df["Ride Status"] == "Completed", "Fare"].sum()
    g = df.groupby("Pickup Location").agg(
        total=("Ride ID", "count"),
        completed=("Ride Status", lambda x: (x == "Completed").sum()),
        cancelled=("Ride Status", lambda x: (x == "Cancelled").sum()),
        revenue=("Fare", lambda x: x[df.loc[x.index, "Ride Status"] == "Completed"].sum()),
    )
    g["cancel_rate"] = g["cancelled"] / g["total"]
    g["pct_of_revenue"] = g["revenue"] / total_revenue
    g["avg_fare"] = g["revenue"] / g["completed"]
    g["revenue_rank"] = g["revenue"].rank(ascending=False).astype(int)
    g = g.sort_values("revenue", ascending=False)
    print("=== LOCATION ANALYSIS (PICKUP) ===")
    print(g)
    print()
    return g


def payment_method_analysis(df):
    total_revenue = df.loc[df["Ride Status"] == "Completed", "Fare"].sum()
    g = df.groupby("Payment Method").agg(
        total=("Ride ID", "count"),
        completed=("Ride Status", lambda x: (x == "Completed").sum()),
        cancelled=("Ride Status", lambda x: (x == "Cancelled").sum()),
        revenue=("Fare", lambda x: x[df.loc[x.index, "Ride Status"] == "Completed"].sum()),
    )
    g["cancel_rate"] = g["cancelled"] / g["total"]
    g["pct_of_revenue"] = g["revenue"] / total_revenue
    g["avg_fare"] = g["revenue"] / g["completed"]
    g = g.sort_values("revenue", ascending=False)
    print("=== PAYMENT METHOD ANALYSIS ===")
    print(g)
    print()
    return g


def route_analysis(df, min_rides=3):
    g = df.groupby("Route").agg(
        total=("Ride ID", "count"),
        completed=("Ride Status", lambda x: (x == "Completed").sum()),
        cancelled=("Ride Status", lambda x: (x == "Cancelled").sum()),
        revenue=("Fare", lambda x: x[df.loc[x.index, "Ride Status"] == "Completed"].sum()),
    )
    g = g[g["total"] >= min_rides]
    g["cancel_rate"] = g["cancelled"] / g["total"]
    g["avg_fare"] = g["revenue"] / g["completed"]
    g = g.sort_values("revenue", ascending=False)
    print(f"=== ROUTE ANALYSIS (routes with {min_rides}+ rides) ===")
    print(g)
    print()
    return g


def fare_segment_analysis(df):
    completed = df[df["Ride Status"] == "Completed"].copy()
    total_revenue = completed["Fare"].sum()
    completed["Fare Tier"] = pd.qcut(completed["Fare"], 3, labels=["Low", "Mid", "High"])
    g = completed.groupby("Fare Tier", observed=True).agg(
        rides=("Ride ID", "count"),
        revenue=("Fare", "sum"),
        avg_fare=("Fare", "mean"),
    )
    g["pct_of_rides"] = g["rides"] / len(completed)
    g["pct_of_revenue"] = g["revenue"] / total_revenue
    print("=== FARE-TIER SEGMENTATION (proxy for customer segmentation) ===")
    print("NOTE: no Customer ID exists in this dataset, so this segments")
    print("      RIDES by fare, not customers by frequency. See README limitations.")
    print(g)
    print()
    return g


def scenario_analysis(df, target_cancel_rate=0.15, fare_increase_pct=0.05):
    completed = df[df["Ride Status"] == "Completed"]
    total_rides = len(df)
    cancelled_rides = (df["Ride Status"] == "Cancelled").sum()
    current_cancel_rate = cancelled_rides / total_rides
    avg_fare = completed["Fare"].mean()
    total_revenue = completed["Fare"].sum()

    additional_completed = round(total_rides * (current_cancel_rate - target_cancel_rate))
    extra_revenue_from_cancellations = additional_completed * avg_fare
    fare_increase_revenue = total_revenue * fare_increase_pct
    combined_uplift = extra_revenue_from_cancellations + fare_increase_revenue

    print("=== SCENARIO / WHAT-IF ANALYSIS (estimates only) ===")
    print(f"Current cancellation rate: {current_cancel_rate:.1%}")
    print(f"Target cancellation rate:  {target_cancel_rate:.1%}")
    print(f"Additional completed rides: {additional_completed}")
    print(f"Extra revenue from fewer cancellations: {extra_revenue_from_cancellations:,.2f}")
    print(f"Revenue impact of {fare_increase_pct:.0%} fare increase: {fare_increase_revenue:,.2f}")
    print(f"Combined estimated uplift: {combined_uplift:,.2f} "
          f"({combined_uplift/total_revenue:.1%} of current revenue)")
    print("Assumptions: demand pattern and fare mix stay constant; saved cancellations")
    print("convert to completed rides at the current average fare; no cost data exists,")
    print("so this is a revenue estimate, not a profit estimate.")
    print()


def main():
    df = load_data()
    data_quality_report(df)
    kpi_summary(df)
    weekday_analysis(df)
    weekly_trend(df)
    location_analysis(df)
    payment_method_analysis(df)
    route_analysis(df)
    fare_segment_analysis(df)
    scenario_analysis(df)

    print("=== LIMITATIONS (cannot be computed from this dataset) ===")
    print("- Driver performance intelligence: no Driver ID column exists.")
    print("- True customer segmentation (ride frequency, repeat riders): no Customer ID column exists.")
    print("- Average Distance / ride-type breakdowns: no distance or ride-type column exists.")
    print("- Hourly peak-period analysis: only a Date is logged, not a timestamp.")


if __name__ == "__main__":
    main()
