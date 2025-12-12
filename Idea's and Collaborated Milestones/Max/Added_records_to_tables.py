# Green team Milestone 2 Python code - ENHANCED VERSION with Repeat Customers
# Alexander Baldree
# Jordan Dardar
# Maksymilian Jankowski
# Aftabur Rahman
# Editedd my Max on 12-10-25 for more robust reports 

import mysql.connector
import requests

# ----------------------------
# FETCH FILE FROM GITHUB
# ----------------------------
url = "https://raw.githubusercontent.com/Panda-Alex21687/Green-Group/main/Outland.data.py"
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
    password="jess1234",     
    database="outland"
)

cursor = db.cursor()

# ----------------------------
# DROP TABLES IF THEY EXIST # deleting any existing databse with the same name
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
    price DECIMAL(10,2),              -- *** ADDED: price field for revenue analysis
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

cursor.executemany("""
INSERT INTO EMPLOYEE VALUES (%s, %s, %s, %s, %s)
""", [
    # --- ORIGINAL 6 EMPLOYEES (unchanged) ---
    (1, "John", "MacNell", "Guide", "mac@outland.com"),
    (2, "Duke", "Marland", "Guide", "duke@outland.com"),
    (3, "Anita", "Gallegos", "Marketing", "anita@outland.com"),
    (4, "Dimitrios", "Stravopolous", "Inventory", "dimitrios@outland.com"),
    (5, "Mei", "Wong", "Web Dev", "mei@outland.com"),
    (6, "Jim", "Ford", "Admin", "jim@outland.com")
])

# ============================================================
# REGION - ORIGINAL: 6 | ENHANCED: 6 (no change)
# ============================================================
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

# ============================================================
# TRIP - ORIGINAL: 6 Added 9 to improve reports
# ============================================================
cursor.executemany("""
INSERT INTO TRIP VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
""", [
    # OG 6 TRIPS 
    (1, "Safari Trek", 1, 1, "2025-03-15", "2025-03-22", 2500.00, True, True),
    (2, "Kilimanjaro Ascent", 1, 2, "2025-05-10", "2025-05-20", 3000.00, True, True),
    (3, "Mediterranean Walk", 3, 1, "2025-04-15", "2025-04-22", 2400.00, False, False),  # *** RENAMED & PRICED
    (4, "Desert Crossing", 1, 2, "2025-08-09", "2025-08-20", 2200.00, False, True),     # *** MOVED TO AFRICA, PRICED
    (5, "Island Climb", 3, 1, "2025-09-12", "2025-09-25", 2800.00, False, False),       # *** PRICED
    (6, "Volcano Route", 2, 2, "2025-07-02", "2025-07-14", 1900.00, True, False),       # *** PRICED
    
    # Africa added 1
    (7, "Victoria Falls Adventure", 1, 1, "2025-07-05", "2025-07-12", 2200.00, True, True),
    
    # Asia added 2
    (8, "Great Wall Trek", 2, 2, "2025-04-10", "2025-04-17", 2200.00, True, True),
    (9, "Mount Fuji Expedition", 2, 1, "2025-06-05", "2025-06-12", 2800.00, True, False),
    
    # Southern Europe added 2
    (10, "Alpine Climb", 3, 2, "2025-07-15", "2025-07-22", 2600.00, False, False),
    (11, "Greek Islands Tour", 3, 1, "2025-09-10", "2025-09-17", 2400.00, False, False),
    
    # South America added 3
    (12, "Machu Picchu Trek", 4, 1, "2025-06-20", "2025-06-28", 2700.00, True, True),
    (13, "Amazon Rainforest", 4, 2, "2025-07-25", "2025-08-02", 2900.00, True, True),
    (14, "Patagonia Hiking", 4, 1, "2025-10-05", "2025-10-14", 3100.00, False, False),
    
    # 1 added in North America 
    (15, "Grand Canyon Trek", 5, 2, "2025-05-15", "2025-05-22", 1800.00, False, False)
])

