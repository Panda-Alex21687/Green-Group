# Milestone_5_Alexander.py
# Author: Alexander Baldree
# Description: Final Combined Reports 1–5 for Outland Adventures (Milestone #5)

import mysql.connector
from datetime import datetime
import pytz

# -------------------------------------------
# DATABASE CONFIGURATION
# -------------------------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Gillmore21",   # keep your password
    "database": "outland"
}

# -------------------------------------------
# TIMESTAMP (CST)
# -------------------------------------------
cst = pytz.timezone("US/Central")
generated_timestamp = datetime.now(cst).strftime("%Y-%m-%d %H:%M:%S %Z")

# -------------------------------------------
# FORMATTED REPORT OUTPUT
# -------------------------------------------
def print_formatted_report(title, headers, rows, currency_cols=None):
    print("\n" + "=" * 80)
    print(title.upper())
    print(f"Generated: {generated_timestamp}")
    print("=" * 80)

    if not rows:
        print("No data available.\n")
        return

    col_widths = [max(len(h), 15) for h in headers]

    for row in rows:
        for i, value in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(value)))

    header_row = " | ".join(headers[i].ljust(col_widths[i]) for i in range(len(headers)))
    print(header_row)
    print("-" * len(header_row))

    for row in rows:
        formatted_row = []
        for i, value in enumerate(row):
            if currency_cols and i in currency_cols:
                formatted_row.append(f"${float(value):,.2f}".rjust(col_widths[i]))
            else:
                formatted_row.append(str(value).ljust(col_widths[i]))
        print(" | ".join(formatted_row))

    print()

# -------------------------------------------
# DATABASE CONNECTION
# -------------------------------------------
try:
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor()
except mysql.connector.Error as err:
    print(f"Database connection error: {err}")
    exit(1)

# =====================================================
# REPORT 1 – EQUIPMENT OLDER THAN 5 YEARS (FIXED)
# =====================================================
query_report_1 = """
SELECT equipment_desc,
       purchase_date
FROM EQUIPMENT
WHERE purchase_date < DATE_SUB(CURDATE(), INTERVAL 5 YEAR);
"""

cursor.execute(query_report_1)
rows = cursor.fetchall()

print_formatted_report(
    title="Report 1 – Equipment Older Than 5 Years",
    headers=["Equipment Description", "Purchase Date"],
    rows=[(r[0], r[1].strftime("%Y-%m-%d")) for r in rows]
)

# =====================================================
# REPORT 2 – TOTAL ORDERS BY ORDER TYPE
# =====================================================
query_report_2 = """
SELECT order_type,
       COUNT(*) AS total_orders
FROM EQUIPMENT_ORDER
GROUP BY order_type;
"""

cursor.execute(query_report_2)
rows = cursor.fetchall()

print_formatted_report(
    title="Report 2 – Total Orders by Order Type",
    headers=["Order Type", "Total Orders"],
    rows=rows
)

# =====================================================
# REPORT 3 – SALES VS RENTAL REVENUE
# =====================================================
query_report_3 = """
SELECT eo.order_type,
       SUM(ol.quantity * ol.price_each) AS total_revenue
FROM EQUIPMENT_ORDER eo
JOIN ORDER_LINE ol ON eo.order_id = ol.order_id
GROUP BY eo.order_type;
"""

cursor.execute(query_report_3)
rows = cursor.fetchall()

print_formatted_report(
    title="Report 3 – Sales vs Rental Revenue",
    headers=["Order Type", "Total Revenue"],
    rows=rows,
    currency_cols=[1]
)

# =====================================================
# REPORT 4 – BOOKINGS BY REGION
# =====================================================
query_report_4 = """
SELECT region,
       COUNT(*) AS total_bookings
FROM CUSTOMER_BOOKING
GROUP BY region;
"""

cursor.execute(query_report_4)
rows = cursor.fetchall()

print_formatted_report(
    title="Report 4 – Customer Bookings by Region",
    headers=["Region", "Total Bookings"],
    rows=rows
)

# =====================================================
# REPORT 5 – TOP REVENUE-GENERATING EQUIPMENT
# =====================================================
query_report_5 = """
SELECT e.equipment_desc,
       SUM(ol.quantity * ol.price_each) AS total_revenue
FROM EQUIPMENT e
JOIN ORDER_LINE ol ON e.equipment_id = ol.equipment_id
GROUP BY e.equipment_desc
ORDER BY total_revenue DESC
LIMIT 5;
"""

cursor.execute(query_report_5)
rows = cursor.fetchall()

print_formatted_report(
    title="Report 5 – Top Revenue-Generating Equipment",
    headers=["Equipment Description", "Total Revenue"],
    rows=rows,
    currency_cols=[1]
)

# -------------------------------------------
# CLEANUP
# -------------------------------------------
cursor.close()
db.close()

print("All Outland Adventures reports generated successfully.")
