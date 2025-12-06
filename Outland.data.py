import mysql.connector
import requests

# ----------------------------
# FETCH FILE FROM GITHUB
# ----------------------------
url = "https://raw.githubusercontent.com/Panda-Alex21687/Green-Group/main/module-9/Outland.data.py"
response = requests.get(url)

print("\n--- GITHUB FETCH STATUS ---")
if response.status_code == 200:
    print("GitHub file downloaded successfully!\n")
    content = response.text
    print(content)
else:
    print("Error fetching GitHub file:", response.status_code)

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

# ----------------------------
# DROP TABLES IF THEY EXIST
# ----------------------------
drop_order = [
    "ORDER_LINE",
    "EQUIPMENT_ORDER",
    "EQUIPMENT",
    "BOOKING",
    "TRIP",
    "CUSTOMER",
    "REGION",
    "EMPLOYEE"
]

for table in drop_order:
    cursor.execute(f"DROP TABLE IF EXISTS {table}")

print("Old tables dropped (if existed).")

# ----------------------------
# CREATE TABLES
# ----------------------------
tables = [

"""
CREATE TABLE EMPLOYEE (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    role VARCHAR(50),
    email VARCHAR(100)
);
""",

"""
CREATE TABLE REGION (
    region_id INT PRIMARY KEY,
    region_name VARCHAR(50)
);
""",

"""
CREATE TABLE TRIP (
    trip_id INT PRIMARY KEY,
    trip_name VARCHAR(100),
    region_id INT,
    guide_id INT,
    start_date DATE,
    end_date DATE,
    visa_required BOOLEAN,
    inoculations_required BOOLEAN,
    FOREIGN KEY (region_id) REFERENCES REGION(region_id),
    FOREIGN KEY (guide_id) REFERENCES EMPLOYEE(employee_id)
);
""",

"""
CREATE TABLE CUSTOMER (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone VARCHAR(25),
    email VARCHAR(100)
);
""",

"""
CREATE TABLE BOOKING (
    booking_id INT PRIMARY KEY,
    customer_id INT,
    trip_id INT,
    booking_date DATE,
    FOREIGN KEY (customer_id) REFERENCES CUSTOMER(customer_id),
    FOREIGN KEY (trip_id) REFERENCES TRIP(trip_id)
);
""",

"""
CREATE TABLE EQUIPMENT (
    equipment_id INT PRIMARY KEY,
    item_name VARCHAR(100),
    item_type VARCHAR(50),
    item_condition VARCHAR(50),
    acquired_date DATE,
    quantity_on_hand INT,
    managed_by INT,
    FOREIGN KEY (managed_by) REFERENCES EMPLOYEE(employee_id)
);
""",

"""
CREATE TABLE EQUIPMENT_ORDER (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    order_type VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES CUSTOMER(customer_id)
);
""",

"""
CREATE TABLE ORDER_LINE (
    order_line_id INT PRIMARY KEY,
    order_id INT,
    equipment_id INT,
    quantity INT,
    price_each DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES EQUIPMENT_ORDER(order_id),
    FOREIGN KEY (equipment_id) REFERENCES EQUIPMENT(equipment_id)
);
"""
]

for t in tables:
    cursor.execute(t)

db.commit()
print("Tables created successfully!")

# ----------------------------
# Data Insertion
# ----------------------------

# EMPLOYEE
cursor.executemany("""
INSERT INTO EMPLOYEE VALUES (%s, %s, %s, %s, %s)
""", [
    (1, "John", "MacNell", "Guide", "mac@outland.com"),
    (2, "Duke", "Marland", "Guide", "duke@outland.com"),
    (3, "Anita", "Gallegos", "Marketing", "anita@outland.com"),
    (4, "Dimitrios", "Stravopolous", "Inventory", "dimitrios@outland.com"),
    (5, "Mei", "Wong", "Web Dev", "mei@outland.com"),
    (6, "Jim", "Ford", "Admin", "jim@outland.com")
])

# REGION
cursor.executemany("""
INSERT INTO REGION VALUES (%s, %s)
""", [
    (1, "Africa"),
    (2, "Asia"),
    (3, "Southern Europe"),
    (4, "South America"),
    (5, "North America"),
    (6, "Middle East")
])

