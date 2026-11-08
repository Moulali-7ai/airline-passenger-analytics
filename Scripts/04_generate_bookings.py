
import pandas as pd
import numpy as np
import os

# ==========================================
# DATASET 4: BOOKING GENERATION
# ==========================================

np.random.seed(42)

TOTAL_BOOKINGS = 25000

# Load existing datasets
df_passengers = pd.read_csv("data/raw/passengers.csv")
df_flights = pd.read_csv("data/raw/flights.csv")

# Generate booking IDs
booking_ids = np.arange(1, TOTAL_BOOKINGS + 1)

# Assign passengers
passenger_ids = np.random.choice(
    df_passengers["Passenger_ID"],
    TOTAL_BOOKINGS
)

# Assign flights
flight_ids = np.random.choice(
    df_flights["Flight_ID"],
    TOTAL_BOOKINGS
)

# Generate booking dates
booking_dates = (
    pd.Timestamp("2024-01-01") +
    pd.to_timedelta(
        np.random.randint(0, 730, TOTAL_BOOKINGS),
        unit="D"
    )
)

# Generate travel dates (always after booking dates)
advance_days = np.random.randint(1, 181, TOTAL_BOOKINGS)

travel_dates = (
    booking_dates +
    pd.to_timedelta(advance_days, unit="D")
)

# Generate travel types
travel_types = np.random.choice(
    ["Business", "Personal"],
    TOTAL_BOOKINGS,
    p=[0.35, 0.65]
)

# Generate travel classes
travel_classes = np.random.choice(
    ["Economy", "Business", "First Class"],
    TOTAL_BOOKINGS,
    p=[0.75, 0.20, 0.05]
)

# Create DataFrame
df_bookings = pd.DataFrame({
    "Booking_ID": booking_ids,
    "Passenger_ID": passenger_ids,
    "Flight_ID": flight_ids,
    "Booking_Date": booking_dates,
    "Travel_Date": travel_dates,
    "Travel_Type": travel_types,
    "Travel_Class": travel_classes
})

# Export dataset
os.makedirs("data/raw", exist_ok=True)

df_bookings.to_csv(
    "data/raw/bookings.csv",
    index=False
)

# Validation
print("\nBOOKING DATASET VALIDATION")

print("Total bookings:", len(df_bookings))

print("Unique booking IDs:",
      df_bookings["Booking_ID"].nunique())

print("Invalid passenger references:",
      (~df_bookings["Passenger_ID"].isin(
          df_passengers["Passenger_ID"]
      )).sum())

print("Invalid flight references:",
      (~df_bookings["Flight_ID"].isin(
          df_flights["Flight_ID"]
      )).sum())

print("Invalid booking dates:",
      (df_bookings["Booking_Date"] >
       df_bookings["Travel_Date"]).sum())

print("Missing values:",
      df_bookings.isnull().sum().sum())

print("\nTravel class distribution:")
print(df_bookings["Travel_Class"].value_counts())

print("\nBooking dataset generated successfully!")
