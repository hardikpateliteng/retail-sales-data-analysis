"""
generate_data.py
Generates a realistic, intentionally messy retail sales dataset
(mimics real-world data an analyst would actually receive).
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

N = 5000

categories = {
    "Electronics": ["Headphones", "Smartphone", "Laptop", "Smartwatch", "Tablet"],
    "Clothing": ["T-Shirt", "Jeans", "Jacket", "Shoes", "Dress"],
    "Home & Kitchen": ["Blender", "Cookware Set", "Vacuum Cleaner", "Lamp", "Bedsheet"],
    "Beauty": ["Face Cream", "Shampoo", "Perfume", "Lipstick", "Sunscreen"],
    "Sports": ["Yoga Mat", "Dumbbells", "Cricket Bat", "Running Shoes", "Cycling Helmet"],
}

regions = ["North", "South", "East", "West", "north", "SOUTH", " East", "West "]  # messy casing/spacing
payment_methods = ["Credit Card", "Debit Card", "UPI", "Cash on Delivery", "Net Banking"]
channels = ["Online", "Retail Store"]

start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)

rows = []
customer_pool = [f"CUST{1000+i}" for i in range(400)]
customer_names = [f"Customer_{1000+i}" for i in range(400)]

for i in range(N):
    order_id = f"ORD{10000+i}"
    cust_idx = random.randint(0, len(customer_pool) - 1)
    customer_id = customer_pool[cust_idx]
    customer_name = customer_names[cust_idx]

    category = random.choice(list(categories.keys()))
    product = random.choice(categories[category])

    qty = random.randint(1, 5)
    # inject some return/negative quantity rows
    if random.random() < 0.02:
        qty = -abs(qty)

    base_price = {
        "Electronics": random.uniform(1500, 60000),
        "Clothing": random.uniform(300, 3000),
        "Home & Kitchen": random.uniform(500, 8000),
        "Beauty": random.uniform(150, 2500),
        "Sports": random.uniform(400, 6000),
    }[category]

    # inject some price outliers (data entry errors)
    if random.random() < 0.01:
        base_price *= 50

    discount = round(random.choice([0, 0, 0, 5, 10, 15, 20, 25]) / 100, 2)

    days_offset = random.randint(0, (end_date - start_date).days)
    order_date = start_date + timedelta(days=days_offset)

    # inject inconsistent date formats (as strings) for messiness
    date_format_choice = random.random()
    if date_format_choice < 0.7:
        order_date_str = order_date.strftime("%Y-%m-%d")
    elif date_format_choice < 0.9:
        order_date_str = order_date.strftime("%d/%m/%Y")
    else:
        order_date_str = order_date.strftime("%d-%b-%Y")

    region = random.choice(regions)
    payment = random.choice(payment_methods)
    channel = random.choice(channels)
    shipping_cost = round(random.uniform(0, 200), 2) if channel == "Online" else 0

    rows.append({
        "OrderID": order_id,
        "OrderDate": order_date_str,
        "CustomerID": customer_id,
        "CustomerName": customer_name,
        "Region": region,
        "Category": category,
        "Product": product,
        "Quantity": qty,
        "UnitPrice": round(base_price, 2),
        "Discount": discount,
        "ShippingCost": shipping_cost,
        "PaymentMethod": payment,
        "Channel": channel,
    })

df = pd.DataFrame(rows)

# Inject missing values
for col in ["Region", "PaymentMethod", "UnitPrice", "Discount"]:
    mask = df.sample(frac=0.03).index
    df.loc[mask, col] = np.nan

# Inject duplicate rows
dupes = df.sample(frac=0.02)
df = pd.concat([df, dupes], ignore_index=True)

# Shuffle
df = df.sample(frac=1, random_state=1).reset_index(drop=True)

df.to_csv("/home/claude/project/retail_sales_raw.csv", index=False)
print("Generated retail_sales_raw.csv with", len(df), "rows")
