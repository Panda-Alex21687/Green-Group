import mysql.connector
import requests

# ----------------------------
# FETCH FILE FROM GITHUB
# ----------------------------
url = "https://raw.githubusercontent.com/Panda-Alex21687/Green-Group/main/Outland.data.py"
response = requests.get(url)

# ----------------------------
# CONNECT TO DATABASE
# ----------------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Gillmore21",
    database="outland"
)

cursor = db.cursor()

print("\n==============================")
print(" OUTLAND ADVENTURES REPORTS")
print("==============================\n")

# -------------------------------------------
# REPORT 1: EQUIPMENT OLDER THAN 5 YEARS
# -------------------------------------------
print("REPORT 1: Equipment Older Than 5 Years\n")

query_equipment_age = """
SELECT equipment_id, item_name, acquired_date,
       TIMESTAMPDIFF(YEAR, acquired_date, CURDATE()) AS age_years
FROM EQUIPMENT
WHERE acquired_date <= DATE_SUB(CURDATE(), INTERVAL 5 YEAR);
"""

cursor.execute(query_equipment_age)
rows = cursor.fetchall()

for row in rows:
    print(row)

print("\n-------------------------------------------\n")

# -------------------------------------------
# REPORT 2: BOOKINGS BY REGION
# -------------------------------------------
print("REPORT 2: Booking Trends by Region\n")

query_region_trends = """
SELECT r.region_name, COUNT(b.booking_id) AS total_bookings
FROM REGION r
LEFT JOIN TRIP t ON r.region_id = t.region_id
LEFT JOIN BOOKING b ON t.trip_id = b.trip_id
GROUP BY r.region_name
ORDER BY total_bookings DESC;
"""

cursor.execute(query_region_trends)
rows = cursor.fetchall()

for row in rows:
    print(row)

print("\n-------------------------------------------\n")

# -------------------------------------------
# REPORT 3: SALES VS RENTAL REVENUE
# -------------------------------------------
print("REPORT 3: Sales vs Rental Revenue\n")

query_sales_vs_rentals = """
SELECT order_type,
       SUM(ol.quantity * ol.price_each) AS total_revenue
FROM EQUIPMENT_ORDER eo
JOIN ORDER_LINE ol ON eo.order_id = ol.order_id
GROUP BY order_type;
"""

cursor.execute(query_sales_vs_rentals)
rows = cursor.fetchall()

for row in rows:
    print(row)

print("\n-------------------------------------------\n")

print("All reports generated!")
