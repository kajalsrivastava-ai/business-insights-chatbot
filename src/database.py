import pandas as pd
import sqlite3
import random
from datetime import datetime, timedelta
import os

def create_sample_data():
    random.seed(42)

    products = [
        ("Laptop Pro 15", "Electronics", 85000),
        ("Wireless Mouse", "Electronics", 1200),
        ("Standing Desk", "Furniture", 22000),
        ("Office Chair", "Furniture", 15000),
        ("Monitor 27in", "Electronics", 28000),
        ("Notebook Pack", "Stationery", 450),
        ("Whiteboard", "Office Supplies", 3500),
        ("Webcam HD", "Electronics", 4500),
        ("Desk Lamp", "Office Supplies", 1800),
        ("Keyboard Mech", "Electronics", 6500),
    ]

    regions = ["North", "South", "East", "West", "Central"]
    sales_reps = ["Amit Sharma", "Priya Patel", "Rahul Singh",
                  "Neha Gupta", "Vikram Rao"]

    rows = []
    start_date = datetime(2024, 1, 1)

    for i in range(500):
        product, category, base_price = random.choice(products)
        region = random.choice(regions)
        rep = random.choice(sales_reps)
        quantity = random.randint(1, 20)
        price = base_price * random.uniform(0.9, 1.1)
        revenue = round(price * quantity, 2)
        date = start_date + timedelta(days=random.randint(0, 364))

        rows.append({
            "order_id": f"ORD-{1000 + i}",
            "date": date.strftime("%Y-%m-%d"),
            "product": product,
            "category": category,
            "region": region,
            "sales_rep": rep,
            "quantity": quantity,
            "unit_price": round(price, 2),
            "revenue": revenue
        })

    return pd.DataFrame(rows)

def load_to_sqlite(df, db_path="data/sales.db"):
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(db_path)
    df.to_sql("sales", conn, if_exists="replace", index=False)
    conn.close()
    print(f"Loaded {len(df)} rows into {db_path}")

def run_query(query, db_path="data/sales.db"):
    conn = sqlite3.connect(db_path)
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result

def get_schema(db_path="data/sales.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(sales)")
    cols = cursor.fetchall()
    conn.close()
    schema = "Table: sales\nColumns:\n"
    for col in cols:
        schema += f"  - {col[1]} ({col[2]})\n"
    return schema

if __name__ == "__main__":
    df = create_sample_data()
    load_to_sqlite(df)
    df.to_csv("data/sales.csv", index=False)
    print("\nSchema:")
    print(get_schema())
    print("\nSample query — top 5 products by revenue:")
    print(run_query("""
        SELECT product, SUM(revenue) as total_revenue
        FROM sales
        GROUP BY product
        ORDER BY total_revenue DESC
        LIMIT 5
    """))