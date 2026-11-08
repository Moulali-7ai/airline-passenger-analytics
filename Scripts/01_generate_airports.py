
import pandas as pd
import numpy as np
import os

# ==========================================
# AIRLINE PASSENGER ANALYTICS
# DATASET 1: AIRPORT MASTER DATA
# ==========================================

# Reproducibility
np.random.seed(42)

# Airport master records
airports = [
    ("HYD", "Rajiv Gandhi International Airport", "Hyderabad", "India"),
    ("DEL", "Indira Gandhi International Airport", "Delhi", "India"),
    ("BOM", "Chhatrapati Shivaji Maharaj International Airport", "Mumbai", "India"),
    ("BLR", "Kempegowda International Airport", "Bengaluru", "India"),
    ("MAA", "Chennai International Airport", "Chennai", "India"),
    ("CCU", "Netaji Subhas Chandra Bose International Airport", "Kolkata", "India"),
    ("COK", "Cochin International Airport", "Kochi", "India"),
    ("AMD", "Sardar Vallabhbhai Patel International Airport", "Ahmedabad", "India"),
    ("PNQ", "Pune Airport", "Pune", "India"),
    ("GOI", "Manohar International Airport", "Goa", "India"),
    ("JAI", "Jaipur International Airport", "Jaipur", "India"),
    ("LKO", "Chaudhary Charan Singh International Airport", "Lucknow", "India"),
    ("DXB", "Dubai International Airport", "Dubai", "UAE"),
    ("AUH", "Zayed International Airport", "Abu Dhabi", "UAE"),
    ("DOH", "Hamad International Airport", "Doha", "Qatar"),
    ("SIN", "Singapore Changi Airport", "Singapore", "Singapore"),
    ("LHR", "Heathrow Airport", "London", "United Kingdom"),
    ("JFK", "John F. Kennedy International Airport", "New York", "USA"),
    ("LAX", "Los Angeles International Airport", "Los Angeles", "USA"),
    ("CDG", "Charles de Gaulle Airport", "Paris", "France"),
    ("FRA", "Frankfurt Airport", "Frankfurt", "Germany"),
    ("HND", "Haneda Airport", "Tokyo", "Japan"),
    ("NRT", "Narita International Airport", "Tokyo", "Japan"),
    ("SYD", "Sydney Airport", "Sydney", "Australia"),
    ("MEL", "Melbourne Airport", "Melbourne", "Australia"),
    ("YYZ", "Toronto Pearson International Airport", "Toronto", "Canada"),
    ("ICN", "Incheon International Airport", "Seoul", "South Korea"),
    ("KUL", "Kuala Lumpur International Airport", "Kuala Lumpur", "Malaysia"),
    ("IST", "Istanbul Airport", "Istanbul", "Turkey"),
    ("CPT", "Cape Town International Airport", "Cape Town", "South Africa")
]

# Create DataFrame
columns = [
    "Airport_Code",
    "Airport_Name",
    "City_Name",
    "Country_Name"
]

df_airports = pd.DataFrame(airports, columns=columns)

# Generate airport IDs
df_airports.insert(
    0,
    "Airport_ID",
    np.arange(1, len(df_airports) + 1)
)

# Create output directory
output_path = "data/raw"

os.makedirs(output_path, exist_ok=True)

# Export CSV
df_airports.to_csv(
    os.path.join(output_path, "airports.csv"),
    index=False
)

# Display dataset
print("\nAIRPORT MASTER DATASET")
print(df_airports)

# Basic validation
print("\nDATASET VALIDATION")

print("Total records:", len(df_airports))
print("Duplicate airport codes:", df_airports["Airport_Code"].duplicated().sum())
print("Missing values:", df_airports.isnull().sum().sum())
print("Unique airport codes:", df_airports["Airport_Code"].nunique())

print("\nDataset exported successfully!")
