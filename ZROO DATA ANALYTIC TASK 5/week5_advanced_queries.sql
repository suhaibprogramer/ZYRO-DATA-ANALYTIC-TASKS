-- ============================================================
-- ZYROO Data Analytics Internship - Week 5
-- Advanced Business Intelligence & Decision Analytics
-- SQL validation queries (equivalent to week5_advanced_analysis.py
-- and the DAX measures used in Power BI)
--
-- Target table: rides (
--   ride_id TEXT, ride_date DATE, pickup_location TEXT,
--   dropoff_location TEXT, fare NUMERIC, payment_method TEXT,
--   ride_status TEXT, rating NUMERIC
-- )
-- Adjust table/column names to match your database load of
-- data/cleaned_rides.csv.
-- ============================================================

-- 1. Data quality checks -------------------------------------
SELECT COUNT(*) AS total_rows FROM rides;

SELECT ride_id, COUNT(*) AS occurrences
FROM rides
GROUP BY ride_id
HAVING COUNT(*) > 1;                      -- expect 0 rows (no duplicate IDs)

SELECT COUNT(*) AS negative_or_zero_fares
FROM rides
WHERE fare <= 0;                          -- expect 0

SELECT DISTINCT ride_status FROM rides;   -- expect only 'Completed', 'Cancelled'

