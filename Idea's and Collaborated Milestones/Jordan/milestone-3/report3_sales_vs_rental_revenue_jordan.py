# report3_sales_vs_rental_revenue_jordan.py
"""
Report 3: Sales vs Rental Revenue
Author: Jordan Dardar

This report looks at all equipment orders and compares total revenue
from SALES vs RENTALS by summing quantity * price_each for each
order type.
"""

from db_connection_jordan import get_connection

def report_sales_vs_rentals():
    cnx = get_connection()
    if cnx is None:
        return

    cursor = cnx.cursor()

    query = """
        SELECT
            eo.order_type,
            SUM(ol.quantity * ol.price_each) AS total_revenue
        FROM EQUIPMENT_ORDER eo
        JOIN ORDER_LINE ol ON eo.order_id = ol.order_id
        GROUP BY eo.order_type;
    """

    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        print("REPORT 3: Sales vs Rental Revenue")
        print("-" * 60)

        if not rows:
            print("No order data found.")
        else:
            for order_type, total_revenue in rows:
                print(f"{order_type}: {total_revenue}")
    except Exception as e:
        print("Error running report:", e)
    finally:
        cursor.close()
        cnx.close()

if __name__ == "__main__":
    report_sales_vs_rentals()
