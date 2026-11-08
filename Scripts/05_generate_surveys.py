
import pandas as pd
import numpy as np
import os

# ==========================================
# DATASET 5: PASSENGER SURVEY GENERATION
# ==========================================

np.random.seed(42)

TOTAL_SURVEYS = 23000

# Load existing datasets
df_bookings = pd.read_csv(
    "data/raw/bookings.csv",
    parse_dates=["Travel_Date"]
)

df_flights = pd.read_csv(
    "data/raw/flights.csv"
)

# Select 23,000 bookings for survey responses
df_survey_bookings = df_bookings.sample(
    n=TOTAL_SURVEYS,
    random_state=42
).copy()

# Connect flight details
df_survey_bookings = df_survey_bookings.merge(
    df_flights[
        ["Flight_ID", "Departure_Delay", "Arrival_Delay"]
    ],
    on="Flight_ID",
    how="left"
)

# Generate service ratings
service_columns = [
    "Inflight_Service",
    "Cleanliness",
    "Seat_Comfort",
    "Food_Drink",
    "Checkin_Service",
    "Baggage_Handling",
    "Online_Boarding"
]

# Base ratings
for column in service_columns:
    df_survey_bookings[column] = np.random.choice(
        [1, 2, 3, 4, 5],
        size=TOTAL_SURVEYS,
        p=[0.08, 0.12, 0.20, 0.35, 0.25]
    )

# Identify delayed flights
high_delay = (
    df_survey_bookings["Departure_Delay"] > 60
)

# Reduce airport service ratings for heavily delayed flights
df_survey_bookings.loc[
    high_delay, "Checkin_Service"
] = np.maximum(
    1,
    df_survey_bookings.loc[
        high_delay, "Checkin_Service"
    ] - 1
)

# Calculate satisfaction score
average_rating = df_survey_bookings[
    service_columns
].mean(axis=1)

# Include operational delay impact
delay_penalty = (
    df_survey_bookings["Departure_Delay"]
    .clip(lower=0, upper=120) / 120
) * 1.2

final_score = average_rating - delay_penalty

# Classify satisfaction
df_survey_bookings["Satisfaction"] = np.where(
    final_score >= 3.6,
    "Satisfied",
    np.where(
        final_score >= 2.7,
        "Neutral",
        "Dissatisfied"
    )
)

# Select final columns
df_surveys = df_survey_bookings[
    [
        "Booking_ID",
        "Inflight_Service",
        "Cleanliness",
        "Seat_Comfort",
        "Food_Drink",
        "Satisfaction",
        "Checkin_Service",
        "Baggage_Handling",
        "Online_Boarding"
    ]
].copy()

# Generate survey IDs
df_surveys.insert(
    0,
    "Survey_ID",
    np.arange(1, TOTAL_SURVEYS + 1)
)

# Export CSV
os.makedirs("data/raw", exist_ok=True)

df_surveys.to_csv(
    "data/raw/passenger_surveys.csv",
    index=False
)

# Validation
print("\nPASSENGER SURVEY VALIDATION")

print("Total surveys:", len(df_surveys))

print("Unique survey IDs:",
      df_surveys["Survey_ID"].nunique())

print("Duplicate booking IDs:",
      df_surveys["Booking_ID"].duplicated().sum())

print("Missing values:",
      df_surveys.isnull().sum().sum())

print("\nSatisfaction distribution:")
print(df_surveys["Satisfaction"].value_counts())

print("\nAverage service ratings:")
print(df_surveys[service_columns].mean())

print("\nPassenger survey dataset generated successfully!")
