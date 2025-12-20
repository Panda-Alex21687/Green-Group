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
    "password": "Gillmore21",
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

# -------------------------------------------
# AUTO-DETECT EQUIPMENT TABLE COLUMNS
# -------------------------------------------
cursor.execute("DESCRIBE EQUIPMENT;")
columns = cursor.fetchall()

column_names = [c[0] for c in columns]

# detect equipment descriptor column
equipment_column = None
for col in column_names:
    if "id" not in col.lower() and "date" not in col.lower():
        equipment_column = col
        break

# detect date column
date_column = None
for col in column_names:
    if "date" in col.lower():
        date_column = col
        break

if not equipment_column or not date_column:
    print("ERROR: Could not determine equipment or date column.")
    print("Detected columns:", column_names)
    cursor.close()
    db.close()
    exit(1)

# =====================================================
# REPORT 1 – EQUIPMENT OLDER THAN 5 YEARS (AUTO-SAFE)
# =====================================================
query_report_1 = f"""
SELECT {equipment_column},
       {date_column}
FROM EQUIPMENT
WHERE {date_column} < DATE_SUB(CURDATE(), INTERVAL 5 YEAR);
"""

cursor.execute(query_report_1)
rows = cursor.fetchall()

print_formatted_report(
    title="Report 1 – Equipment Older Than 5 Years",
    headers=["Equipment", "Purchase Date"],
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

# report 4 guide assignments 

print("REPORT 4: Guide Assignment Report\n")
from datetime import datetime  # Add this import at the top of your file

query_guide_assignments = """
SELECT e.first_name, e.last_name, e.role,
       COUNT(t.trip_id) AS trips_assigned
FROM EMPLOYEE e
LEFT JOIN TRIP t ON e.employee_id = t.guide_id
WHERE e.role = 'Guide'
GROUP BY e.employee_id, e.first_name, e.last_name, e.role
ORDER BY trips_assigned DESC;
"""

cursor.execute(query_guide_assignments)
rows = cursor.fetchall()

# Print uppercase headers
print(f"{'FIRST NAME':<15} {'LAST NAME':<15} {'ROLE':<10} {'TRIPS ASSIGNED':<15}")
print("-" * 60)

# Print formatted data
for row in rows:
    print(f"{row[0]:<15} {row[1]:<15} {row[2]:<10} {row[3]:<15}")

# Add timestamp at the bottom
report_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(f"\nReport generated on: {report_time}")

print("\n-------------------------------------------\n")

# report 5 frequency of equipment order 
from datetime import datetime  # Make sure this is at the top of your file

print("REPORT 5: Equipment Order Frequency\n")

query_equipment_popularity = """
SELECT e.item_name, e.item_type,
       COUNT(DISTINCT ol.order_id) AS times_ordered,
       COALESCE(SUM(ol.quantity), 0) AS total_quantity_ordered,
       COALESCE(SUM(ol.quantity * ol.price_each), 0) AS total_revenue
FROM EQUIPMENT e
LEFT JOIN ORDER_LINE ol ON e.equipment_id = ol.equipment_id
GROUP BY e.equipment_id, e.item_name, e.item_type
ORDER BY total_revenue DESC;
"""

cursor.execute(query_equipment_popularity)
rows = cursor.fetchall()

# Separate rentals and sales
rentals = [row for row in rows if row[1] == 'Rental']
sales = [row for row in rows if row[1] == 'Sale']

# Print RENTALS section
print("=" * 90)
print("RENTALS")
print("=" * 90)
print(f"{'ITEM NAME':<25} {'ITEM TYPE':<12} {'TIMES ORDERED':<15} {'TOTAL QUANTITY':<16} {'TOTAL REVENUE':<15}")
print("-" * 90)

for row in rentals:
    print(f"{row[0]:<25} {row[1]:<12} {row[2]:<15} {row[3]:<16} ${row[4]:<14.2f}")

print(f"\nTotal Rental Items: {len(rentals)}")

# Print SALES section
print("\n" + "=" * 90)
print("SALES")
print("=" * 90)
print(f"{'ITEM NAME':<25} {'ITEM TYPE':<12} {'TIMES ORDERED':<15} {'TOTAL QUANTITY':<16} {'TOTAL REVENUE':<15}")
print("-" * 90)

for row in sales:
    print(f"{row[0]:<25} {row[1]:<12} {row[2]:<15} {row[3]:<16} ${row[4]:<14.2f}")

print(f"\nTotal Sale Items: {len(sales)}")

# Add timestamp at the bottom
report_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(f"\nReport generated on: {report_time}")

print("\n-------------------------------------------\n")

# -------------------------------------------
# CLEANUP
# -------------------------------------------
cursor.close()
db.close()

print("All Outland Adventures reports generated successfully.")
