# Data Cleaning Log

## Cleaning Steps

## Step 1: Remove rows with missing "Order Date"
DELETE FROM orders WHERE "Order Date" IS NULL;

Result: 0 rows deleted
Comment: The dataset contains no missing "Order Date" values — no action required.

## Step 2: Standardize "Segment" values

UPDATE orders SET "Segment" = 'Consumer' WHERE "Segment" ILIKE 'consumer%';
UPDATE orders SET "Segment" = 'Corporate' WHERE "Segment" ILIKE 'corporate%';
UPDATE orders SET "Segment" = 'Home Office' WHERE "Segment" ILIKE 'home office%';

Result:
    2586 rows updated to "Consumer"
    1514 rows updated to "Corporate"
    909 rows updated to "Home Office"
Comment: Segment values were inconsistent in case; now standardized across the dataset.

## Step 3: Format "Category" to Proper Case

UPDATE orders SET "Category" = INITCAP("Category");

Result: 5009 rows updated
Comment: Converted all category values to title case (e.g., “office supplies” → “Office Supplies”).

##  Step 4: Remove exact duplicates by "Order ID"

DELETE FROM orders a
USING (
  SELECT MIN(ctid) as keep_ctid, "Order ID"
  FROM orders
  GROUP BY "Order ID"
  HAVING COUNT(*) > 1
) dup
WHERE a."Order ID" = dup."Order ID"
AND a.ctid <> dup.keep_ctid;

Result: 0 rows deleted
Comment: No exact duplicate "Order ID" entries found — data appears clean.

## Step 5: Flag negative profits for review

UPDATE orders SET "Profit" = NULL WHERE "Profit" < 0;

Result: 0 rows updated
Comment: No negative profit values detected — data appears clean.