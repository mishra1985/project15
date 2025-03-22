import psycopg2
from psycopg2 import sql
import os
# Connect to the default 'postgres' database
conn = psycopg2.connect(
    dbname=os.environ.get('GENERATIVE_AI_API_KEY'),
    user=os.environ.get('GENERATIVE_AI_API_KEY'),
    password=os.environ.get('GENERATIVE_AI_API_KEY'),
    host=os.environ.get('GENERATIVE_AI_API_KEY'),
    port=os.environ.get('GENERATIVE_AI_API_KEY')
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
 
