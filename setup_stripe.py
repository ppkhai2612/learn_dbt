from faker import Faker
import random
import psycopg2


# Configs
NUM_ROWS = 5000

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "raw",
    "user": "khai",
    "password": "khai2612"
}

fake = Faker()
Faker.seed(42)
random.seed(42)

# Create table
def create_table(cur):

    cur.execute("""
        CREATE SCHEMA IF NOT EXISTS stripe;
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS stripe.payment (
            id INTEGER,
            orderid INTEGER,
            paymentmethod TEXT,
            status TEXT,
            amount NUMERIC(10, 2),
            created TIMESTAMP
        );
    """)

# Generate data
def generate_data(n):
    payment_methods = ["card", "bank_transfer", "wallet"]
    statuses = ["pending", "completed", "failed", "refunded"]

    data = []
    for i in range(1, n + 1):
        data.append((
            i,
            random.randint(1, 2000),  # orderid
            random.choice(payment_methods),
            random.choices(
                statuses,
                weights=[0.1, 0.7, 0.1, 0.1],  # skew realistic
                k=1
            )[0],
            round(random.uniform(5, 500), 2),  # amount
            fake.date_time_between(start_date="-1y", end_date="now")
        ))
    return data

# Insert data
def insert_data(cur):

    try:
        data = generate_data(NUM_ROWS)
        cur.execute("TRUNCATE stripe.payment;")
        query = """
            INSERT INTO stripe.payment
            (id, orderid, paymentmethod, status, amount, created)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cur.executemany(query, data)
        
        conn.commit()
        print("Data inserted successfully")

    except Exception as e:
        conn.rollback()
        print(f"Error:", {e})

    finally:
        cur.close()
        conn.close()

    
if __name__ == "__main__":

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    create_table(cur)
    insert_data(cur)
