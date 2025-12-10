import mysql.connector

# ----------------------------
# CONNECT TO DATABASE
# ----------------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="jess1234",
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

# -------------------------------------------
# REPORT 4: GUIDE ASSIGNMENT REPORT
# -------------------------------------------
print("REPORT 4: Guide Assignment Report\n")

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

for row in rows:
    print(row)

print("\n-------------------------------------------\n")

# -------------------------------------------
# REPORT 5: EQUIPMENT ORDER FREQUENCY
# -------------------------------------------
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

for row in rows:
    print(row)

print("\n-------------------------------------------\n")



print("All reports generated!")
