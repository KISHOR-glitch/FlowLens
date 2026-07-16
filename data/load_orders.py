import pandas as pd
import psycopg2

# Read CSV
df = pd.read_csv("orders.csv")

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="ecommerce_db",
    user="postgres",
    password="wifirit24",
    port="5433"
)

cursor = conn.cursor()

# Insert rows
for _, row in df.iterrows():

    cursor.execute("""
        INSERT INTO orders
        (order_id, customer_name, city, payment_method, status, created_at)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (
        int(row["order_id"]),
        row["customer_name"],
        row["city"],
        row["payment_method"],
        row["status"],
        row["created_at"]
    ))

conn.commit()

cursor.close()
conn.close()

print("Orders inserted successfully!")