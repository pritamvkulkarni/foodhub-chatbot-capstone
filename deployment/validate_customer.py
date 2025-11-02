
import re
import sqlite3 

# --- Validate customer ID using direct SQL ---
def is_valid_customer(customer_id: str) -> bool:

    try:
        # Connect to your database
        conn = sqlite3.connect("customer_orders.db")  # Replace with your actual DB connection
        cursor = conn.cursor()

        # Run a simple query to check existence
        cursor.execute("SELECT 1 FROM orders WHERE cust_id = ?", (customer_id,))
        result = cursor.fetchone()

        conn.close()
        return result is not None

    except Exception as e:
        print(f"Database error: {e}")
        return True
