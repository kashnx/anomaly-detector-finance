-- Detect months where sales dropped more than 40% compared to previous month
WITH monthly_sales AS (
    SELECT
        Year,
        Month_Number,
        Month_Name,
        SUM(Sales) AS total_sales
    FROM financials
    GROUP BY Year, Month_Number, Month_Name
),
sales_with_lag AS (
    SELECT *,
           LAG(total_sales) OVER (PARTITION BY Year ORDER BY Month_Number) AS prev_month_sales
    FROM monthly_sales
)
SELECT *
FROM sales_with_lag
WHERE prev_month_sales IS NOT NULL
  AND total_sales < prev_month_sales * 0.6
ORDER BY Year, Month_Number;

-- Detect unusually low profit months (e.g., below 10th percentile)
WITH profit_stats AS (
    SELECT
        Year,
        Month_Name,
        SUM(Profit) AS monthly_profit
    FROM financials
    GROUP BY Year, Month_Name
),
threshold AS (
    SELECT PERCENTILE_CONT(0.10) WITHIN GROUP (ORDER BY monthly_profit) AS low_profit_threshold
    FROM profit_stats
)
SELECT p.*
FROM profit_stats p, threshold t
WHERE p.monthly_profit < t.low_profit_threshold;