SELECT
    SUM(CASE WHEN rating IS NULL THEN 1 ELSE 0 END)      AS missing_ratings,
    SUM(CASE WHEN ride_status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_rides
FROM rides;                               -- these two should match

-- 2. Core KPI summary -----------------------------------------
SELECT
    COUNT(*)                                                        AS total_rides,
    SUM(CASE WHEN ride_status = 'Completed' THEN 1 ELSE 0 END)      AS completed_rides,
    SUM(CASE WHEN ride_status = 'Cancelled' THEN 1 ELSE 0 END)      AS cancelled_rides,
    ROUND(1.0 * SUM(CASE WHEN ride_status = 'Completed' THEN 1 ELSE 0 END) / COUNT(*), 4) AS completion_rate,
    ROUND(1.0 * SUM(CASE WHEN ride_status = 'Cancelled' THEN 1 ELSE 0 END) / COUNT(*), 4) AS cancellation_rate,
    SUM(CASE WHEN ride_status = 'Completed' THEN fare ELSE 0 END)   AS total_revenue,
    ROUND(AVG(CASE WHEN ride_status = 'Completed' THEN fare END), 2) AS avg_fare,
    ROUND(AVG(rating), 2)                                            AS avg_rating
FROM rides;

-- 3. Weekday analysis (finest time grain available - no timestamp) ---
SELECT
    TO_CHAR(ride_date, 'Day')                                        AS weekday,
    COUNT(*)                                                         AS total_rides,
    SUM(CASE WHEN ride_status = 'Cancelled' THEN 1 ELSE 0 END)       AS cancelled,
    ROUND(1.0 * SUM(CASE WHEN ride_status = 'Cancelled' THEN 1 ELSE 0 END) / COUNT(*), 4) AS cancel_rate,
    SUM(CASE WHEN ride_status = 'Completed' THEN fare ELSE 0 END)    AS revenue
FROM rides
GROUP BY TO_CHAR(ride_date, 'Day'), EXTRACT(ISODOW FROM ride_date)
ORDER BY EXTRACT(ISODOW FROM ride_date);

-- 4. Week-over-week trend --------------------------------------
SELECT
    EXTRACT(WEEK FROM ride_date)                                     AS week_no,
    COUNT(*)                                                         AS total_rides,
    SUM(CASE WHEN ride_status = 'Completed' THEN 1 ELSE 0 END)       AS completed,
    SUM(CASE WHEN ride_status = 'Cancelled' THEN 1 ELSE 0 END)       AS cancelled,
    SUM(CASE WHEN ride_status = 'Completed' THEN fare ELSE 0 END)    AS revenue
FROM rides
GROUP BY EXTRACT(WEEK FROM ride_date)
ORDER BY week_no;
-- compute week-over-week change/percent-change in your BI tool or
-- with a LAG() window function, e.g.:
--   revenue - LAG(revenue) OVER (ORDER BY week_no) AS revenue_change

-- 5. Revenue & cancellation by pickup location -------------------
SELECT
    pickup_location,
    COUNT(*)                                                         AS total_rides,
    SUM(CASE WHEN ride_status = 'Completed' THEN 1 ELSE 0 END)       AS completed,
    SUM(CASE WHEN ride_status = 'Cancelled' THEN 1 ELSE 0 END)       AS cancelled,
    ROUND(1.0 * SUM(CASE WHEN ride_status = 'Cancelled' THEN 1 ELSE 0 END) / COUNT(*), 4) AS cancel_rate,
    SUM(CASE WHEN ride_status = 'Completed' THEN fare ELSE 0 END)    AS revenue,
    ROUND(
        1.0 * SUM(CASE WHEN ride_status = 'Completed' THEN fare ELSE 0 END)
        / SUM(SUM(CASE WHEN ride_status = 'Completed' THEN fare ELSE 0 END)) OVER (), 4
    )                                                                 AS pct_of_total_revenue,
    RANK() OVER (
        ORDER BY SUM(CASE WHEN ride_status = 'Completed' THEN fare ELSE 0 END) DESC
    )                                                                 AS revenue_rank
FROM rides
GROUP BY pickup_location
ORDER BY revenue DESC;

-- 6. Revenue & cancellation by payment method ---------------------
SELECT
    payment_method,
    COUNT(*)                                                         AS total_rides,
    SUM(CASE WHEN ride_status = 'Cancelled' THEN 1 ELSE 0 END)       AS cancelled,
    ROUND(1.0 * SUM(CASE WHEN ride_status = 'Cancelled' THEN 1 ELSE 0 END) / COUNT(*), 4) AS cancel_rate,
    SUM(CASE WHEN ride_status = 'Completed' THEN fare ELSE 0 END)    AS revenue
FROM rides
GROUP BY payment_method
ORDER BY revenue DESC;

-- 7. Route-level analysis (proxy for ride-type segmentation) ------
SELECT
    pickup_location || ' -> ' || dropoff_location                    AS route,
    COUNT(*)                                                         AS total_rides,
    SUM(CASE WHEN ride_status = 'Cancelled' THEN 1 ELSE 0 END)       AS cancelled,
    ROUND(1.0 * SUM(CASE WHEN ride_status = 'Cancelled' THEN 1 ELSE 0 END) / COUNT(*), 4) AS cancel_rate,
    SUM(CASE WHEN ride_status = 'Completed' THEN fare ELSE 0 END)    AS revenue
FROM rides
GROUP BY pickup_location, dropoff_location
HAVING COUNT(*) >= 3
ORDER BY revenue DESC;

-- 8. Fare-tier segmentation (proxy for customer segmentation) -----
-- NOTE: no customer_id exists in this dataset, so this segments
--       RIDES by fare, not customers by frequency.
WITH thresholds AS (
    SELECT
        PERCENTILE_CONT(0.3333) WITHIN GROUP (ORDER BY fare) AS low_cut,
        PERCENTILE_CONT(0.6667) WITHIN GROUP (ORDER BY fare) AS high_cut
    FROM rides WHERE ride_status = 'Completed'
)
SELECT
    CASE
        WHEN fare < t.low_cut THEN 'Low'
        WHEN fare <= t.high_cut THEN 'Mid'
        ELSE 'High'
    END                                                               AS fare_tier,
    COUNT(*)                                                          AS rides,
    SUM(fare)                                                         AS revenue,
    ROUND(AVG(fare), 2)                                               AS avg_fare
FROM rides, thresholds t
WHERE ride_status = 'Completed'
GROUP BY 1;

-- ============================================================
-- Not computable from this dataset (documented, not worked around):
--   - Driver performance intelligence -> requires a driver_id column
--   - Customer segmentation by ride frequency -> requires a customer_id column
--   - Average distance / ride-type breakdowns -> requires those columns
--   - Hourly peak-period analysis -> requires a timestamp, not just a date
-- ============================================================
