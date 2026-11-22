CREATE DATABASE  superstore_db;
USE superstore_db;

CREATE TABLE superstore_stg (
    row_id        VARCHAR(10),
    order_id      VARCHAR(30),
    order_date    VARCHAR(15),
    ship_date     VARCHAR(15),
    ship_mode     VARCHAR(30),
    customer_id   VARCHAR(20),
    customer_name VARCHAR(60),
    segment       VARCHAR(30),
    country       VARCHAR(30),
    city          VARCHAR(60),
    state         VARCHAR(40),
    postal_code   VARCHAR(10),
    region        VARCHAR(20),
    product_id    VARCHAR(20),
    category      VARCHAR(30),
    sub_category  VARCHAR(30),
    product_name  VARCHAR(255),
    sales         VARCHAR(20),
    quantity      VARCHAR(10),
    discount      VARCHAR(10),
    profit        VARCHAR(20)
);


CREATE TABLE superstore (
    row_id        INT PRIMARY KEY,
    order_id      VARCHAR(30),
    order_date    DATE,
    ship_date     DATE,
    ship_mode     VARCHAR(30),
    customer_id   VARCHAR(20),
    customer_name VARCHAR(60),
    segment       VARCHAR(30),
    country       VARCHAR(30),
    city          VARCHAR(60),
    state         VARCHAR(40),
    postal_code   VARCHAR(10),      -- text, so leading zeros are safe
    region        VARCHAR(20),
    product_id    VARCHAR(20),
    category      VARCHAR(30),
    sub_category  VARCHAR(30),
    product_name  VARCHAR(255),
    sales         DECIMAL(12,4),
    quantity      INT,
    discount      DECIMAL(4,2),
    profit        DECIMAL(12,4)
);

SELECT COUNT(*) AS rows_loaded FROM superstore_stg;

INSERT INTO superstore
SELECT
    CAST(NULLIF(REGEXP_REPLACE(row_id, '[^0-9]', ''), '') AS UNSIGNED),
    TRIM(order_id),
    STR_TO_DATE(NULLIF(TRIM(order_date), ''), '%m/%d/%Y'),
    STR_TO_DATE(NULLIF(TRIM(ship_date), ''),  '%m/%d/%Y'),
    TRIM(ship_mode),
    TRIM(customer_id),
    TRIM(customer_name),
    TRIM(segment),
    TRIM(country),
    TRIM(city),
    TRIM(state),
    TRIM(postal_code),
    TRIM(region),
    TRIM(product_id),
    TRIM(category),
    TRIM(sub_category),
    TRIM(product_name),
    CAST(NULLIF(REGEXP_REPLACE(sales,    '[^0-9.-]', ''), '') AS DECIMAL(12,4)),
    CAST(NULLIF(REGEXP_REPLACE(quantity, '[^0-9]',    ''), '') AS UNSIGNED),
    CAST(NULLIF(REGEXP_REPLACE(discount, '[^0-9.]',   ''), '') AS DECIMAL(4,2)),
    CAST(NULLIF(REGEXP_REPLACE(profit,   '[^0-9.-]', ''), '') AS DECIMAL(12,4))
FROM superstore_stg
WHERE NULLIF(REGEXP_REPLACE(row_id, '[^0-9]', ''), '') IS NOT NULL;

SELECT COUNT(*) FROM superstore;

-- TASK 1: Region-wise sales
SELECT
    region,
    ROUND(SUM(sales), 2)                          AS total_sales,
    ROUND(SUM(profit), 2)                         AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2)      AS profit_margin_pct,
    COUNT(DISTINCT order_id)                      AS total_orders,
    ROUND(SUM(sales) * 100.0 /
          (SELECT SUM(sales) FROM superstore), 2) AS sales_share_pct
FROM superstore
GROUP BY region
ORDER BY total_sales DESC;

-- TASK 2: Highest profit categories (and sub-categories)
SELECT
    category,
    ROUND(SUM(sales), 2)                     AS total_sales,
    ROUND(SUM(profit), 2)                    AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct
FROM superstore
GROUP BY category
ORDER BY total_profit DESC;
 
SELECT
    category,
    sub_category,
    ROUND(SUM(sales), 2)                     AS total_sales,
    ROUND(SUM(profit), 2)                    AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct
FROM superstore
GROUP BY category, sub_category
ORDER BY total_profit DESC;

