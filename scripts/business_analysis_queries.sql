-- Are certian product categories are more profitable in specific regions?
SELECT 
    "Region",
    "Category",
    ROUND(SUM("Profit")::NUMERIC, 2) AS total_profit
FROM orders
GROUP BY "Region", "Category"
ORDER BY "Region", total_profit DESC;


-- 2 Which customers frequently buy from more than one category?
SELECT 
    "Customer Name",
    COUNT(DISTINCT "Category") AS category_count,
    COUNT("Order ID") AS total_orders
FROM orders
GROUP BY "Customer Name"
HAVING COUNT(DISTINCT "Category") > 1
ORDER BY category_count DESC, total_orders DESC;

-- 3 Is there a difference of average profit for first time customers and repeated customes?
SELECT 
    CASE 
        WHEN COUNT("Order ID") = 1 THEN 'First-time'
        ELSE 'Repeat'
    END AS customer_type,
    ROUND(AVG("Profit")::NUMERIC, 2) AS avg_profit
FROM orders
GROUP BY "Customer ID";

-- 4 Cities with high discount rates but low profit?
SELECT 
    "City",
    ROUND(AVG("Discount")::NUMERIC, 2) AS avg_discount,
    ROUND(SUM("Profit")::NUMERIC, 2) AS total_profit
FROM orders
GROUP BY "City"
HAVING AVG("Discount") > 0.2 AND SUM("Profit") < 100
ORDER BY avg_discount DESC;

-- 5 Do average profit per order affected by different shipping modes?
SELECT 
    "Ship Mode",
    ROUND(AVG("Profit")::NUMERIC, 2) AS avg_profit,
    ROUND(AVG("Sales")::NUMERIC, 2) AS avg_sales
FROM orders
GROUP BY "Ship Mode"
ORDER BY avg_profit DESC;
