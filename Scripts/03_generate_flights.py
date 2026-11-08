
import pandas as pd
import numpy as np
import os

# ==========================================
# AIRLINE PASSENGER ANALYTICS
# DATASET 3: FLIGHT OPERATIONS
# ==========================================

np.random.seed(42)

TOTAL_FLIGHTS = 2500

# Load airport master dataset
df_airports = pd.read_csv("data/raw/airports.csv")

airport_ids = df_airports["Airport_ID"].to_numpy()

# Airline information
airlines = [
    "Air India",
    "IndiGo",
    "Emirates",
    "Qatar Airways",
    "Singapore Airlines",
    "British Airways",
    "Lufthansa",
    "Etihad Airways"
]

airline_codes = {
    "Air India": "AI",
    "IndiGo": "6E",
    "Emirates": "EK",
    "Qatar Airways": "QR",
    "Singapore Airlines": "SQ",
    "British Airways": "BA",
    "Lufthansa": "LH",
    "Etihad Airways": "EY"
}

# Generate flight IDs
flight_ids = np.arange(1, TOTAL_FLIGHTS + 1)

# Generate airlines
selected_airlines = np.random.choice(
    airlines,
    TOTAL_FLIGHTS
)

# Generate flight numbers
flight_numbers = [
    f"{airline_codes[airline]}{np.random.randint(100, 9999)}"
    for airline in selected_airlines
]

# Generate origin and destination airports
origin_airports = np.random.choice(
    airport_ids,
    TOTAL_FLIGHTS
)

destination_airports = []

for origin in origin_airports:
    possible_destinations = airport_ids[airport_ids != origin]
    destination_airports.append(
        np.random.choice(possible_destinations)
    )

destination_airports = np.array(destination_airports)

# Generate distance in kilometres
distances = np.random.randint(250, 12000, TOTAL_FLIGHTS)

# Generate departure delays
departure_delays = np.random.normal(
    loc=15,
    scale=35,
    size=TOTAL_FLIGHTS
).astype(int)

# Generate arrival delays
arrival_delays = (
    departure_delays +
    np.random.normal(0, 20, TOTAL_FLIGHTS).astype(int)
)

# Scheduled departure dates and times
scheduled_departures = (
    pd.Timestamp("2025-01-01") +
    pd.to_timedelta(
        np.random.randint(0, 365 * 24 * 60, TOTAL_FLIGHTS),
        unit="m"
    )
)

# Estimate flight duration from distance
flight_duration = (
    distances / 750 * 60
).astype(int)

scheduled_arrivals = (
    scheduled_departures +
    pd.to_timedelta(flight_duration, unit="m")
)

# Actual flight timings
actual_departures = (
    scheduled_departures +
    pd.to_timedelta(departure_delays, unit="m")
)

actual_arrivals = (
    scheduled_arrivals +
    pd.to_timedelta(arrival_delays, unit="m")
)

# Create DataFrame
df_flights = pd.DataFrame({
    "Flight_ID": flight_ids,
    "Flight_Number": flight_numbers,
    "Airline_Name": selected_airlines,
    "Distance": distances,
    "Departure_Delay": departure_delays,
    "Arrival_Delay": arrival_delays,
    "Origin_Airport_ID": origin_airports,
    "Destination_Airport_ID": destination_airports,
    "Scheduled_Departure": scheduled_departures,
    "Scheduled_Arrival": scheduled_arrivals,
    "Actual_Departure": actual_departures,
    "Actual_Arrival": actual_arrivals
})

# Export CSV
os.makedirs("data/raw", exist_ok=True)

df_flights.to_csv(
    "data/raw/flights.csv",
    index=False
)

# Validation
print("\nFLIGHT DATASET VALIDATION")

print("Total flights:", len(df_flights))

print("Unique flight IDs:",
      df_flights["Flight_ID"].nunique())

print("Duplicate flight IDs:",
      df_flights["Flight_ID"].duplicated().sum())

print("Same origin and destination:",
      (df_flights["Origin_Airport_ID"] ==
       df_flights["Destination_Airport_ID"]).sum())

print("Missing values:",
      df_flights.isnull().sum().sum())

print("\nAverage departure delay:",
      round(df_flights["Departure_Delay"].mean(), 2))

print("Average arrival delay:",
      round(df_flights["Arrival_Delay"].mean(), 2))

print("\nFlight dataset exported successfully!")
