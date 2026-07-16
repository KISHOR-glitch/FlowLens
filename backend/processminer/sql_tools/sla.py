import psycopg2


def sla_detection():

    conn = psycopg2.connect(
        host="localhost",
        database="ecommerce_db",
        user="postgres",
        password="wifirit24",
        port="5433"
    )

    cursor = conn.cursor()

    cursor.execute("""

    WITH transitions AS (

        SELECT

            e.order_id,

            a.activity_name,

            e.event_time,

            LEAD(e.event_time)
            OVER(
                PARTITION BY e.order_id
                ORDER BY e.event_time
            ) AS next_time,

            LEAD(a.activity_name)
            OVER(
                PARTITION BY e.order_id
                ORDER BY e.event_time
            ) AS next_activity

        FROM event_log e

        JOIN activities a
        ON e.activity_id = a.activity_id

    )

    SELECT

        order_id,

        activity_name,

        next_activity,

        next_time - event_time AS delay

    FROM transitions

    WHERE
        activity_name = 'Payment Verification'
        AND next_time - event_time > INTERVAL '24 hours'

    ORDER BY delay DESC;

    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


if __name__ == "__main__":

    results = sla_detection()

    for row in results[:20]:
        print(row)