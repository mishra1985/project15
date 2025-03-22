import psycopg2
from psycopg2 import sql
import os
# Connect to the default 'postgres' database
conn = psycopg2.connect(
    dbname=os.environ.get('DB_NAME'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'),
    host=os.environ.get('DB_HOST'),
    port=os.environ.get('DB_PORT')
)
DB_NAME=p1db
DB_USER=p1db_user
DB_PASSWORD=FOyeuq6lS88Ch24DbNNYiscUEXEeDvJj
DB_HOST=dpg-cvfil75ds78s73fm8t6g-a
DB_PORT=5432
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
 
