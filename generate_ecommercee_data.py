# generate_ecommerce_data.py
# English comments throughout.
# Produces four CSVs: users.csv, items.csv, orders.csv, order_details.csv
# Schema is suitable for SQL joins and Power BI analysis.

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# ---- Configurable parameters ----
NUM_USERS = 20000           # number of distinct users
NUM_ITEMS = 1000            # number of distinct items (SKUs)
NUM_ORDERS = 23000          # number of orders (order headers)
AVG_ITEMS_PER_ORDER = 3     # average number of line items per order
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)
OUTPUT_DIR = "./ecommerce_simulated"  # output directory for CSVs

# Create output directory if not exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

np.random.seed(42)
random.seed(42)

# ---- 1) Generate users table ----
# user_id, gender, age, register_date, city, member_level
user_ids = [f"u{100000+i}" for i in range(NUM_USERS)]
genders = np.random.choice(["M", "F", "Unknown"], size=NUM_USERS, p=[0.48, 0.50, 0.02])
ages = np.clip(np.random.normal(loc=32, scale=8, size=NUM_USERS).astype(int), 18, 70)
register_dates = [START_DATE + timedelta(days=int(x)) for x in np.random.randint(0, (END_DATE-START_DATE).days, NUM_USERS)]
cities = np.random.choice(["Beijing","Shanghai","Guangzhou","Shenzhen","Chengdu","Hangzhou","Nanjing","Wuhan","Xi'an","Chongqing"], size=NUM_USERS)
member_levels = np.random.choice(["None","Silver","Gold","Platinum"], size=NUM_USERS, p=[0.6,0.25,0.1,0.05])

users_df = pd.DataFrame({
    "user_id": user_ids,
    "gender": genders,
    "age": ages,
    "register_date": [d.strftime("%Y-%m-%d") for d in register_dates],
    "city": cities,
    "member_level": member_levels
})

# ---- 2) Generate items table ----
# item_id, category, brand, price, cost, launch_date
categories = ["Electronics","Home","Fashion","Beauty","Sports","Toys","Grocery"]
brands_per_category = {
    "Electronics": ["ElecMax","Techio","NovaTek","GigaPro"],
    "Home": ["HomeEase","ComfortCo","CasaBella"],
    "Fashion": ["TrendWear","UrbanStyle","ClassicCloth"],
    "Beauty": ["GlowUp","PureSkin","Beautify"],
    "Sports": ["ProFit","MoveWell","Sportive"],
    "Toys": ["FunTime","Playful","KidJoy"],
    "Grocery": ["FreshFarm","DailyGood","PantryPlus"]
}
item_ids = [f"i{200000+i}" for i in range(NUM_ITEMS)]
item_category = np.random.choice(categories, size=NUM_ITEMS, p=[0.15,0.15,0.2,0.1,0.1,0.1,0.2])
item_brand = [random.choice(brands_per_category[cat]) for cat in item_category]

# price distribution by category rough ranges (in CNY)
price_ranges = {
    "Electronics": (100, 5000),
    "Home": (20, 800),
    "Fashion": (30, 800),
    "Beauty": (10, 300),
    "Sports": (40, 1000),
    "Toys": (10, 300),
    "Grocery": (3, 200)
}
prices = []
costs = []
launch_dates = []
for cat in item_category:
    low, high = price_ranges[cat]
    p = round(float(np.random.lognormal(mean=np.log((low+high)/4), sigma=0.8)), 2)
    p = float(np.clip(p, low, high))
    c = round(p * (0.4 + np.random.rand()*0.4), 2)  # cost between 40%-80% of price
    prices.append(p)
    costs.append(c)
    delta_days = np.random.randint(0, 365*3)
    launch_dates.append((START_DATE + timedelta(days=delta_days)).strftime("%Y-%m-%d"))

items_df = pd.DataFrame({
    "item_id": item_ids,
    "category": item_category,
    "brand": item_brand,
    "price": prices,
    "cost": costs,
    "launch_date": launch_dates
})

# ---- 3) Generate orders and order_details ----
order_ids = [f"o{300000+i}" for i in range(NUM_ORDERS)]
order_user = np.random.choice(user_ids, size=NUM_ORDERS)
total_days = (END_DATE - START_DATE).days
order_dates = []
for _ in range(NUM_ORDERS):
    r = np.random.rand()
    biased = int((1 - (1-r)**2) * total_days)  # bias towards recent dates
    order_dates.append((START_DATE + timedelta(days=biased)).strftime("%Y-%m-%d"))

status_choices = ["completed","cancelled","refunded","pending","shipped"]
status_probs = [0.85, 0.03, 0.03, 0.02, 0.07]
order_status = np.random.choice(status_choices, p=status_probs, size=NUM_ORDERS)

orders_df = pd.DataFrame({
    "order_id": order_ids,
    "user_id": order_user,
    "order_date": order_dates,
    "order_status": order_status
})

detail_rows = []
detail_id_counter = 400000
for oid, odate, ouid, ostatus in zip(order_ids, order_dates, order_user, order_status):
    num_lines = max(1, int(np.random.poisson(AVG_ITEMS_PER_ORDER)))
    chosen_items = np.random.choice(item_ids, size=num_lines)
    for it in chosen_items:
        detail_id = f"d{detail_id_counter}"
        detail_id_counter += 1
        item_row = items_df[items_df["item_id"] == it].iloc[0]
        list_price = float(item_row["price"])
        discount = np.random.choice([1.0, 0.95, 0.9, 0.8, 0.5], p=[0.7,0.15,0.08,0.05,0.02])
        sale_price = round(list_price * discount, 2)
        qty = int(np.random.zipf(a=2.0)) if np.random.rand() < 0.02 else np.random.randint(1,4)
        if ostatus == "refunded":
            sale_price = 0.0
        line_total = round(sale_price * qty, 2)
        detail_rows.append({
            "order_detail_id": detail_id,
            "order_id": oid,
            "item_id": it,
            "quantity": qty,
            "list_price": list_price,
            "sale_price": sale_price,
            "line_total": line_total
        })

order_details_df = pd.DataFrame(detail_rows)

# Compute pay_amount per order
pay_amounts = order_details_df.groupby("order_id")["line_total"].sum().reset_index().rename(columns={"line_total":"pay_amount"})
orders_df = orders_df.merge(pay_amounts, on="order_id", how="left")
orders_df["pay_amount"] = orders_df["pay_amount"].fillna(0.0).round(2)
orders_df["order_month"] = pd.to_datetime(orders_df["order_date"]).dt.to_period("M").astype(str)

# map category/brand into order_details for easier analysis
order_details_df["category"] = order_details_df["item_id"].map(items_df.set_index("item_id")["category"])
order_details_df["brand"] = order_details_df["item_id"].map(items_df.set_index("item_id")["brand"])

# ---- Save CSV files ----
users_df.to_csv(os.path.join(OUTPUT_DIR, "users.csv"), index=False, encoding="utf-8-sig")
items_df.to_csv(os.path.join(OUTPUT_DIR, "items.csv"), index=False, encoding="utf-8-sig")
orders_df.to_csv(os.path.join(OUTPUT_DIR, "orders.csv"), index=False, encoding="utf-8-sig")
order_details_df.to_csv(os.path.join(OUTPUT_DIR, "order_details.csv"), index=False, encoding="utf-8-sig")

print("Saved CSVs to", os.path.abspath(OUTPUT_DIR))
print("Shapes:")
print(" users:", users_df.shape)
print(" items:", items_df.shape)
print(" orders:", orders_df.shape)
print(" order_details:", order_details_df.shape)
