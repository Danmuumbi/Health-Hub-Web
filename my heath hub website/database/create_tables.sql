-- Create Users table
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender CHAR(1) NOT NULL,
    address VARCHAR(255),
    phone_number VARCHAR(15),
    profile_picture BLOB
);

-- Create Medical_Records table
CREATE TABLE Medical_Records (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    medical_history TEXT,
    medications TEXT,
    vaccination_record TEXT,
    lab_results TEXT,
    allergies TEXT,
    immunizations TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Create Appointments table
CREATE TABLE Appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    service_type VARCHAR(100),
    date_time DATETIME NOT NULL,
    status VARCHAR(50),
    FOREIGN KEY (patient_id) REFERENCES Users(user_id)
    ALTER TABLE Appointments ADD COLUMN price DECIMAL(10, 2);

);

-- Create Departments table
CREATE TABLE Departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    location VARCHAR(255),
    contact_info VARCHAR(255)
);

-- Create Payments table
CREATE TABLE Payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    payment_info TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
