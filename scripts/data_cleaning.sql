-- 1. Remove rows missing an order date
DELETE FROM orders
 WHERE "Order Date" IS NULL;

-- 2. Standardize Segment values
UPDATE orders
   SET "Segment" = 'Consumer'
 WHERE "Segment" ILIKE 'consumer%';

UPDATE orders
   SET "Segment" = 'Corporate'
 WHERE "Segment" ILIKE 'corporate%';

UPDATE orders
   SET "Segment" = 'Home Office'
 WHERE "Segment" ILIKE 'home office%';

-- 3. Standardize Category (if needed)
UPDATE orders
   SET "Category" = INITCAP("Category");

-- 4. Drop exact duplicates (keeping the first)
DELETE FROM orders a
USING (
  SELECT MIN(ctid) as keep_ctid, "Order ID"
  FROM orders
  GROUP BY "Order ID"
  HAVING COUNT(*) > 1
) dup
WHERE a."Order ID" = dup."Order ID"
AND a.ctid <> dup.keep_ctid;

-- 5. (Optional) Flag negative profits for manual review
UPDATE orders
   SET "Profit" = NULL
 WHERE "Profit" < 0;