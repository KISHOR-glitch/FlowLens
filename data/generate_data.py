from faker import Faker
import pandas as pd
import random
from datetime import datetime

fake = Faker()

orders = []

for order_id in range(1,1001):

    orders.append({
        "order_id": order_id,
        "customer_name": fake.name(),
        "city": random.choice([
            "Bangalore",
            "Mumbai",
            "Hyderabad",
            "Delhi",
            "Chennai"
        ]),
        "payment_method": random.choice([
            "UPI",
            "Card",
            "Net Banking"
        ]),
        "status": "Processing",
        "created_at": datetime.now()
    })

df = pd.DataFrame(orders)

df.to_csv("orders.csv", index=False)

print("Orders Created")