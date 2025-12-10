# report2_bookings_by_region_jordan.py
"""
Report 2: Booking Trends by Region
Author: Jordan Dardar

This report joins BOOKING, TRIP, and REGION to count how many
bookings each region has. This helps show which regions are more
popular and which may be slowing down.
"""

from db_connection_jordan import get_connection

def report_bookings_by_region():
    cnx = get_connection()
    if cnx is None:
        return

    cursor = cnx.cursor()

    query = """
        SELECT
            r.region_name,
            COUNT(*) AS total_bookings
        FROM BOOKING b
        JOIN TRIP t ON b.trip_id = t.trip_id
        JOIN REGION r ON t.region_id = r.region_id
        GROUP BY r.region_name
        ORDER BY total_bookings DESC, r.region_name;
    """

    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        print("REPORT 2: Booking Trends by Region")
        print("-" * 60)

        if not rows:
            print("No bookings found.")
        else:
            for region_name, total_bookings in rows:
                print(f"Region: {region_name:15}  Total bookings: {total_bookings}")

    except Exception as e:
        print("Error running report:", e)
    finally:
        cursor.close()
        cnx.close()

if __name__ == "__main__":
    report_bookings_by_region()
