import psycopg2
from psycopg2 import sql

# Connect to the default 'postgres' database
conn = psycopg2.connect(
    dbname='p1db',
    user='Superuser',         # Change to your superuser if different
    password='abc@123',  # Replace with your actual password
    host='localhost',
    port='5432'
)
conn.autocommit = True  # Allow database creation without a transaction

cur = conn.cursor()

# Create a new database named 'mydatabase'
try:
    cur.execute(sql.SQL("CREATE DATABASE {}").format(
        sql.Identifier('mydatabase')
    ))
    print("Database 'mydatabase' created successfully!")
except Exception as e:
    print("Error creating database:", e)
finally:
    cur.close()
    conn.close()
 
