-- Total revenue by year
SELECT Year, SUM(Sales) AS total_revenue
FROM financials
GROUP BY Year
ORDER BY Year;

-- Total profit by product
SELECT Product, SUM(Profit) AS total_profit
FROM financials
GROUP BY Product
ORDER BY total_profit DESC;

-- Top 5 countries by revenue
SELECT Country, SUM(Sales) AS revenue
FROM financials
GROUP BY Country
ORDER BY revenue DESC
LIMIT 5;

-- Monthly sales trend for 2014
SELECT Month_Name, SUM(Sales) AS monthly_sales
FROM financials
WHERE Year = 2014
GROUP BY Month_Name, Month_Number
ORDER BY Month_Number;
