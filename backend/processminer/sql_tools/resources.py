import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
import psycopg2


def resource_analysis():

    conn = psycopg2.connect(
        host="localhost",
        database="ecommerce_db",
        user="postgres",
        password=os.environ.get("DB_PASSWORD", "your_new_secure_password"),
        port="5433"
    )

    cursor = conn.cursor()

    cursor.execute("""

    WITH activity_times AS (

        SELECT

            r.resource_name,

            a.activity_name,

            e.event_time,

            LEAD(e.event_time)
            OVER(
                PARTITION BY e.order_id
                ORDER BY e.event_time
            ) AS next_time

        FROM event_log e

        JOIN resources r
        ON e.resource_id = r.resource_id

        JOIN activities a
        ON e.activity_id = a.activity_id

    )

    SELECT

        resource_name,

        COUNT(*) AS activities_handled,

        AVG(next_time - event_time) AS average_processing_time

    FROM activity_times

    WHERE next_time IS NOT NULL

    GROUP BY resource_name

    ORDER BY average_processing_time DESC;

    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


if __name__ == "__main__":

    results = resource_analysis()

    for row in results:
        print(row)