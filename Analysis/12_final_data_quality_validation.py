import pandas as pd

from sqlalchemy import create_engine, URL
from getpass import getpass

# MySQL Connection
password = getpass("Enter MySQL password: ")

connection_url = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password=password,
    host="localhost",
    port=3306,
    database="airline_passenger_analytics"
)

engine = create_engine(connection_url)

# Extract survey, booking and passenger data
df_surveys = pd.read_sql(
    "SELECT * FROM passenger_surveys", engine
)

df_bookings = pd.read_sql(
    "SELECT Booking_ID, Passenger_ID, Flight_ID, Travel_Class, Travel_Type FROM Bookings",
    engine
)

df_passengers = pd.read_sql(
    "SELECT Passenger_ID, Age, Gender FROM Passengers",
    engine
)

df_flights = pd.read_sql(
    "SELECT Flight_ID, Departure_Delay, Arrival_Delay FROM Flights",
    engine
)

# Merge datasets
df_final = df_surveys.merge(
    df_bookings,
    on="Booking_ID",
    how="left",
    validate="one_to_one"
)

df_final = df_final.merge(
    df_passengers,
    on="Passenger_ID",
    how="left",
    validate="many_to_one"
)

df_final = df_final.merge(
    df_flights,
    on="Flight_ID",
    how="left",
    validate="many_to_one"
)

# Final Data Quality Validation
print("\n========== FINAL DATA QUALITY REPORT ==========")

print("\nDataset Shape:")
print(df_final.shape)

print("\nMissing Values:")
print(df_final.isnull().sum())

print("\nDuplicate Records:")
print(df_final.duplicated().sum())

print("\nDuplicate Survey IDs:")
print(df_final["Survey_ID"].duplicated().sum())

print("\nUnique Booking IDs:")
print(df_final["Booking_ID"].nunique())

print("\nDataset Information:")
df_final.info()

engine.dispose()