
import pandas as pd
import numpy as np
import os

# Reproducibility
np.random.seed(42)

# Configuration
TOTAL_PASSENGERS = 25000

# Sample names
first_names = [
    "Arjun", "Rahul", "Priya", "Ananya", "Vikram",
    "Sneha", "Karthik", "Divya", "Amit", "Neha",
    "Rohit", "Meera", "Sanjay", "Pooja", "Varun",
    "Aisha", "Daniel", "John", "Sarah", "Michael"
]

last_names = [
    "Sharma", "Reddy", "Kumar", "Patel", "Singh",
    "Gupta", "Rao", "Verma", "Mehta", "Nair",
    "Williams", "Brown", "Wilson", "Taylor", "Thomas"
]

# Generate passenger IDs
passenger_ids = np.arange(1, TOTAL_PASSENGERS + 1)

# Generate passenger names
passenger_names = [
    np.random.choice(first_names) + " " +
    np.random.choice(last_names)
    for _ in range(TOTAL_PASSENGERS)
]

# Generate age
ages = np.random.randint(18, 80, TOTAL_PASSENGERS)

# Generate gender
genders = np.random.choice(
    ["Male", "Female", "Other"],
    size=TOTAL_PASSENGERS,
    p=[0.50, 0.47, 0.03]
)

# Create DataFrame
df_passengers = pd.DataFrame({
    "Passenger_ID": passenger_ids,
    "Passenger_Name": passenger_names,
    "Age": ages,
    "Gender": genders
})

# Export dataset
os.makedirs("data/raw", exist_ok=True)

df_passengers.to_csv(
    "data/raw/passengers.csv",
    index=False
)

# Validation
print("\nPASSENGER DATASET VALIDATION")

print("Total passengers:", len(df_passengers))
print("Unique passenger IDs:",
      df_passengers["Passenger_ID"].nunique())

print("Duplicate IDs:",
      df_passengers["Passenger_ID"].duplicated().sum())

print("Missing values:",
      df_passengers.isnull().sum().sum())

print("\nGender distribution:")
print(df_passengers["Gender"].value_counts())

print("\nAge statistics:")
print(df_passengers["Age"].describe())

print("\nPassenger dataset exported successfully!")
