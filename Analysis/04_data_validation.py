import pandas as pd
import numpy as np

# Load all datasets

df_airports = pd.read_csv("data/raw/airports.csv")

df_passengers = pd.read_csv("data/raw/passengers.csv")

df_flights = pd.read_csv("data/raw/flights.csv")

df_bookings = pd.read_csv("data/raw/bookings.csv")

df_surveys = pd.read_csv("data/raw/passenger_surveys.csv")

print("All datasets loaded successfully!")

## Check dataset dimensions

print("\nDATASET DIMENSIONS")

print("Airports:", df_airports.shape)
print("Passengers:", df_passengers.shape)
print("Flights:", df_flights.shape)
print("Bookings:", df_bookings.shape)
print("Surveys:", df_surveys.shape)

## Missing-value analysis....This identifies missing values in every column.

datasets = {
    "Airports": df_airports,
    "Passengers": df_passengers,
    "Flights": df_flights,
    "Bookings": df_bookings,
    "Surveys": df_surveys
}

for name, df in datasets.items():

    print(f"\n{name} DATASET")

    print(df.isnull().sum())

## Duplicate analysis

print("Airport duplicates:",
      df_airports["Airport_ID"].duplicated().sum())

print("Passenger duplicates:",
      df_passengers["Passenger_ID"].duplicated().sum())

print("Flight duplicates:",
      df_flights["Flight_ID"].duplicated().sum())

print("Booking duplicates:",
      df_bookings["Booking_ID"].duplicated().sum())

print("Survey duplicates:",
      df_surveys["Survey_ID"].duplicated().sum())

print("Duplicate survey bookings:",
      df_surveys["Booking_ID"].duplicated().sum())

## Referential integrity validation ......This is particularly important because we designed a relational database.

# Validate airport references in flights

print("Invalid origin airports:",
      (~df_flights["Origin_Airport_ID"].isin(
          df_airports["Airport_ID"]
      )).sum())

print("Invalid destination airports:",
      (~df_flights["Destination_Airport_ID"].isin(
          df_airports["Airport_ID"]
      )).sum())


# Validate passenger references in bookings

print("Invalid passenger references:",
      (~df_bookings["Passenger_ID"].isin(
          df_passengers["Passenger_ID"]
      )).sum())


# Validate flight references in bookings

print("Invalid flight references:",
      (~df_bookings["Flight_ID"].isin(
          df_flights["Flight_ID"]
      )).sum())


# Validate booking references in surveys

print("Invalid booking references:",
      (~df_surveys["Booking_ID"].isin(
          df_bookings["Booking_ID"]
      )).sum())



## Business rule validation

# Passenger age validation

print("Invalid passenger ages:",
      ((df_passengers["Age"] < 0) |
       (df_passengers["Age"] > 120)).sum())


# Flight route validation

print("Invalid flight routes:",
      (df_flights["Origin_Airport_ID"] ==
       df_flights["Destination_Airport_ID"]).sum())


# Booking date validation

df_bookings["Booking_Date"] = pd.to_datetime(
    df_bookings["Booking_Date"]
)

df_bookings["Travel_Date"] = pd.to_datetime(
    df_bookings["Travel_Date"]
)

print("Invalid booking dates:",
      (df_bookings["Booking_Date"] >
       df_bookings["Travel_Date"]).sum())


# Service rating validation

rating_columns = [
    "Inflight_Service",
    "Cleanliness",
    "Seat_Comfort",
    "Food_Drink",
    "Checkin_Service",
    "Baggage_Handling",
    "Online_Boarding"
]

invalid_ratings = (
    (df_surveys[rating_columns] < 1) |
    (df_surveys[rating_columns] > 5)
).sum().sum()

print("Invalid service ratings:", invalid_ratings)