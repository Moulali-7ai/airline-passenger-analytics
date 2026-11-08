import pandas as pd
from sqlalchemy import create_engine, URL
from getpass import getpass

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

# Load passenger data
df = pd.read_sql("SELECT * FROM Passengers", engine)

print(df.head())
print(df.shape)
print(df.info())

# 1. Statistical summary
print("\n--- Statistical Summary ---")
print(df.describe())

# 2. Missing values
print("\n--- Missing Values ---")
print(df.isnull().sum())

# 3. Duplicate records
print("\n--- Duplicate Records ---")
print("Total duplicates:", df.duplicated().sum())

# 4. Duplicate passenger IDs
print("\n--- Duplicate Passenger IDs ---")
print(df["Passenger_ID"].duplicated().sum())

# 5. Unique values
print("\n--- Unique Values ---")
print("Unique Passenger IDs:", df["Passenger_ID"].nunique())
print("Unique Ages:", df["Age"].nunique())
print("Unique Genders:", df["Gender"].unique())

# 6. Age statistics
print("\n--- Age Statistics ---")
print("Minimum Age:", df["Age"].min())
print("Maximum Age:", df["Age"].max())
print("Average Age:", round(df["Age"].mean(), 2))

# 7. Gender distribution
print("\n--- Gender Distribution ---")
print(df["Gender"].value_counts())

engine.dispose()