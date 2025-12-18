# Report_3.py
# Author: Alexander Baldree
# Description: Report 3 – Sales vs Rental Revenue with timestamps, timezone,
# monthly totals, and grand totals by order type

import mysql.connector
from datetime import datetime
import pytz

# -------------------------------------------
# REPORT GENERATED TIMESTAMP (CST)
# -------------------------------------------
cst = pytz.timezone("US/Central")
generated_timestamp = datetime.now(cst).strftime("%Y-%m-%d %H:%M:%S %Z")

print("\n======================================================")
print("REPORT 3: Sales vs Rental Revenue")
print(f"Report Generated: {generated_timestamp}")
print("======================================================\n")

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

# ======================================================
# SECTION 1: DETAILED SALES VS RENTAL REVENUE (TIMESTAMP)
# ======================================================
print("DETAILED REVENUE BY ORDER\n")

query_detailed = """
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

cursor.execute(query_detailed)
rows = cursor.fetchall()

print(f"{'Order Type':<15}{'Order Timestamp':<25}{'Total Revenue':>15}")
print("-" * 55)

for order_type, order_timestamp, total_revenue in rows:
    print(
        f"{order_type:<15}"
        f"{str(order_timestamp):<25}"
        f"${total_revenue:>14,.2f}"
    )

print("\n------------------------------------------------------\n")

# ======================================================
# SECTION 2: MONTHLY TOTALS
# ======================================================
print("MONTHLY REVENUE TOTALS\n")

query_monthly = """
SELECT 
    eo.order_type,
    DATE_FORMAT(eo.order_date, '%Y-%m') AS order_month,
    SUM(ol.quantity * ol.price_each) AS monthly_total
FROM EQUIPMENT_ORDER eo
JOIN ORDER_LINE ol 
    ON eo.order_id = ol.order_id
GROUP BY eo.order_type, order_month
ORDER BY order_month, eo.order_type;
"""

cursor.execute(query_monthly)
rows = cursor.fetchall()

print(f"{'Order Type':<15}{'Month':<15}{'Monthly Total':>15}")
print("-" * 50)

for order_type, order_month, monthly_total in rows:
    print(
        f"{order_type:<15}"
        f"{order_month:<15}"
        f"${monthly_total:>14,.2f}"
    )

print("\n------------------------------------------------------\n")

# ======================================================
# SECTION 3: GRAND TOTALS BY ORDER TYPE
# ======================================================
print("GRAND TOTALS BY ORDER TYPE\n")

query_grand_totals = """
SELECT 
    eo.order_type,
    SUM(ol.quantity * ol.price_each) AS grand_total
FROM EQUIPMENT_ORDER eo
JOIN ORDER_LINE ol 
    ON eo.order_id = ol.order_id
GROUP BY eo.order_type;
"""

cursor.execute(query_grand_totals)
rows = cursor.fetchall()

print(f"{'Order Type':<15}{'Grand Total Revenue':>20}")
print("-" * 35)

for order_type, grand_total in rows:
    print(
        f"{order_type:<15}"
        f"${grand_total:>19,.2f}"
    )

print("\n======================================================\n")

# -------------------------------------------
# CLEANUP
# -------------------------------------------
cursor.close()
db.close()
print("Database connection closed.")
