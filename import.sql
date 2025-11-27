-- import users
COPY users
FROM '/tmp/users.csv'
CSV HEADER;

-- import products
COPY items
FROM '/tmp/items.csv'
CSV HEADER;

-- import orders
COPY orders
FROM '/tmp/orders.csv'
CSV HEADER;

-- import order_details
COPY order_details
FROM '/tmp/order_details.csv'
CSV HEADER;
