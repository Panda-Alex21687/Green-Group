CREATE TABLE EMPLOYEE (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    role VARCHAR(50),
    email VARCHAR(100)
);

CREATE TABLE REGION (
    region_id INT PRIMARY KEY,
    region_name VARCHAR(50)
);

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

CREATE TABLE CUSTOMER (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone VARCHAR(25),
    email VARCHAR(100)
);

CREATE TABLE BOOKING (
    booking_id INT PRIMARY KEY,
    customer_id INT,
    trip_id INT,
    booking_date DATE,
    FOREIGN KEY (customer_id) REFERENCES CUSTOMER(customer_id),
    FOREIGN KEY (trip_id) REFERENCES TRIP(trip_id)
);

CREATE TABLE EQUIPMENT (
    equipment_id INT PRIMARY KEY,
    item_name VARCHAR(100),
    item_type VARCHAR(50),
    condition VARCHAR(50),
    acquired_date DATE,
    quantity_on_hand INT,
    managed_by INT,
    FOREIGN KEY (managed_by) REFERENCES EMPLOYEE(employee_id)
);

CREATE TABLE EQUIPMENT_ORDER (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    order_type VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES CUSTOMER(customer_id)
);

CREATE TABLE ORDER_LINE (
    order_line_id INT PRIMARY KEY,
    order_id INT,
    equipment_id INT,
    quantity INT,
    price_each DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES EQUIPMENT_ORDER(order_id),
    FOREIGN KEY (equipment_id) REFERENCES EQUIPMENT(equipment_id)
);
