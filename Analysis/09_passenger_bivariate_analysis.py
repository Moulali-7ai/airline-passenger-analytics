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

# Extract data
df = pd.read_sql("SELECT * FROM Passengers", engine)

# Age distribution by gender
plt.figure(figsize=(9, 5))

df.boxplot(
    column="Age",
    by="Gender",
    grid=False
)

plt.title("Passenger Age Distribution by Gender")
plt.suptitle("")
plt.xlabel("Gender")
plt.ylabel("Age")

plt.savefig(
    "visualizations/04_age_distribution_by_gender.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# Passenger age segmentation

def categorize_age(age):
    if 18 <= age <= 30:
        return "Young Adults"
    elif 31 <= age <= 45:
        return "Adults"
    elif 46 <= age <= 60:
        return "Middle-Aged"
    else:
        return "Seniors"


df["Age_Group"] = df["Age"].apply(categorize_age)

print(df[["Passenger_ID", "Age", "Age_Group"]].head(10))

## Calculate passenger distribution

age_group_counts = df["Age_Group"].value_counts()

print("\nPassenger Distribution by Age Group:")
print(age_group_counts)

## Create a visualization

plt.figure(figsize=(9, 5))

plt.bar(
    age_group_counts.index,
    age_group_counts.values,
    edgecolor="black"
)

plt.title("Passenger Distribution by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Number of Passengers")
plt.xticks(rotation=15)

plt.savefig(
    "visualizations/05_passenger_age_segmentation.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

engine.dispose()