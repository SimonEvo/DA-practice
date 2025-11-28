SELECT SUM(pay_amount) AS gmv
FROM orders;

"output total gmv"

SELECT
    order_month AS month,
    SUM(pay_amount) AS gmv
FROM orders
GROUP BY 1
ORDER BY 1;


SELECT
    order_status,
    SUM(pay_amount) AS gmv
FROM orders
GROUP BY order_status
ORDER BY gmv DESC;