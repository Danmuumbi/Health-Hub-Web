/*
DROP TABLE IF EXISTS Medical_Records;
DROP TABLE IF EXISTS Appointments;
DROP TABLE IF EXISTS Payments;
DROP TABLE IF EXISTS order_item;
DROP TABLE IF EXISTS `order`;
DROP TABLE IF EXISTS product;

-- Drop parent tables
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Departments;

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
);

-- Add price column to Appointments table
ALTER TABLE Appointments ADD COLUMN price DECIMAL(10, 2);

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

-- Create product table
CREATE TABLE product (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    seller_id INT NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL,
    date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
    image LONGBLOB,
    FOREIGN KEY (seller_id) REFERENCES Users(user_id)
);

-- Create order table
CREATE TABLE `order` (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    buyer_id INT NOT NULL,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50),
    FOREIGN KEY (buyer_id) REFERENCES Users(user_id)
);

-- Create order_item table
CREATE TABLE order_item (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES `order`(order_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);*/
-- Drop dependent tables first
DROP TABLE IF EXISTS Medical_Records;
DROP TABLE IF EXISTS Appointments;
DROP TABLE IF EXISTS Payments;
DROP TABLE IF EXISTS order_item;
DROP TABLE IF EXISTS `order`;
DROP TABLE IF EXISTS product;

-- Drop parent tables
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Departments;

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
);

-- Add price column to Appointments table
ALTER TABLE Appointments ADD COLUMN price DECIMAL(10, 2);

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

-- Create product table
CREATE TABLE product (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    seller_id INT NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL,
    date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
    image LONGBLOB,
    FOREIGN KEY (seller_id) REFERENCES Users(user_id)
);

-- Create order table
CREATE TABLE `order` (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    buyer_id INT NOT NULL,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50),
    FOREIGN KEY (buyer_id) REFERENCES Users(user_id)
);

-- Create order_item table
CREATE TABLE order_item (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES `order`(order_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);

