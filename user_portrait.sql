
"output total numebr of users"
SELECT COUNT(DISTINCT user_id) as total_users
FROM orders;


"number of new users by month"

WITH first_order AS (
    SELECT
        user_id,
        MIN(order_date::date) AS first_date
    FROM orders
    GROUP BY user_id
)
SELECT
    DATE_TRUNC('month', first_date::date) AS month,
    COUNT(*) AS new_users
FROM first_order
GROUP BY 1
ORDER BY 1;

"repurchase rate"
WITH user_orders AS (
    SELECT
        user_id,
        COUNT(*) as order_count
    FROM orders
    GROUP BY user_id
)
SELECT
    SUM(CASE WHEN order_count >= 2 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS repurchase_rate
FROM user_orders;

SELECT 
    SUM(pay_amount)/COUNT(DISTINCT user_id) as cov,
    SUM(pay_amount)/COUNT(*) as aov
FROM orders;


SELECT
    DATE_TRUNC('month', order_date::date) AS month,
    SUM(pay_amount)/COUNT(*) as aov
FROM orders
GROUP BY 1
ORDER BY 1;