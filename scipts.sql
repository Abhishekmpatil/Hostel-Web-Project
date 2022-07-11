CREATE TABLE hostel
(
    Hostel_ID      INTEGER PRIMARY KEY,
    Hostel_Name    TEXT,
    Hostel_Phone   INTEGER,
    Hostel_Email   TEXT,
    Hostel_Address TEXT,
    Postcode       TEXT
);
CREATE TABLE room
(
    Room_ID      INTEGER PRIMARY KEY,
    Hostel_ID    INTEGER,
    Room_Type_ID TEXT
);
CREATE TABLE room_category
(
    Room_category_id    INTEGER PRIMARY KEY,
    Room_category_Name  TEXT,
    Room_Rent_per_month INTEGER,
    Number_Of_Seats     INTEGER,
    Description         TEXT
);
CREATE TABLE student
(
    Student_ID          INTEGER PRIMARY KEY,
    Student_Name        TEXT,
    Student_Father_Name TEXT,
    Date_of_Birth       DATE,
    Student_Gender      TEXT,
    Mobile              TEXT,
    Student_Email       TEXT,
    Permanent_Address   TEXT,
    Username            TEXT,
    Password            TEXT
);

DROP TABLE IF EXISTS reservation;
CREATE TABLE reservation
(
    Reservation_ID   INTEGER PRIMARY KEY,
    Student_ID       INTEGER,
    Room_ID          INT,
    Room_Category    TEXT,
    Reservation_Date DATE,
    Total_Month      INT,
    Status           TEXT
);
