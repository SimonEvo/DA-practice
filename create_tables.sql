CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    gender VARCHAR,
    age INT,
    register_date DATE,
    city TEXT,
    member_level TEXT
);



CREATE TABLE items (
    item_id TEXT PRIMARY KEY,
    category TEXT,
    brand TEXT, 
    price NUMERIC(10, 2),
    cost NUMERIC(10,2),
    launch_date DATE
);

CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    user_id TEXT,
    order_date DATE,
    order_status TEXT,
    pay_amount NUMERIC(10,2), 
    order_month VARCHAR(7)
);

CREATE TABLE order_details (
    order_detail_id TEXT PRIMARY KEY,
    order_id TEXT,
    item_id TEXT,
    quantity INT,
    list_price NUMERIC(10, 2),
    sale_price NUMERIC(10, 2),
    line_total NUMERIC(10, 2),
    category TEXT,
    brand TEXT
);



DROP TABLE items;
DROP TABLE order_details;
DROP TABLE users;
DROP Table orders;