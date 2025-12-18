# Report_3.py
# Author: Alexander Baldree
# Description: Report 3 – Sales vs Rental Revenue with timestamps and currency formatting

import mysql.connector

# -------------------------------------------
# DATABASE CONNECTION
# -------------------------------------------
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",              
        password="Gillmore21",      
        database="outland"      
    )

    cursor = db.cursor()
    print("Database connection successful.\n")

except mysql.connector.Error as err:
    print(f"Error connecting to database: {err}")
    exit(1)

# -------------------------------------------
# REPORT 3: SALES VS RENTAL REVENUE (TIMESTAMPED)
# -------------------------------------------
print("REPORT 3: Sales vs Rental Revenue\n")

query_sales_vs_rentals = """
SELECT 
    eo.order_type,
    eo.order_date AS order_timestamp,
    SUM(ol.quantity * ol.price_each) AS total_revenue
FROM EQUIPMENT_ORDER eo
JOIN ORDER_LINE ol 
    ON eo.order_id = ol.order_id
GROUP BY eo.order_type, eo.order_date
ORDER BY eo.order_date, eo.order_type;
"""

cursor.execute(query_sales_vs_rentals)
rows = cursor.fetchall()

# -------------------------------------------
# TABLE OUTPUT
# -------------------------------------------
print(f"{'Order Type':<15}{'Order Timestamp':<25}{'Total Revenue':>15}")
print("-" * 55)

for order_type, order_timestamp, total_revenue in rows:
    revenue_formatted = f"${total_revenue:,.2f}"
    print(f"{order_type:<15}{str(order_timestamp):<25}{revenue_formatted:>15}")

print("\n-------------------------------------------\n")

# -------------------------------------------
# CLEANUP
# -------------------------------------------
cursor.close()
db.close()
print("Database connection closed.")

