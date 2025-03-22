import psycopg2
from psycopg2 import sql
import os
# Connect to the default 'postgres' database
conn = psycopg2.connect(
    dbname=os.environ.get('DB_NAME', 'p1db'),
    user=os.environ.get('DB_USER', 'Superuser'),
    password=os.environ.get('DB_PASSWORD', 'abc@123'),
    host=os.environ.get('DB_HOST', 'localhost'),
    port=os.environ.get('DB_PORT', '5432')
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
 
