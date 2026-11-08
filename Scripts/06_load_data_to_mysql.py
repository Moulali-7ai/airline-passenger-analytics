
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from getpass import getpass
import os

# ==========================================
# AIRLINE ANALYTICS - ETL DATA LOADING
# ==========================================

print("AIRLINE PASSENGER ANALYTICS")
print("ETL PROCESS STARTED")

# Database configuration
username = input("MySQL Username [root]: ").strip() or "root"
password = getpass("MySQL Password: ")

connection_url = URL.create(
    drivername="mysql+pymysql",
    username=username,
    password=password,
    host="localhost",
    port=3306,
    database="airline_passenger_analytics"
)

engine = create_engine(
    connection_url,
    pool_pre_ping=True
)

# Dataset configuration
datasets = {
    "Airport": "airports.csv",
    "Passengers": "passengers.csv",
    "Flights": "flights.csv",
    "Bookings": "bookings.csv",
    "passenger_surveys": "passenger_surveys.csv"
}

raw_path = "data/raw"

try:
    with engine.connect() as connection:

        # Check whether tables already contain records
        total_existing = 0

        for table in datasets:
            count = connection.execute(
                text(f"SELECT COUNT(*) FROM `{table}`")
            ).scalar_one()

            total_existing += count

        if total_existing > 0:
            raise RuntimeError(
                "Tables already contain records. "
                "Stopping to prevent duplicate insertion."
            )

    # Load datasets in foreign-key order
    for table, filename in datasets.items():

        file_path = os.path.join(raw_path, filename)

        print(f"\nLoading: {table}")

        df = pd.read_csv(file_path)

        # Convert date columns
        if table == "Flights":
            date_columns = [
                "Scheduled_Departure",
                "Scheduled_Arrival",
                "Actual_Departure",
                "Actual_Arrival"
            ]

            for column in date_columns:
                df[column] = pd.to_datetime(
                    df[column],
                    errors="raise"
                )

        elif table == "Bookings":
            df["Booking_Date"] = pd.to_datetime(
                df["Booking_Date"],
                errors="raise"
            )

            df["Travel_Date"] = pd.to_datetime(
                df["Travel_Date"],
                errors="raise"
            )

        # Insert records
        df.to_sql(
            name=table,
            con=engine,
            if_exists="append",
            index=False,
            chunksize=1000,
            method="multi"
        )

        print(f"Successfully loaded {len(df)} records")

    print("\nETL DATA LOADING COMPLETED!")

except Exception as e:
    print("\nETL PROCESS FAILED!")
    print("Error:", e)

finally:
    engine.dispose()
