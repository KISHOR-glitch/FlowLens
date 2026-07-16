import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
import psycopg2


def process_discovery():

    conn = psycopg2.connect(
        host="localhost",
        database="ecommerce_db",
        user="postgres",
        password=os.environ.get("DB_PASSWORD", "your_new_secure_password"),
        port="5433"
    )

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        e.order_id,
        a.activity_name AS current_activity,

        LEAD(a.activity_name)
        OVER(
            PARTITION BY e.order_id
            ORDER BY e.event_time
        ) AS next_activity

    FROM event_log e
    JOIN activities a
    ON e.activity_id = a.activity_id

    ORDER BY e.order_id, e.event_time;
    """)

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result


if __name__ == "__main__":

    rows = process_discovery()

    for row in rows[:20]:
        print(row)