CREATE DATABASE IF NOT EXISTS car_damage_detection;

USE car_damage_detection;

CREATE TABLE IF NOT EXISTS user_info (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    vehicle_id VARCHAR(50) NOT NULL UNIQUE,
    contact_number VARCHAR(10) NOT NULL,
    address VARCHAR(100) NOT NULL,
    car_brand VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS car_models (
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    part VARCHAR(50) NOT NULL,
    price INT NOT NULL
);

SELECT * FROM user_info;
SELECT * FROM car_models;
SELECT COUNT(*) FROM car_models;

-- DROP TABLE user_info;
-- DROP TABLE car_models;