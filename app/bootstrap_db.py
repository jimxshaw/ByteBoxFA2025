import psycopg2
import os

# Capture the environment variables within docker-compose.yml.
conn = psycopg2.connect(
    dbname=os.environ['POSTGRES_DB'],
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD'],
    host='db',  # This must match the service name in docker-compose.yml.
    port=5432
)

cur = conn.cursor()

# Check if the "customer" table exists.
# PostgreSQL automatically converts all table names to lowercase by default.
# E.g. ClimateControl becomes clitmatecontrol, Customer becomes customer.
cur.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' AND table_name = 'customer'
    );
""")
table_exists = cur.fetchone()[0]

if not table_exists:
    print("Customer table not found. Running create.sql + load.sql...")
    with open('create.sql', 'r') as f:
        cur.execute(f.read())
    with open('load.sql', 'r') as f:
        cur.execute(f.read())
    conn.commit()
else:
    # Check if customer table has data.
    cur.execute("SELECT COUNT(*) FROM customer;")
    count = cur.fetchone()[0]
    if count == 0:
        print("Customer table empty. Running load.sql only...")
        with open('load.sql', 'r') as f:
            cur.execute(f.read())
        conn.commit()
    else:
        print("Database and tables already initialized.")

cur.close()
conn.close()
