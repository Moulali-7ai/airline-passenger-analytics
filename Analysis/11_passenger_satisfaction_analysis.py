## Step 1 : Extract passenger survey data

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sqlalchemy import create_engine, URL
from getpass import getpass

## MySQL Connection

password = getpass("Enter MySQL Password: ")

connection_url = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password=password,
    host="localhost",
    port=3306,
    database="airline_passenger_analytics"
)

engine = create_engine(connection_url)

## Extract Survey Data

df_surveys = pd.read_sql(
    "SELECT * FROM passenger_surveys",
    engine

)

print("\nPassenger Survey Data:")
print(df_surveys.head())

print("\nDataset Shape:")
print(df_surveys.shape)

print("\nDataset Information:")
df_surveys.info()

## Step 2: Passenger satisfaction distribution
# First, let's understand how passengers are distributed across three satisfaction categories:
# - Satisfied
# -  Neutral
# - Dissatisfied

# Overall Passenger Satisfaction

satisfaction_counts = df_surveys["Satisfaction"].value_counts()

print("\nPassenger Satisfaction DIstribution:")
print(satisfaction_counts)

# Calculate Percentage
satisfaction_percentage = (
    df_surveys["Satisfaction"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print("\nSatisfaction Percentage:")
print(satisfaction_percentage)

## Step3: Visualize satisfaction distribution

plt.figure(figsize=(8,5))

plt.bar(
    satisfaction_counts.index,
    satisfaction_counts.values,
    edgecolor="black"
)

plt.title("Passenger Satisfaction Distribution")
plt.xlabel("Satisfaction Level")
plt.ylabel("Number of Passengers")

plt.tight_layout()
plt.savefig(
    "visualizations/11_passenger_satisfaction_distribution.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

#Step3: Service Quality Analysis

Service_columns = [
    "Inflight_Service",
    "Cleanliness",
    "Seat_Comfort",
    "Food_Drink",
    "Checkin_Service",
    "Baggage_Handling",
    "Online_Boarding"
]

service_ratings = df_surveys[Service_columns].mean().round(2)
service_ratings = service_ratings.sort_values()

print("\nAverage Service Rating:")
print(service_ratings)

# Visualize service ratings

plt.figure(figsize=(11,6))

plt.barh(
    service_ratings.index,
    service_ratings.values,
    edgecolor="black"
)

plt.title("Average Passenger Ratings by Service")
plt.xlabel("Average Rating(1-5)")
plt.ylabel("Service Category")
plt.xlim(0,5)

plt.tight_layout()

plt.savefig(
    "visualizations/12_service_quality_ratings.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# Step4-Satisfaction By travel class

# 1. join Bookings and Survey tables

# Extract booking information
df_bookings = pd.read_sql(
    "SELECT Booking_ID, Travel_Class, Travel_Type, Flight_ID FROM Bookings",
    engine
)

# Merge survey and booking data
df_satisfaction = pd.merge(
    df_surveys,
    df_bookings,
    on="Booking_ID",
    how="left",
    validate="one_to_one"
)

print("\nMerged Satisfied Data:")
print(df_satisfaction.head())

# Calculate satisfaction by travel class

class_satisfaction = pd.crosstab(
    df_satisfaction["Travel_Class"],
    df_satisfaction["Satisfaction"],
    normalize="index"
).mul(100).round(2)

print("\nSatisfaction by Travel Class (%):")
print(class_satisfaction)


## Visualize the results

class_satisfaction.plot (
    kind="bar",
    stacked=True,
    figsize=(10,6)
)

plt.title("Passenger Satisfaction by Travel Class")
plt.xlabel("Travel Class")
plt.ylabel("Percentage of Passengers")
plt.xticks(rotation=0)
plt.legend(title="satisfaction")

plt.tight_layout()
plt.savefig(
    "visualizations/13_satisfaction_by_travel_class.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# Step5 - Satisfaction by Travel Type

# Calcualte satisfaction by type

travel_type_satisfaction = pd.crosstab(
    df_satisfaction["Travel_Type"],
    df_satisfaction["Satisfaction"],
    normalize="index"
).mul(100).round(2)

print("\nSatifaction by Travel Type(%):")
print(travel_type_satisfaction)

# Visualize the results

travel_type_satisfaction.plot(
    kind="bar",
    stacked=True,
    figsize=(9,6)
)

plt.title("Passenger Satisfaction by Travel Type")
plt.xlabel("Travel Type")
plt.ylabel("Percentage of passengers")
plt.xticks(rotation=0)
plt.legend(title="Satisaction")

plt.tight_layout()

plt.savefig(
    "visualizations/14_satisfaction_by_travel_type.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

df_flight_delays = pd.read_sql(
    """
    SELECT
        Flight_ID,
        Departure_Delay,
        Arrival_Delay
    FROM Flights
    """,
    engine
)

print(df_flight_delays.head())
print(df_flight_delays.columns.tolist())

print("df_satisfaction columns:")
print(df_satisfaction.columns.tolist())

print("\ndf_bookings columns:")
print(df_bookings.columns.tolist())

print("\ndf_flight_delays columns:")
print(df_flight_delays.columns.tolist())

df_satisfaction = df_surveys.merge(
    df_bookings,
    on="Booking_ID",
    how="left"
)

df_satisfaction = df_satisfaction.merge(
    df_flight_delays,
    on="Flight_ID",
    how="left"
)

print("\nFinal Dataset:")
print(df_satisfaction.head())

print("\nDataset Shape:")
print(df_satisfaction.shape)

# Create delay categorie

df_satisfaction["Delay_Category"] = pd.cut(
    df_satisfaction["Departure_Delay"],
    bins=[-float("inf"), 15, 60, float("inf")],
    labels=["On Time", "Minor Delay", "Major Delay"]
)

print("\nDelay Category Distribution:")
print(df_satisfaction["Delay_Category"].value_counts())

# Step 2: Analyse satisfaction by delay category
delay_satisfaction = pd.crosstab(
    df_satisfaction["Delay_Category"],
    df_satisfaction["Satisfaction"],
    normalize="index"
).mul(100).round(2)

print("\nSatisfaction by Delay Category (%):")
print(delay_satisfaction)

# Step 3: Visualise the results

delay_satisfaction.plot(
    kind="bar",
    stacked=True,
    figsize=(10, 6)
)

plt.title("Passenger Satisfaction by Flight Delay Category")
plt.xlabel("Departure Delay Category")
plt.ylabel("Percentage of Passengers")
plt.xticks(rotation=0)
plt.legend(title="Satisfaction")

plt.tight_layout()

plt.savefig(
    "visualizations/15_satisfaction_by_flight_delay.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# 3. Next: Analyse service quality by delay category

# Do passengers experiencing major delays also give lower ratings to airline services?

# Average service ratings by delay category

service_columns = [
    "Inflight_Service",
    "Cleanliness",
    "Seat_Comfort",
    "Food_Drink",
    "Checkin_Service",
    "Baggage_Handling",
    "Online_Boarding"
]

delay_service_analysis = (
    df_satisfaction.groupby("Delay_Category", observed=False)[service_columns]
    .mean()
    .round(2)
)

print("\nService Ratings by Delay Category:")
print(delay_service_analysis)

# Visualize the comparison

delay_service_analysis.T.plot(
    kind="bar",
    figsize=(12, 6)
)

plt.title("Service Quality Ratings by Flight Delay Category")
plt.xlabel("Service Category")
plt.ylabel("Average Rating (1–5)")
plt.xticks(rotation=35, ha="right")
plt.legend(title="Delay Category")

plt.tight_layout()

plt.savefig(
    "visualizations/16_service_ratings_by_delay.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# Analyse passenger demographics
# Step 1: Extract passenger demographics

df_passengers = pd.read_sql(
    """
    SELECT
        Passenger_ID,
        Age,
        Gender
    FROM Passengers
    """,
    engine
)

# Step 2: Merge passenger information

# Load passenger ID from Bookings
df_booking_passengers = pd.read_sql(
    """
    SELECT
        Booking_ID,
        Passenger_ID
    FROM Bookings
    """,
    engine
)

# Merge Passenger_ID into satisfaction dataset
df_satisfaction = df_satisfaction.merge(
    df_booking_passengers,
    on="Booking_ID",
    how="left",
    validate="one_to_one"
)

# Merge demographic information
df_satisfaction = df_satisfaction.merge(
    df_passengers,
    on="Passenger_ID",
    how="left",
    validate="many_to_one"
)

print(df_satisfaction.head())
print(df_satisfaction.shape)

# Step 3: Analyse satisfaction by gender
gender_satisfaction = pd.crosstab(
    df_satisfaction["Gender"],
    df_satisfaction["Satisfaction"],
    normalize="index"
).mul(100).round(2)

print("\nSatisfaction by Gender (%):")
print(gender_satisfaction)

# Step 4: Analyse satisfaction by age group

df_satisfaction["Age_Group"] = pd.cut(
    df_satisfaction["Age"],
    bins=[17, 30, 45, 60, 79],
    labels=[
        "Young Adults",
        "Adults",
        "Middle-Aged",
        "Seniors"
    ]
)

age_satisfaction = pd.crosstab(
    df_satisfaction["Age_Group"],
    df_satisfaction["Satisfaction"],
    normalize="index"
).mul(100).round(2)

print("\nSatisfaction by Age Group (%):")
print(age_satisfaction)

# Step 5: Visualize the results

age_satisfaction.plot(
    kind="bar",
    stacked=True,
    figsize=(10, 6)
)

plt.title("Passenger Satisfaction by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Percentage of Passengers")
plt.xticks(rotation=0)
plt.legend(title="Satisfaction")

plt.tight_layout()

plt.savefig(
    "visualizations/17_satisfaction_by_age_group.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


engine.dispose()