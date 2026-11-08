
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from getpass import getpass

# ==========================================
# PYTHON - MYSQL CONNECTION TEST
# ==========================================

# Database configuration
host = "localhost"
port = 3306
database = "airline_passenger_analytics"

username = input("Enter MySQL username [root]: ").strip() or "root"
password = getpass("Enter MySQL password: ")

# Create database connection URL safely
connection_url = URL.create(
    drivername="mysql+pymysql",
    username=username,
    password=password,
    host=host,
    port=port,
    database=database
)

# Establish connection
try:
    engine = create_engine(
        connection_url,
        pool_pre_ping=True
    )

    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT DATABASE(), VERSION()")
        ).fetchone()

        print("\nMySQL connection successful!")

        print("Database:", result[0])
        print("MySQL Version:", result[1])

    engine.dispose()

except Exception as e:
    print("\nMySQL connection failed!")
    print("Error:", e)
