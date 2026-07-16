# before if statemens and b
# efore making into long chain toolLangGraph cannot call this directly.
'''
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
import psycopg2


def bottleneck_analysis():

    conn = psycopg2.connect(
        host="localhost",
        database="ecommerce_db",
        user="postgres",
        password=os.environ.get("DB_PASSWORD", "your_new_secure_password"),
        port="5433"
    )

    cursor = conn.cursor()

    cursor.execute("""
    WITH transitions AS (

        SELECT

            a.activity_name AS current_activity,

            LEAD(a.activity_name)
            OVER(
                PARTITION BY e.order_id
                ORDER BY e.event_time
            ) AS next_activity,

            e.event_time,

            LEAD(e.event_time)
            OVER(
                PARTITION BY e.order_id
                ORDER BY e.event_time
            ) AS next_time

        FROM event_log e

        JOIN activities a
        ON e.activity_id = a.activity_id

    )

    SELECT

        current_activity,

        next_activity,

        AVG(next_time - event_time) AS average_delay

    FROM transitions

    WHERE next_activity IS NOT NULL

    GROUP BY
        current_activity,
        next_activity

    ORDER BY average_delay DESC;
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


if __name__ == "__main__":

    results = bottleneck_analysis()

    for row in results:
        print(row)
        '''

        
import psycopg2



def bottleneck_analysis():

    conn = psycopg2.connect(
        host="localhost",
        database="ecommerce_db",
        user="postgres",
        password=os.environ.get("DB_PASSWORD", "your_new_secure_password"),
        port="5433"
    )

    cursor = conn.cursor()

    cursor.execute("""
    WITH transitions AS (

        SELECT

            a.activity_name AS current_activity,

            LEAD(a.activity_name)
            OVER(
                PARTITION BY e.order_id
                ORDER BY e.event_time
            ) AS next_activity,

            e.event_time,

            LEAD(e.event_time)
            OVER(
                PARTITION BY e.order_id
                ORDER BY e.event_time
            ) AS next_time

        FROM event_log e

        JOIN activities a
        ON e.activity_id = a.activity_id

    )

    SELECT

        current_activity,

        next_activity,

        AVG(next_time - event_time) AS average_delay

    FROM transitions

    WHERE next_activity IS NOT NULL

    GROUP BY
        current_activity,
        next_activity

    ORDER BY average_delay DESC;
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


if __name__ == "__main__":

    results = bottleneck_analysis()

    for row in results:
        print(row)
        