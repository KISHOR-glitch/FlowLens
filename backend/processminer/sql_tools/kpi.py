import psycopg2


def kpi_dashboard():

    conn = psycopg2.connect(
        host="localhost",
        database="ecommerce_db",
        user="postgres",
        password="wifirit24",
        port="5433"
    )

    cursor = conn.cursor()

    cursor.execute("""

    WITH last_activity AS (

        SELECT
            e.order_id,
            a.activity_name,

            ROW_NUMBER() OVER(
                PARTITION BY e.order_id
                ORDER BY e.event_time DESC
            ) AS rn

        FROM event_log e

        JOIN activities a
        ON e.activity_id = a.activity_id

    ),

    cycle_time AS (

        SELECT
            order_id,
            MIN(event_time) AS start_time,
            MAX(event_time) AS end_time,
            MAX(event_time) - MIN(event_time) AS total_cycle_time

        FROM event_log

        GROUP BY order_id

    )

    SELECT

        (SELECT COUNT(*) FROM orders) AS total_orders,

        (SELECT COUNT(*)
         FROM last_activity
         WHERE rn = 1
         AND activity_name = 'Delivered') AS completed_orders,

        (SELECT COUNT(*)
         FROM last_activity
         WHERE rn = 1
         AND activity_name = 'Cancelled') AS cancelled_orders,

        (SELECT COUNT(*)
         FROM last_activity
         WHERE rn = 1
         AND activity_name = 'Returned') AS returned_orders,

        (SELECT AVG(total_cycle_time)
         FROM cycle_time) AS average_cycle_time;

    """)

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result


if __name__ == "__main__":

    total, delivered, cancelled, returned, avg_cycle = kpi_dashboard()

    print("\n========== FLOWLENS KPI DASHBOARD ==========\n")

    print(f"Total Orders       : {total}")
    print(f"Delivered Orders   : {delivered}")
    print(f"Cancelled Orders   : {cancelled}")
    print(f"Returned Orders    : {returned}")
    print(f"Average Cycle Time : {avg_cycle}")

    print("\n===========================================\n")