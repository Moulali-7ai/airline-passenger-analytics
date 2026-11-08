import pandas as pd
import matplotlib.pyplot as plt

from sqlalchemy import create_engine, URL
from getpass import getpass

# 1. MySQL Connection
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

# 2. Extract passenger data from MySQL
df = pd.read_sql("SELECT * FROM Passengers", engine)

print("Dataset loaded successfully!")
print(df.head())

# 3. Age Distribution - Histogram
plt.figure(figsize=(10, 5))

plt.hist(df["Age"], bins=15, edgecolor="black")

plt.title("Passenger Age Distribution")
plt.xlabel("Age")
plt.ylabel("Number of Passengers")

plt.show()

# 4. Gender Distribution - Bar Chart
gender_counts = df["Gender"].value_counts()

plt.figure(figsize=(8, 5))

plt.bar(
    gender_counts.index,
    gender_counts.values,
    edgecolor="black"
)

plt.title("Passenger Gender Distribution")
plt.xlabel("Gender")
plt.ylabel("Number of Passengers")

plt.show()

# 5. Age Distribution - Box Plot
plt.figure(figsize=(8, 4))

plt.boxplot(df["Age"], vert=False)

plt.title("Passenger Age Box Plot")
plt.xlabel("Age")

plt.show()

# 6. Close database connection
engine.dispose()