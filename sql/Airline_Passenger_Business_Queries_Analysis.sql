show databases;

use airline_passenger_analytics;

ALTER TABLE Airport
MODIFY Airport_Code VARCHAR(3) NOT NULL,
ADD CONSTRAINT UQ_Airport_Code UNIQUE (Airport_Code);

desc Airport;

SHOW CREATE TABLE Flights;

SHOW CREATE TABLE Bookings;

ALTER TABLE Flights
DROP FOREIGN KEY Flights_ibfk_1,
DROP COLUMN Airport_ID;

ALTER TABLE Flights
MODIFY Flight_Number VARCHAR(20),
CHANGE COLUMN AirLine_Name Airline_Name VARCHAR(50),
ADD COLUMN Origin_Airport_ID INT NOT NULL,
ADD COLUMN Destination_Airport_ID INT NOT NULL,
ADD COLUMN Scheduled_Departure DATETIME,
ADD COLUMN Scheduled_Arrival DATETIME;

ALTER TABLE Flights
ADD CONSTRAINT FK_Flights_Origin
FOREIGN KEY (Origin_Airport_ID)
REFERENCES Airport(Airport_ID),

ADD CONSTRAINT FK_Flights_Destination
FOREIGN KEY (Destination_Airport_ID)
REFERENCES Airport(Airport_ID);

ALTER TABLE Bookings
DROP FOREIGN KEY Bookings_ibfk_3,
DROP FOREIGN KEY Bookings_ibfk_4,
DROP COLUMN Origin_Airport_ID,
DROP COLUMN Destination_Airport_ID;

DESCRIBE passenger_surveys;

ALTER TABLE passenger_surveys
CHANGE COLUMN Cleanlines Cleanliness TINYINT,
MODIFY COLUMN Inflight_Service TINYINT,
MODIFY COLUMN Seat_Comfort TINYINT,
MODIFY COLUMN Food_Drink TINYINT,
MODIFY COLUMN Satisfaction VARCHAR(20);

ALTER TABLE passenger_surveys
ADD CONSTRAINT UQ_Survey_Booking UNIQUE (Booking_ID),

ADD CONSTRAINT CHK_Inflight_Service
CHECK (Inflight_Service BETWEEN 1 AND 5),

ADD CONSTRAINT CHK_Cleanliness
CHECK (Cleanliness BETWEEN 1 AND 5),

ADD CONSTRAINT CHK_Seat_Comfort
CHECK (Seat_Comfort BETWEEN 1 AND 5),

ADD CONSTRAINT CHK_Food_Drink
CHECK (Food_Drink BETWEEN 1 AND 5),

ADD CONSTRAINT CHK_Satisfaction
CHECK (Satisfaction IN ('Satisfied', 'Neutral', 'Dissatisfied'));

USE airline_passenger_analytics;

SHOW TABLES;

DESC Passengers;
DESC Airport;
DESC Flights;
DESC Bookings;
DESC passenger_surveys;


SELECT
    TABLE_NAME,
    COLUMN_NAME,
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'airline_passenger_analytics'
AND REFERENCED_TABLE_NAME IS NOT NULL;

DESC Passengers;

ALTER TABLE Flights
ADD CONSTRAINT CHK_Flight_Route
CHECK (Origin_Airport_ID <> Destination_Airport_ID);

ALTER TABLE Bookings
ADD CONSTRAINT CHK_Booking_Date
CHECK (Booking_Date <= Travel_Date);

SELECT
    TABLE_NAME,
    COLUMN_NAME,
    COLUMN_TYPE,
    IS_NULLABLE,
    COLUMN_KEY,
    EXTRA
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'airline_passenger_analytics'
ORDER BY TABLE_NAME, ORDINAL_POSITION;

ALTER TABLE Flights
ADD COLUMN Actual_Departure DATETIME,
ADD COLUMN Actual_Arrival DATETIME;

ALTER TABLE passenger_surveys
ADD COLUMN Checkin_Service TINYINT,
ADD COLUMN Baggage_Handling TINYINT,
ADD COLUMN Online_Boarding TINYINT;

