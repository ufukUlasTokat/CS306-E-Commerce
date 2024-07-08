import mysql.connector
from faker import Faker
import random
from connect import create_connection
from mysql.connector import Error

# Function to execute a query
def execute_query(connection, query, data=None):
    cursor = connection.cursor()
    try:
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        print(data)
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()

def get_customer_ids(connection):
    query = "SELECT id FROM customer"
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        customer_ids = [row[0] for row in cursor.fetchall()]  # Fetch and store the results
        return customer_ids
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()

# Delete Operation
def delete(connection, table_name):
    # Write a function to delete a student with given id
    query = f"DELETE FROM {table_name}"
    execute_query(connection, query)

# Connect to your MySQL server
connection = create_connection()

# Create a cursor object
cursor = connection.cursor()

# Create a Faker instance
fake = Faker()

# Number of records to generate
num_records = 1000000


# Generate and insert data
for _ in range(num_records):
    name = fake.first_name()
    surname = fake.last_name()
    email = fake.email()
    age = random.randint(18, 99)
    phone = fake.phone_number()
    balance = random.randint(0, 100)

    execute_query(connection,
        """
        INSERT INTO customer (name, surname, age ,phone, email, balance)
        VALUES (%s, %s, %s, %s, %s, %s)
    """,
        (name, surname, age ,phone, email, balance),
    )

customer_ids = get_customer_ids(connection)

# Generate and insert data
for _ in range(num_records):
    product_id = random.randint(1,10)
    customer_id = random.choice(customer_ids)
    comment = fake.text()
    point = random.randint(0,5)

    execute_query(connection,
        """
        INSERT INTO comments (product_id, customer_id, comment, point)
        VALUES (%s, %s, %s, %s)
    """,
        (product_id, customer_id, comment, point),
    )


# Commit the changes
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()

print("finished")