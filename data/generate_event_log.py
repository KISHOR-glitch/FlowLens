import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
import psycopg2
import random
from datetime import timedelta

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="ecommerce_db",
    user="postgres",
    password=os.environ.get("DB_PASSWORD", "your_new_secure_password"),
    port="5433"
)

cursor = conn.cursor()

# Get all orders
cursor.execute("""
SELECT order_id, created_at
FROM orders
ORDER BY order_id;
""")

orders = cursor.fetchall()

events = []

for order_id, created_at in orders:

    current_time = created_at

    # Random scenario
    scenario = random.random()

    # -------------------------
    # Order Placed
    # -------------------------
    events.append((order_id, 1, 1, current_time))

    # -------------------------
    # Payment Verification
    # -------------------------
    current_time += timedelta(minutes=5)

    # Random payment team
    payment_team = random.choice([2, 3])

    events.append((order_id, 2, payment_team, current_time))

    # -------------------------
    # Payment Delay (15%)
    # -------------------------
    if scenario < 0.15:
        current_time += timedelta(days=random.randint(2, 4))
    else:
        current_time += timedelta(hours=2)

    # -------------------------
    # Cancelled Orders (7%)
    # -------------------------
    if 0.15 <= scenario < 0.22:
        events.append((order_id, 7, payment_team, current_time))
        continue

    # -------------------------
    # Packed
    # -------------------------
    warehouse = random.choice([4, 5])
    events.append((order_id, 3, warehouse, current_time))

    # -------------------------
    # Skip Packed (5%)
    # -------------------------
    if 0.22 <= scenario < 0.27:

        current_time += timedelta(hours=5)
        courier = random.choice([6, 7])

        events.append((order_id, 4, courier, current_time))

        current_time += timedelta(days=1)
        events.append((order_id, 6, courier, current_time))

        continue

    # -------------------------
    # Shipped
    # -------------------------
    current_time += timedelta(hours=5)
    courier = random.choice([6, 7])

    events.append((order_id, 4, courier, current_time))

    # -------------------------
    # Out for Delivery
    # -------------------------
    current_time += timedelta(days=1)

    events.append((order_id, 5, courier, current_time))

    # -------------------------
    # Delivered
    # -------------------------
    current_time += timedelta(hours=5)

    events.append((order_id, 6, courier, current_time))

    # -------------------------
    # Returned Orders (3%)
    # -------------------------
    if scenario >= 0.97:

        current_time += timedelta(days=3)

        events.append((order_id, 8, courier, current_time))

# Insert into PostgreSQL
cursor.executemany("""
INSERT INTO event_log
(order_id, activity_id, resource_id, event_time)
VALUES (%s, %s, %s, %s)
""", events)

conn.commit()

cursor.close()
conn.close()

print("✅ Event log generated successfully!")