import pandas as pd
import matplotlib.pyplot as plt

from sqlalchemy import create_engine, URL
from getpass import getpass

# Database connection
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

# Extract flight data
df_flights = pd.read_sql(
    "SELECT * FROM Flights",
    engine
)

print(df_flights.head())
print(df_flights.shape)
print(df_flights.info())

df_flights = pd.read_sql(
    "SELECT * FROM Flights",
    engine
)

print(df_flights.head())
print(df_flights.shape)
print(df_flights["Airline_Name"].value_counts())

# Average departure delay by airline

departure_delay = (
    df_flights.groupby("Airline_Name")["Departure_Delay"]
    .mean()
    .round(2)
    .sort_values(ascending=False)
)

print("\nAverage Departure Delay by Airline:")
print(departure_delay)


# Average arrival delay by airline

arrival_delay = (
    df_flights.groupby("Airline_Name")["Arrival_Delay"]
    .mean()
    .round(2)
    .sort_values(ascending=False)
)

print("\nAverage Arrival Delay by Airline:")
print(arrival_delay)

import numpy as np

# Classify flight performance

df_flights["Flight_Status"] = np.where(
    df_flights["Departure_Delay"] <= 15,
    "On Time",
    "Delayed"
)

# Calculate flight counts

flight_status = df_flights["Flight_Status"].value_counts()

print("\nFlight Status Distribution:")
print(flight_status)

# Calculate percentages

flight_percentage = (
    df_flights["Flight_Status"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print("\nFlight Status Percentage:")
print(flight_percentage)

## visualizarion

plt.figure(figsize=(8, 5))

plt.bar(
    flight_status.index,
    flight_status.values,
    edgecolor="black"
)

plt.title("On-Time vs Delayed Flights")
plt.xlabel("Flight Status")
plt.ylabel("Number of Flights")

plt.savefig(
    "visualizations/06_flight_status_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

## Step 1: Load airport data

# Load Airport Data
df_airports = pd.read_sql("SELECT * FROM Airport", engine)

print("\nAirport Data:")
print(df_airports.head())

print("\nAirport Shape:")
print(df_airports.shape)

# Rename airport columns for origin analysis
origin_airports = df_airports.rename(columns={
    "Airport_ID": "Origin_Airport_ID",
    "Airport_Code": "Origin_Airport_Code",
    "Airport_Name": "Origin_Airport_Name",
    "City_Name": "Origin_City"
})

# Merge Flights and Airport tables
df_origin = pd.merge(
    df_flights,
    origin_airports[
        ["Origin_Airport_ID", "Origin_Airport_Code",
         "Origin_Airport_Name", "Origin_City"]
    ],
    on="Origin_Airport_ID",
    how="left",
    validate="many_to_one"
)

print("\nMerged Data:")
print(df_origin.head())

## Analyse airport performance

airport_performance = (
    df_origin.groupby(
        ["Origin_Airport_Code", "Origin_City"]
    )
    .agg(
        Total_Flights=("Flight_ID", "count"),
        Average_Departure_Delay=("Departure_Delay", "mean")
    )
    .round(2)
    .sort_values("Average_Departure_Delay", ascending=False)
)

print("\nAirport Performance:")
print(airport_performance)

## Visualize airport performance

plt.figure(figsize=(12, 6))

plt.bar(
    airport_performance.index.get_level_values("Origin_Airport_Code"),
    airport_performance["Average_Departure_Delay"],
    edgecolor="black"
)

plt.title("Average Departure Delay by Origin Airport")
plt.xlabel("Airport Code")
plt.ylabel("Average Departure Delay (Minutes)")
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig(
    "visualizations/07_airport_departure_delay.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

## Step 2: Destination airport analysis

## Merge Flights with destination airport details

destination_airports = df_airports.rename(columns={
    "Airport_ID": "Destination_Airport_ID",
    "Airport_Code": "Destination_Airport_Code",
    "Airport_Name": "Destination_Airport_Name",
    "City_Name": "Destination_City"
})

df_destination = pd.merge(
    df_flights,
    destination_airports[
        ["Destination_Airport_ID", "Destination_Airport_Code",
         "Destination_Airport_Name", "Destination_City"]
    ],
    on="Destination_Airport_ID",
    how="left",
    validate="many_to_one"
)

## Calculate destination airport performance

destination_performance = (
    df_destination.groupby(
        ["Destination_Airport_Code", "Destination_City"]
    )
    .agg(
        Total_Flights=("Flight_ID", "count"),
        Average_Arrival_Delay=("Arrival_Delay", "mean")
    )
    .round(2)
    .sort_values("Average_Arrival_Delay", ascending=False)
)

print("\nDestination Airport Performance:")
print(destination_performance)

## Create a visualization

plt.figure(figsize=(12, 6))

plt.bar(
    destination_performance.index.get_level_values(
        "Destination_Airport_Code"
    ),
    destination_performance["Average_Arrival_Delay"],
    edgecolor="black"
)

plt.title("Average Arrival Delay by Destination Airport")
plt.xlabel("Destination Airport")
plt.ylabel("Average Arrival Delay (Minutes)")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "visualizations/08_destination_airport_performance.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

## Step 3: Flight route analysis
## A route represents the journey from an origin airport to a destination airport.

# Merge origin and destination airport details
df_routes = df_origin.merge(
    destination_airports[
        ["Destination_Airport_ID", "Destination_Airport_Code"]
    ],
    on="Destination_Airport_ID",
    how="left",
    validate="many_to_one"
)

df_routes["Flight_Route"] = (
    df_routes["Origin_Airport_Code"] + " → " +
    df_routes["Destination_Airport_Code"]
)

## Calculate route performance

route_performance = (
    df_routes.groupby("Flight_Route")
    .agg(
        Total_Flights=("Flight_ID", "count"),
        Average_Departure_Delay=("Departure_Delay", "mean"),
        Average_Arrival_Delay=("Arrival_Delay", "mean")
    )
    .round(2)
    .sort_values("Average_Arrival_Delay", ascending=False)
)

print("\nTop 10 Routes with Highest Average Arrival Delay:")
print(route_performance.head(10))

##  Visualize the top 10 delayed routes

top_routes = route_performance.head(10)

plt.figure(figsize=(12, 6))

plt.bar(
    top_routes.index,
    top_routes["Average_Arrival_Delay"],
    edgecolor="black"
)

plt.title("Top 10 Routes by Average Arrival Delay")
plt.xlabel("Flight Routes")
plt.ylabel("Average Arrival Delay (Minutes)")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "visualizations/09_top_delayed_routes.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

## Step 4: Relationship between departure and arrival delays
## Business question: Do departure delays affect arrival delays?

# Correlation between departure and arrival delays

correlation = df_flights[
    ["Departure_Delay", "Arrival_Delay"]
].corr()

print("\nDelay Correlation:")
print(correlation)

print(
    "\nCorrelation Value:",
    round(
        df_flights["Departure_Delay"].corr(
            df_flights["Arrival_Delay"]
        ),
        3
    )
)

## 2. Create a scatter plot

plt.figure(figsize=(9, 6))

plt.scatter(
    df_flights["Departure_Delay"],
    df_flights["Arrival_Delay"],
    alpha=0.5
)

plt.title("Relationship Between Departure and Arrival Delays")
plt.xlabel("Departure Delay (Minutes)")
plt.ylabel("Arrival Delay (Minutes)")

plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    "visualizations/10_departure_vs_arrival_delay.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

engine.dispose()