-- TASK 3: Top 10 customers
SELECT
    customer_id,
    customer_name,
    segment,
    COUNT(DISTINCT order_id)  AS total_orders,
    ROUND(SUM(sales), 2)      AS total_sales,
    ROUND(SUM(profit), 2)     AS total_profit
FROM superstore
GROUP BY customer_id, customer_name, segment
ORDER BY total_sales DESC
LIMIT 10;

-- TASK 4: Monthly sales trend
SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS year_month_,
    ROUND(SUM(sales), 2)             AS monthly_sales,
    ROUND(SUM(profit), 2)            AS monthly_profit,
    COUNT(DISTINCT order_id)         AS orders
FROM superstore
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY year_month_;
 
-- TASK 5: Seasonality (which calendar month is strongest, all years combined)
SELECT
    MONTH(order_date)              AS month_no,
    MONTHNAME(order_date)          AS month_name,
    ROUND(SUM(sales), 2)           AS total_sales,
    ROUND(AVG(sales), 2)           AS avg_line_sales
FROM superstore
GROUP BY MONTH(order_date), MONTHNAME(order_date)
ORDER BY month_no;
 
-- TASK 6: Year-over-year growth
WITH yearly AS (
    SELECT YEAR(order_date) AS yr, SUM(sales) AS sales
    FROM superstore
    GROUP BY YEAR(order_date)
)
SELECT
    yr,
    ROUND(sales, 2) AS total_sales,
    ROUND((sales - LAG(sales) OVER (ORDER BY yr)) /
          LAG(sales) OVER (ORDER BY yr) * 100, 2) AS yoy_growth_pct
FROM yearly;

-- Loss-making sub-categories
SELECT
    category, sub_category,
    ROUND(SUM(profit), 2) AS total_profit
FROM superstore
GROUP BY category, sub_category
HAVING SUM(profit) < 0
ORDER BY total_profit;
 
-- Top 10 loss-making products
SELECT
    product_name,
    ROUND(SUM(sales), 2)  AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
FROM superstore
GROUP BY product_name
HAVING SUM(profit) < 0
ORDER BY total_profit
LIMIT 10;
 
-- Revenue leakage: how discount level affects profit
SELECT
    discount,
    COUNT(*)              AS line_items,
    ROUND(SUM(sales), 2)  AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
FROM superstore
GROUP BY discount
ORDER BY discount;
 
-- Revenue leakage: state-level profit (find the worst states)
SELECT
    region, state,
    ROUND(SUM(sales), 2)  AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
FROM superstore
GROUP BY region, state
ORDER BY total_profit
LIMIT 10;
 
-- ABC product analysis (A = top 70% of sales, B = next 20%, C = last 10%)
WITH product_sales AS (
    SELECT product_name, SUM(sales) AS sales
    FROM superstore
    GROUP BY product_name
),
ranked AS (
    SELECT
        product_name,
        sales,
        SUM(sales) OVER (ORDER BY sales DESC) * 100.0 /
        SUM(sales) OVER ()                       AS cum_pct
    FROM product_sales
)
SELECT
    product_name,
    ROUND(sales, 2)   AS total_sales,
    ROUND(cum_pct, 2) AS cumulative_pct,
    CASE
        WHEN cum_pct <= 70 THEN 'A'
        WHEN cum_pct <= 90 THEN 'B'
        ELSE 'C'
    END AS abc_class
FROM ranked
ORDER BY sales DESC;
 
-- ABC summary: how many products fall in each class
WITH product_sales AS (
    SELECT product_name, SUM(sales) AS sales
    FROM superstore
    GROUP BY product_name
),
ranked AS (
    SELECT product_name, sales,
           SUM(sales) OVER (ORDER BY sales DESC) * 100.0 / SUM(sales) OVER () AS cum_pct
    FROM product_sales
),
classed AS (
    SELECT sales,
           CASE WHEN cum_pct <= 70 THEN 'A' WHEN cum_pct <= 90 THEN 'B' ELSE 'C' END AS abc_class
    FROM ranked
)
SELECT abc_class, COUNT(*) AS products, ROUND(SUM(sales), 2) AS total_sales
FROM classed
GROUP BY abc_class
ORDER BY abc_class;
 
-- Customer retention: repeat vs one-time customers
SELECT
    CASE WHEN order_count = 1 THEN 'One-time' ELSE 'Repeat' END AS customer_type,
    COUNT(*) AS customers
FROM (
    SELECT customer_id, COUNT(DISTINCT order_id) AS order_count
    FROM superstore
    GROUP BY customer_id
) t
GROUP BY customer_type;

