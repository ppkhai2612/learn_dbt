from faker import Faker
import random
import psycopg2
from datetime import datetime, timezone

# Configs
NUM_CUSTOMERS = 1000
NUM_ORDERS = 5000

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "raw",
    "user": "khai",
    "password": "khai2612" # replace with your own passowrd
}

fake = Faker()
# Ensure deterministic random data across reruns
Faker.seed(42)
random.seed(42)

# Generate customers
def generate_customers(n):
    customers = []
    for i in range(1, n + 1):
        customers.append((
            i,
            fake.first_name(),
            fake.last_name()
        ))
    return customers

# Generate orders
def generate_orders(n, customer_ids):
    statuses = ["placed", "shipped", "completed", "returned", "return_pending"]
    load_time = datetime.now(timezone.utc)
    orders = []

    for i in range(1, n + 1):
        orders.append((
            i,
            random.choice(customer_ids),
            fake.date_between(start_date="-1y", end_date="today"),
            random.choices(
                statuses,
                weights=[0.1, 0.2, 0.65, 0.03, 0.02], # skew realistic
                k=1
            )[0],
            load_time
        ))
    return orders

# Insert data into Postgres
def insert_data(cur):

    try:
        # Generate data
        customers = generate_customers(NUM_CUSTOMERS)
        customer_ids = [c[0] for c in customers]
        orders = generate_orders(NUM_ORDERS, customer_ids)

        # Clear old data
        cur.execute("""
            TRUNCATE jaffle_shop.orders,
                    jaffle_shop.customers
            CASCADE
        """)

        # Insert customers
        cur.executemany("""
            INSERT INTO jaffle_shop.customers (id, first_name, last_name)
            VALUES (%s, %s, %s)
        """, customers)

        # Insert orders
        cur.executemany("""
            INSERT INTO jaffle_shop.orders (id, user_id, order_date, status, _etl_loaded_at)
            VALUES (%s, %s, %s, %s, %s)
        """, orders)

        conn.commit()
        print("Data inserted successfully")

    except Exception as e:
        conn.rollback()
        print(f"Error:", {e})

    finally:
        cur.close()
        conn.close()

# Create tables
def create_table(cur):

    cur.execute("""
        CREATE SCHEMA IF NOT EXISTS jaffle_shop;
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS jaffle_shop.customers (
            id INTEGER,
            first_name TEXT,
            last_name TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS jaffle_shop.orders (
            id INTEGER,
            user_id INTEGER,
            order_date DATE,
            status TEXT,
            _etl_loaded_at TIMESTAMPTZ
        );
    """)


if __name__ == "__main__":

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    create_table(cur)
    insert_data(cur)