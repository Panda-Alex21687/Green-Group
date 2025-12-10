# report1_equipment_over_5_years_jordan.py
"""
Report 1: Equipment Older Than Five Years
Author: Jordan Dardar

This report checks the EQUIPMENT table and lists any items that are
more than five years old based on their acquired_date.
"""

from db_connection_jordan import get_connection

def report_equipment_older_than_five_years():
    cnx = get_connection()
    if cnx is None:
        return

    cursor = cnx.cursor()

    query = """
        SELECT
            equipment_id,
            item_name,
            item_type,
            item_condition,
            acquired_date,
            TIMESTAMPDIFF(YEAR, acquired_date, CURDATE()) AS age_years
        FROM EQUIPMENT
        WHERE TIMESTAMPDIFF(YEAR, acquired_date, CURDATE()) > 5
        ORDER BY age_years DESC, item_name;
    """

    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        print("REPORT 1: Equipment Older Than 5 Years")
        print("-" * 60)

        if not rows:
            print("No equipment items are older than five years.")
        else:
            for row in rows:
                (equipment_id, name, item_type,
                 condition, acquired_date, age_years) = row
                print(
                    f"ID: {equipment_id}, "
                    f"Name: {name}, "
                    f"Type: {item_type}, "
                    f"Condition: {condition}, "
                    f"Acquired: {acquired_date}, "
                    f"Age: {age_years} years"
                )

    except Exception as e:
        print("Error running report:", e)
    finally:
        cursor.close()
        cnx.close()

if __name__ == "__main__":
    report_equipment_older_than_five_years()
