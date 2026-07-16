import psycopg2


def variant_analysis():

    conn = psycopg2.connect(
        host="localhost",
        database="ecommerce_db",
        user="postgres",
        password="wifirit24",
        port="5433"
    )

    cursor = conn.cursor()

    cursor.execute("""

    SELECT
        order_id,

        STRING_AGG(
            a.activity_name,
            ' -> '
            ORDER BY e.event_time
        ) AS process_variant

    FROM event_log e
    JOIN activities a
    ON e.activity_id = a.activity_id

    GROUP BY order_id

    ORDER BY order_id;

    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


if __name__ == "__main__":

    variants = variant_analysis()

    for row in variants[:20]:
        print(row)