# Custmers added 11 Some ith repeat adventures 
cursor.executemany("""
INSERT INTO CUSTOMER VALUES (%s, %s, %s, %s, %s)
""", [
    # Og 6 customers
    (1, "Alex", "Baldree", "555-1234", "alex@example.com"),       
    (2, "Sarah", "Knight", "555-5678", "sarah@example.com"),      
    (3, "David", "Lee", "555-2233", "david@example.com"),         
    (4, "Emma", "Stone", "555-9988", "emma@example.com"),          
    (5, "Liam", "Wong", "555-4433", "liam@example.com"),           
    (6, "Mia", "Torres", "555-1122", "mia@example.com"),           
    
   # added more cust, some with repeat trips
    (7, "Oliver", "Brown", "555-3344", "oliver@example.com"),     
    (8, "Sophia", "Davis", "555-7788", "sophia@example.com"),    
    (9, "Noah", "Garcia", "555-9900", "noah@example.com"),        
    (10, "Isabella", "Miller", "555-2211", "isabella@example.com"),
    (11, "Ethan", "Wilson", "555-6677", "ethan@example.com"),     
    (12, "Ava", "Moore", "555-8899", "ava@example.com"),         
    (13, "Mason", "Taylor", "555-4455", "mason@example.com"),     
    (14, "Charlotte", "Anderson", "555-3366", "charlotte@example.com"), 
    (15, "Logan", "Thomas", "555-5544", "logan@example.com"),     
    (16, "Amelia", "Jackson", "555-7799", "amelia@example.com"),   
    (17, "Lucas", "White", "555-1100", "lucas@example.com")        
])

# Bookings
# Added 26 more bookings 
cursor.executemany("""
INSERT INTO BOOKING VALUES (%s, %s, %s, %s)
""", [
  
    (1, 1, 1, "2024-12-01"),      
    (2, 2, 8, "2024-12-10"),      
    (3, 3, 10, "2025-01-05"),     
    (4, 4, 1, "2025-01-08"),      
    (5, 5, 12, "2025-01-12"),     
    (6, 6, 15, "2025-01-18"),  
    (7, 1, 2, "2025-01-15"),         
    (8, 1, 7, "2025-02-10"),   
    (9, 1, 12, "2025-03-05"),    
    (10, 2, 9, "2025-01-20"),     
    (11, 2, 6, "2025-02-15"),     
    (12, 2, 10, "2025-03-10"),     
    (13, 3, 3, "2025-02-01"),
    (14, 3, 11, "2025-02-25"),     
    (15, 4, 12, "2025-02-05"),    
    (16, 4, 13, "2025-02-28"),    
    (17, 5, 14, "2025-02-20"),   
    (18, 6, 15, "2025-02-22"),    
    (19, 7, 8, "2025-01-22"),   
    (20, 7, 4, "2025-03-15"),     
    (21, 8, 2, "2025-01-25"),     
    (22, 8, 9, "2025-03-01"),    
    (23, 9, 3, "2025-02-08"),    
    (24, 9, 10, "2025-03-22"),    
    (25, 10, 7, "2025-02-12"),  
    (26, 11, 13, "2025-02-18"),   
    (27, 12, 14, "2025-03-08"),   
    (28, 13, 15, "2025-02-28"),  
    (29, 14, 6, "2025-03-02"),   
    (30, 15, 5, "2025-03-12"),   
    (31, 16, 11, "2025-03-18"),   
    (32, 17, 4, "2025-03-20")     
])

# EQUIPMENT - added 9 items

cursor.executemany("""
INSERT INTO EQUIPMENT VALUES (%s, %s, %s, %s, %s, %s, %s)
""", [
    # --- ORIGINAL 6 ITEMS ---
    (1, "Tent", "Rental", "Good", "2021-01-10", 15, 4),
    (2, "Backpack", "Sale", "New", "2023-05-12", 40, 4),
    (3, "Hiking Boots", "Sale", "New", "2024-01-15", 20, 4),
    (4, "Lantern", "Rental", "Fair", "2020-03-22", 12, 4),
    (5, "Climbing Rope", "Sale", "Good", "2022-11-05", 25, 4),
    (6, "Sleeping Bag", "Rental", "Good", "2021-07-19", 18, 4),
    # added 9
    (7, "4-Person Tent", "Rental", "Good", "2018-05-10", 8, 4),    
    (8, "Water Filter", "Sale", "New", "2024-02-10", 40, 4),
    (9, "Trekking Poles", "Rental", "Good", "2021-09-15", 18, 4),
    (10, "Headlamp", "Sale", "New", "2024-01-05", 50, 4),
    (11, "Rain Jacket", "Rental", "Good", "2022-06-05", 20, 4),
    (12, "Camp Stove", "Rental", "Fair", "2019-04-12", 10, 4),    
    (13, "GPS Device", "Rental", "Excellent", "2023-03-10", 8, 4),
    (14, "First Aid Kit", "Sale", "New", "2024-04-01", 35, 4),
    (15, "Insulated Jacket", "Rental", "Good", "2020-10-05", 14, 4)
])

# EQUIPMENT_ORDER - had 6 I added 22

