CREATE DATABASE hostel_complaints;
USE hostel_complaints;

CREATE TABLE complaints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    room_number VARCHAR(50),
    category VARCHAR(100),
    description TEXT,
    date DATE DEFAULT (CURRENT_DATE),
    priority VARCHAR(20)
);