# TRIP
cursor.executemany("""
INSERT INTO TRIP VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""", [
    (1, "Safari Trek", 1, 1, "2025-05-10", "2025-05-20", True, True),
    (2, "Himalayan Hike", 2, 2, "2025-06-01", "2025-06-10", True, True),
    (3, "Mediterranean Walk", 3, 1, "2025-04-15", "2025-04-22", False, False),
    (4, "Desert Crossing", 1, 2, "2025-08-09", "2025-08-20", False, True),
    (5, "Island Climb", 3, 1, "2025-09-12", "2025-09-25", False, False),
    (6, "Volcano Route", 2, 2, "2025-07-02", "2025-07-14", True, False)
])

# CUSTOMER
cursor.executemany("""
INSERT INTO CUSTOMER VALUES (%s, %s, %s, %s, %s)
""", [
    (1, "Alex", "Baldree", "555-1234", "alex@example.com"),
    (2, "Sarah", "Knight", "555-5678", "sarah@example.com"),
    (3, "David", "Lee", "555-2233", "david@example.com"),
    (4, "Emma", "Stone", "555-9988", "emma@example.com"),
    (5, "Liam", "Wong", "555-4433", "liam@example.com"),
    (6, "Mia", "Torres", "555-1122", "mia@example.com")
])

# BOOKING
cursor.executemany("""
INSERT INTO BOOKING VALUES (%s, %s, %s, %s)
""", [
    (1, 1, 1, "2025-01-01"),
    (2, 2, 2, "2025-01-10"),
    (3, 3, 3, "2025-02-01"),
    (4, 4, 1, "2025-02-15"),
    (5, 5, 5, "2025-03-01"),
    (6, 6, 4, "2025-03-08")
])

# EQUIPMENT
cursor.executemany("""
INSERT INTO EQUIPMENT VALUES (%s, %s, %s, %s, %s, %s, %s)
""", [
    (1, "Tent", "Rental", "Good", "2021-01-10", 15, 4),
    (2, "Backpack", "Sale", "New", "2023-05-12", 40, 4),
    (3, "Hiking Boots", "Sale", "New", "2024-01-15", 20, 4),
    (4, "Lantern", "Rental", "Fair", "2020-03-22", 12, 4),
    (5, "Climbing Rope", "Sale", "Good", "2022-11-05", 25, 4),
    (6, "Sleeping Bag", "Rental", "Good", "2021-07-19", 18, 4)
])

# EQUIPMENT_ORDER
cursor.executemany("""
INSERT INTO EQUIPMENT_ORDER VALUES (%s, %s, %s, %s)
""", [
    (1, 1, "2025-01-05", "RENTAL"),
    (2, 2, "2025-02-01", "SALE"),
    (3, 3, "2025-02-10", "SALE"),
    (4, 4, "2025-03-01", "RENTAL"),
    (5, 5, "2025-03-05", "SALE"),
    (6, 6, "2025-03-12", "RENTAL")
])

# ORDER_LINE
cursor.executemany("""
INSERT INTO ORDER_LINE VALUES (%s, %s, %s, %s, %s)
""", [
    (1, 1, 1, 1, 25.00),
    (2, 2, 2, 1, 60.00),
    (3, 3, 3, 1, 90.00),
    (4, 4, 4, 2, 10.00),
    (5, 5, 5, 1, 120.00),
    (6, 6, 6, 1, 30.00)
])

db.commit()
print("All sample records inserted!")

# ----------------------------
# DISPLAY ALL TABLE DATA
# ----------------------------
tables = [
    "EMPLOYEE",
    "REGION",
    "TRIP",
    "CUSTOMER",
    "BOOKING",
    "EQUIPMENT",
    "EQUIPMENT_ORDER",
    "ORDER_LINE"
]

print("\n---------------------------")
print("DISPLAYING OUTLAND DATA")
print("---------------------------")

for table in tables:
    print(f"\n--- {table} ---")
    cursor.execute(f"SELECT * FROM {table}")
    for row in cursor.fetchall():
        print(row)

print("\nAll data displayed. Take your screenshots now!")
