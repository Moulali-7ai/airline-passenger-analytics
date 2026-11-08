import pandas as pd
import numpy as np

# Read CSV file
df = pd.read_csv("Data/Raw/bookings.csv")

# Display first five records
print(df.head())

"""# 1. Find the most frequently booked travel class
highest_bookings = df["Travel_Class"].value_counts().idxmax()

print("Travel Class with highest bookings:", highest_bookings)"""

"""2. What is the average number of days between booking and travel?
# Convert columns to datetime
df["Booking_Date"] = pd.to_datetime(df["Booking_Date"])
df["Travel_Date"] = pd.to_datetime(df["Travel_Date"])

# Calculate days between booking and travel
df["Days_Before_Travel"] = (df["Travel_Date"] - df["Booking_Date"]).dt.days

# Average number of days
avg_days = df["Days_Before_Travel"].mean()

print("Average days between booking and travel:", round(avg_days, 2))"""

"""3.How many passengers have booked more than once?

# Count bookings for each passenger
booking_counts = df["Passenger_ID"].value_counts()

# Passengers with more than one booking
repeat_passengers = booking_counts[booking_counts > 1]

print("Number of passengers who booked more than once:", len(repeat_passengers))"""

"""4.What percentage of bookings are for business travel?

# Total bookings
total_bookings = len(df)

# Business travel bookings
business_bookings = (df["Travel_Type"] == "Business").sum()

# Percentage
percentage = (business_bookings / total_bookings) * 100

print(f"Business Travel Bookings: {percentage:.2f}%")"""

"""5. Which flights have the highest number of bookings?"""

booking_counts = df["Flight_ID"].value_counts()

print("Flight with highest bookings:", booking_counts.idxmax())
print("Number of bookings:", booking_counts.max())