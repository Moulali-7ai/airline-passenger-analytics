import pandas as pd
import numpy as np

# Read CSV file
df_flights = pd.read_csv("data/raw/flights.csv")

# Display dataset
print("\nFirst five records:")
print(df_flights.head())

print("\nDataset information:")
print(df_flights.info())

print("\nDataset shape:")
print(df_flights.shape)