ALTER TABLE Bookings
MODIFY Passenger_ID INT NOT NULL,
MODIFY Flight_ID INT NOT NULL;

ALTER TABLE Bookings
DROP FOREIGN KEY bookings_ibfk_1;

ALTER TABLE Bookings
MODIFY Passenger_ID INT NOT NULL,
MODIFY Flight_ID INT NOT NULL;

ALTER TABLE Bookings
DROP FOREIGN KEY bookings_ibfk_1,
DROP FOREIGN KEY bookings_ibfk_2;

SHOW CREATE TABLE Bookings;

ALTER TABLE Bookings
DROP FOREIGN KEY bookings_ibfk_2;

ALTER TABLE Bookings
MODIFY Passenger_ID INT NOT NULL,
MODIFY Flight_ID INT NOT NULL;

ALTER TABLE Bookings

ADD CONSTRAINT FK_Booking_Passenger
FOREIGN KEY (Passenger_ID)
REFERENCES Passengers(Passenger_ID),

ADD CONSTRAINT FK_Booking_Flight
FOREIGN KEY (Flight_ID)
REFERENCES Flights(Flight_ID);

SHOW CREATE TABLE Bookings;

USE airline_passenger_analytics;

SHOW TABLES;

SELECT
    TABLE_NAME,
    TABLE_ROWS
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'airline_passenger_analytics';

USE airline_passenger_analytics;

SELECT COUNT(*) AS Total_Airports FROM Airport;

SELECT COUNT(*) AS Total_Passengers FROM Passengers;

SELECT COUNT(*) AS Total_Flights FROM Flights;

SELECT COUNT(*) AS Total_Bookings FROM Bookings;

SELECT COUNT(*) AS Total_Surveys FROM passenger_surveys;

USE airline_passenger_analytics;

SELECT 'Airport' AS Table_Name, COUNT(*) AS Total_Records FROM Airport
UNION ALL
SELECT 'Passengers', COUNT(*) FROM Passengers
UNION ALL
SELECT 'Flights', COUNT(*) FROM Flights
UNION ALL
SELECT 'Bookings', COUNT(*) FROM Bookings
UNION ALL
SELECT 'Passenger Surveys', COUNT(*) FROM passenger_surveys;

/*Business requirement
The airline management wants to know the total number of unique passengers registered in its database.

select count(distinct Passenger_ID) as Unique_Passenger_lise
from passengers;
*/

/* Business requirement: The airline management wants to understand the gender distribution of registered passengers. 

	select count(Passenger_ID) from Passengers
	group by Gender;
SELECT
    Gender,
    COUNT(Passenger_ID) AS Total_Passengers
FROM Passengers
GROUP BY Gender
ORDER BY Total_Passengers DESC;

SELECT
    gender,
    COUNT(*) AS passenger_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM passengers
GROUP BY gender;
*/

/*Business requirement: The airline wants to understand the average age of its registered passengers to support customer segmentation and targeted marketing.

select age,
count(*) as Passengers_count,
round(count(*)*100.0/avg(count(*)) over(), 2) As Average_age
From passengers
Group By Age
order by Passengers_count desc;

*/

/*Business requirement: The airline management wants to know what percentage of passengers belong to each travel class.*/


select Travel_Class,
count(*) as Total_Travel_class,
round (count(*)*100.0 /sum(count(*))over(),2) as Percentage
from bookings
group by Travel_Class
order by Percentage;

/*Business requirement: The airline wants to identify how passenger ages are distributed across different age groups.*/

select Age,
count(*) as Total_age_groups,
round(count(*) *100.0/
sum(count(*))over(),
2)
from Passengers
group by Age
order by total_age_groups;

SELECT
    CASE
        WHEN Age < 18 THEN 'Under 18'
        WHEN Age BETWEEN 18 AND 30 THEN 'Younger'
        WHEN Age BETWEEN 31 AND 45 THEN 'Middle'
        WHEN Age BETWEEN 46 AND 60 THEN 'Old'
        ELSE 'Above 60'
    END AS Age_Group,
    COUNT(*) AS Total_Passengers,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS Percentage
