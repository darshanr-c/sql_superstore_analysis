import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:<password>@localhost:5432/superstore_db")

# --- 1 Profit by Region vs. categories ---
query1 = """
SELECT 
    "Region",
    "Category",
    ROUND(SUM("Profit")::NUMERIC, 2) AS total_profit
FROM orders
GROUP BY "Region", "Category"
ORDER BY "Region", total_profit DESC;
"""
df1 = pd.read_sql(query1, engine)
df1.to_csv("visuals/profit_by_region_and_category.csv", index=False)

# --- 2 customers by category ---
query2 = """
SELECT 
    "Customer Name",
    COUNT(DISTINCT "Category") AS category_count,
    COUNT("Order ID") AS total_orders
FROM orders
GROUP BY "Customer Name"
HAVING COUNT(DISTINCT "Category") > 1
ORDER BY category_count DESC, total_orders DESC;
"""
df2 = pd.read_sql(query2, engine)
df2.to_csv("visuals/customers_by_category.csv", index=False)

# --- 3 profits by new vs repeated customers ---
query3 = """
SELECT 
    CASE 
        WHEN COUNT("Order ID") = 1 THEN 'First-time'
        ELSE 'Repeat'
    END AS customer_type,
    ROUND(AVG("Profit")::NUMERIC, 2) AS avg_profit
FROM orders
GROUP BY "Customer ID";
"""
df3 = pd.read_sql(query3, engine)
df3.to_csv("visuals/profits_new_vs_old_customers.csv", index=False)

# --- 4 city by discounts vs profits ---
query4 = """
SELECT 
    "City",
    ROUND(AVG("Discount")::NUMERIC, 2) AS avg_discount,
    ROUND(SUM("Profit")::NUMERIC, 2) AS total_profit
FROM orders
GROUP BY "City"
HAVING AVG("Discount") > 0.2 AND SUM("Profit") < 100
ORDER BY avg_discount DESC;
"""
df4 = pd.read_sql(query4, engine)
df4.to_csv("visuals/city_discount_vs_profit.csv", index=False)

# --- 5 shipping mode vs profits ---
query5 = """
SELECT 
    "Ship Mode",
    ROUND(AVG("Profit")::NUMERIC, 2) AS avg_profit,
    ROUND(AVG("Sales")::NUMERIC, 2) AS avg_sales
FROM orders
GROUP BY "Ship Mode"
ORDER BY avg_profit DESC;
"""
df5 = pd.read_sql(query5, engine)
df5.to_csv("visuals/ship_mode_vs_profits.csv", index=False)

print("✅ All query results exported to /visuals/")
