# db_connection_jordan.py
"""
Database connection helper for Outland Adventures
Author: Jordan Dardar
"""

import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="addimae69",
            database="outland"
        )
        return connection
    except Error as e:
        print("Error connecting to MySQL:", e)
        return None