FROM Passengers
GROUP BY
    CASE
        WHEN Age < 18 THEN 'Under 18'
        WHEN Age BETWEEN 18 AND 30 THEN 'Younger'
        WHEN Age BETWEEN 31 AND 45 THEN 'Middle'
        WHEN Age BETWEEN 46 AND 60 THEN 'Old'
        ELSE 'Above 60'
    END
ORDER BY Percentage DESC;

/* Average passenger age using AVG().*
The airline management wants to know the average age of its registered passengers to support customer segmentation and targeted marketing.*/

select Age,
count(*) as avg_age,
round(count(*) *100.0/
avg(count(*))over(),
2)
from Passengers
group by Age
order by avg_age;

select
round(avg(Age), 2 ) as average_passengrs_age
from passengers;

 /* Multiple-condition business analysis
Business requirement:
The airline wants to identify passengers who are:
Male passengers
Between 25 and 45 years old
*/
SELECT Passenger_ID, Passenger_Name, Gender, Age 
FROM Passengers
WHERE Gender = 'Male'
	AND Age BETWEEN 25 AND 45;
  
  /*How many male passengers are between 25 and 45 years old?*/
  
select count(*) as Total_Male_Passengers
from Passengers
Where Gender = 'Male'
And Age between 25 and 45;

/* Business requirement:
The airline management wants to identify passengers who meet either of these conditions:
- Male passengers aged between 25 and 35.
- Female passengers aged between 40 and 50. */

SELECT COUNT(*) AS Total_Passengers
FROM Passengers
WHERE (Gender = 'Male' AND Age BETWEEN 25 AND 35)
   OR (Gender = 'Female' AND Age BETWEEN 40 AND 50)
group by Gender;

show databases;
use airline_passenger_analytics;

/*Business requirement:

The airline wants to identify passengers who:
- Are between 18 and 30 years old.
- Have either Male or Female gender.
- Should be classified into age groups.
- Management wants the passenger count and percentage for each gender-age combination.*/

SELECT
    Gender,
    CASE
        WHEN Age BETWEEN 18 AND 24 THEN '18-24'
        WHEN Age BETWEEN 25 AND 30 THEN '25-30'
    END AS Age_Group,
    COUNT(*) AS Passenger_Count,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS Percentage
FROM Passengers
WHERE Age BETWEEN 18 AND 30
  AND Gender IN ('Male', 'Female')
GROUP BY Gender, Age_Group
ORDER BY Gender, Age_Group;

/*Business requirement:(CTE)

The airline management wants to identify the average age of passengers by gender.

They also want to display only gender groups whose average age is greater than 40.
*/


WITH Avg_Age_By_Gender AS (
    SELECT
        Gender,
        AVG(Age) AS Average_Age
    FROM Passengers
    GROUP BY Gender
)
SELECT
    Gender,
    ROUND(Average_Age, 2) AS Average_Age
FROM Avg_Age_By_Gender
WHERE Average_Age > 40;

/*Business requirement: (CTE)

The airline management wants to identify age groups with significant passenger populations.

Requirements:
1. Classify passengers into:
   - Young Adults: 18–30
   - Adults: 31–45
   - Middle-Aged: 46–60
   - Seniors: Above 60
2. Calculate the total passengers in each age group.
3. Calculate the average age of each group.
4. Display only age groups containing more than 5,000 passengers.
5. Sort by passenger count in descending order.
*/

WITH Age_Group_Analysis AS (
    SELECT
        CASE
            WHEN Age BETWEEN 18 AND 30 THEN 'Young Adults'
            WHEN Age BETWEEN 31 AND 45 THEN 'Adults'
            WHEN Age BETWEEN 46 AND 60 THEN 'Middle-Aged'
            ELSE 'Seniors'
        END AS Age_Group,
        COUNT(*) AS Passenger_Count,
        AVG(Age) AS Average_Age
    FROM Passengers
    WHERE Age >= 18
    GROUP BY Age_Group
)

SELECT
    Age_Group,
    Passenger_Count,
    ROUND(Average_Age, 2) AS Average_Age
FROM Age_Group_Analysis
WHERE Passenger_Count > 5000
ORDER BY Passenger_Count DESC;