cursor.executemany("""
INSERT INTO EQUIPMENT_ORDER VALUES (%s, %s, %s, %s)
""", [
    #OG 6
    (1, 1, "2025-01-05", "RENTAL"),
    (2, 2, "2025-02-01", "SALE"),
    (3, 3, "2025-02-10", "SALE"),
    (4, 4, "2025-03-01", "RENTAL"),
    (5, 5, "2025-03-05", "SALE"),
    (6, 6, "2025-03-12", "RENTAL"),
    
    # *** ADDED: 22 NEW ORDERS - VIP CUSTOMERS ORDER MULTIPLE TIMES ***
    # VIP customers Alex & Sarah order equipment for each trip
    (7, 1, "2024-11-28", "RENTAL"),   # Alex - before Safari
    (8, 1, "2025-01-10", "SALE"),     # Alex - buying own gear
    (9, 1, "2025-02-05", "RENTAL"),   # Alex - Victoria Falls
    (10, 1, "2025-03-01", "RENTAL"),  # Alex - Machu Picchu
    (11, 2, "2024-12-05", "RENTAL"),  # Sarah - Great Wall
    (12, 2, "2025-01-15", "RENTAL"),  # Sarah - Mount Fuji
    (13, 2, "2025-02-10", "SALE"),    # Sarah - buying gear
    (14, 2, "2025-03-05", "RENTAL"),  # Sarah - Alpine
    
    # Repeat customers order 1-2 times
    (15, 3, "2025-01-02", "RENTAL"),  # David
    (16, 3, "2025-01-28", "RENTAL"),  # David again
    (17, 4, "2025-01-05", "SALE"),    # Emma
    (18, 4, "2025-02-01", "RENTAL"),  # Emma
    (19, 5, "2025-01-08", "RENTAL"),  # Liam
    (20, 5, "2025-02-15", "RENTAL"),  # Liam again
    (21, 6, "2025-01-15", "SALE"),    # Mia
    (22, 7, "2025-01-20", "RENTAL"),  # Oliver
    (23, 8, "2025-01-22", "SALE"),    # Sophia
    (24, 9, "2025-02-05", "RENTAL"),  # Noah
    (25, 9, "2025-03-18", "SALE"),    # Noah - buying gear (converted!)
    
    # One-time customers
    (26, 10, "2025-02-10", "RENTAL"), # Isabella
    (27, 11, "2025-02-15", "SALE"),   # Ethan
    (28, 12, "2025-03-05", "RENTAL")  # Ava
])


# ORDER_LINE had 6 added 44

cursor.executemany("""
INSERT INTO ORDER_LINE VALUES (%s, %s, %s, %s, %s)
""", [
    # og 6
    (1, 1, 1, 1, 25.00),
    (2, 2, 2, 1, 60.00),
    (3, 3, 3, 1, 90.00),
    (4, 4, 4, 2, 10.00),
    (5, 5, 5, 1, 120.00),
    (6, 6, 6, 1, 30.00),
    
    # 44 added
    (7, 7, 7, 1, 40.00),
    (8, 7, 11, 1, 20.00),
    (9, 8, 3, 2, 75.00),
    (10, 8, 2, 1, 120.00),
    (11, 8, 10, 2, 25.00),
    (12, 8, 8, 1, 35.00),
    (13, 9, 6, 1, 30.00),
    (14, 9, 15, 1, 35.00),
    (15, 10, 9, 1, 15.00),
    (16, 10, 13, 1, 50.00),
    (17, 11, 9, 2, 15.00),
    (18, 11, 6, 1, 30.00),
    (19, 12, 6, 1, 30.00),
    (20, 12, 13, 1, 50.00),
    (21, 13, 3, 1, 75.00),
    (22, 13, 10, 1, 25.00),
    (23, 13, 14, 1, 45.00),
    (24, 14, 15, 1, 35.00),
    (25, 15, 1, 1, 40.00),
    (26, 15, 4, 1, 10.00),
    (27, 16, 11, 1, 20.00),
    (28, 16, 9, 1, 15.00),
    (29, 17, 2, 1, 120.00),
    (30, 17, 8, 1, 35.00),
    (31, 18, 1, 1, 40.00),
    (32, 18, 6, 1, 30.00),
    (33, 19, 6, 2, 30.00),
    (34, 19, 9, 1, 15.00),
    (35, 20, 6, 1, 30.00),
    (36, 20, 15, 1, 35.00),
    (37, 21, 3, 1, 75.00),
    (38, 21, 14, 1, 45.00),
    (39, 22, 4, 1, 10.00),
    (40, 23, 3, 2, 75.00),
    (41, 23, 10, 1, 25.00),
    (42, 24, 11, 1, 20.00),
    (43, 25, 2, 1, 120.00),
    (44, 25, 10, 1, 25.00),
    (45, 26, 1, 1, 40.00),
    (46, 27, 2, 1, 120.00),
    (47, 27, 8, 2, 35.00),
    (48, 28, 6, 1, 30.00),
    (49, 28, 9, 1, 15.00),
    (50, 8, 14, 1, 45.00)
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

print("\nAll data displayed!")
