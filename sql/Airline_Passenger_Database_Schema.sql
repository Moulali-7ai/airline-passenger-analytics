Create database airline_passenger_analytics;

show databases;

use airline_passenger_analytics;

CREATE table Passengers (
Passenger_ID varchar(10) primary key, 
Passenger_Name varchar(50), 
Age int(2), 
Gender varchar(15)
);

DESC passengers; /* to check the data type of the column */

alter table Passengers
modify column Passenger_ID int auto_increment; /* change the column datatype and also adding auto_increment the number */

show columns from Passengers;

Create table Airport (
Airport_ID int primary key auto_increment,
Airport_Name varchar(50),
City_Name Varchar(50),
Country_Name Varchar(50) 
);

create table Flights(
Flight_ID Int primary key auto_increment,
Airport_ID int,foreign key (Airport_ID) references Airport(Airport_ID),
Flight_Number int,
AirLine_Name Varchar(30),
Distance int,
Departure_Delay int,
Arrival_Delay int
);

DESC Flights;

alter table Airport
add column Airport_Code varchar(15)
after Airport_ID;

show columns from Airport;

Create Table Bookings (
Booking_ID int primary key auto_increment,
Passenger_ID int,foreign key (Passenger_ID) references Passengers(Passenger_ID),
Flight_ID int,foreign key (Flight_ID) references Flights(Flight_ID),
Origin_Airport_ID int, foreign key (Origin_Airport_ID) references Airport(Airport_ID),
Destination_Airport_ID int, foreign key (Destination_Airport_ID) references Airport(Airport_ID),
Booking_Date date,
Travel_Date date,
Travel_Type varchar(50),
Travel_Class varchar(50)
);

show tables;

create table passenger_surveys (
Survey_ID int primary key	auto_increment,
Booking_ID int,foreign key (Booking_ID) references Bookings(Booking_ID),
Inflight_Service int,
Cleanlines int,
Seat_Comfort int,
Food_Drink int,
Satisfaction int
);
desc Bookings;