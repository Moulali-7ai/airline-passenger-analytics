import pandas as pd
import numpy as np

df = pd.read_csv("Data\Raw\passenger_surveys.csv")
## print(df.head())

"""What percentage of passengers are dissatisfied?

total_passengers = len(df)
dissatisfied = (df["Satisfaction"] == "Dissatisfied").sum()

percentage = (dissatisfied / total_passengers) * 100

print(f"Percentage of dissatisfied passengers: {percentage:.2f}%")"""

"""Which service has the lowest average rating?

service_avg = df[[
    "Inflight_Service",
    "Cleanliness",
    "Seat_Comfort",
    "Food_Drink"
]].mean()

print(service_avg)

print("\nLowest Rated Service:")
print(service_avg.idxmin())
print("Average Rating:", service_avg.min())

"""
"""What is the satisfaction distribution

print(df["Satisfaction"].value_counts(normalize=True) * 100)

"""

"""
What percentage of passengers are satisfied?

satisfied_count = (df["Satisfaction"] == "Satisfied").sum()

total_passengers = len(df)

percentage = (satisfied_count / total_passengers) * 100

print(f"Percentage of satisfied passengers: {percentage:.2f}%")

"""

"""Which service should management prioritize for improvement?"""

service_ratings = df[[
    "Inflight_Service",
    "Cleanliness",
    "Seat_Comfort",
    "Food_Drink"
]].mean()

lowest_service = service_ratings.idxmin()
lowest_rating = service_ratings.min()

print("Service to prioritize:", lowest_service)
print("Average Rating:", round(lowest_rating, 2))
