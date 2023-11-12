create database if not exists GrainSenseDB;

use GrainSenseDB;

CREATE TABLE if not exists entry (
    id INT AUTO_INCREMENT PRIMARY KEY,
    send_id INT NOT NULL,
    height_level INT NOT NULL,
    stick_id INT NOT NULL,
    temp INT NOT NULL,
    time DATETIME NOT NULL
);

CREATE TABLE if not exists owner (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username NVARCHAR(45) NOT NULL,
    password NVARCHAR(45) NOT NULL,
    email NVARCHAR(100) NOT NULL,
    first_name NVARCHAR(45) NOT NULL,
    last_name NVARCHAR(45) NOT NULL
);

CREATE TABLE if not exists gateway (
    id INT AUTO_INCREMENT PRIMARY KEY,
    owner_id INT NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES owner (id)
);



CREATE TABLE if not exists seed_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lower_bound INT NOT NULL,
    upper_bound INT NOT NULL,
    name NVARCHAR(45) NOT NULL
);

CREATE TABLE if not exists storage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    address NVARCHAR(100) NOT NULL,
    owner_id INT NOT NULL,
    seed_types_id INT NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES owner (id),
    FOREIGN KEY (seed_types_id) REFERENCES seed_types (id)
);

CREATE TABLE if not exists stick (
    id INT AUTO_INCREMENT PRIMARY KEY,
    gateway_id INT NOT NULL,
    storage_id INT NOT NULL,
    FOREIGN KEY (gateway_id) REFERENCES gateway (id),
    FOREIGN KEY (storage_id) REFERENCES storage (id)
);

-- Inserting data into owner table
INSERT INTO owner (username, password, email, first_name, last_name) VALUES
('user1', 'pass1', 'user1@example.com', 'John', 'Doe'),
('user2', 'pass2', 'user2@example.com', 'Jane', 'Smith'),
('user3', 'pass3', 'user3@example.com', 'Bob', 'Johnson');

-- Inserting data into gateway table
INSERT INTO gateway (owner_id) VALUES
(1),  -- Owner ID for user1
(2),  -- Owner ID for user2
(3);  -- Owner ID for user3

-- Inserting data into seed_types table
INSERT INTO seed_types (lower_bound, upper_bound, name) VALUES
(10, 20, 'Type A'),
(21, 30, 'Type B'),
(31, 40, 'Type C');

-- Inserting data into storage table
INSERT INTO storage (address, owner_id, seed_types_id) VALUES
('Storage Location 1', 1, 1),  -- Owner ID for user1, Seed Type ID for Type A
('Storage Location 2', 2, 2),  -- Owner ID for user2, Seed Type ID for Type B
('Storage Location 3', 3, 3);  -- Owner ID for user3, Seed Type ID for Type C

-- Inserting data into stick table
INSERT INTO stick (gateway_id, storage_id) VALUES
(1, 1),  -- Gateway ID for user1, Storage ID for Storage Location 1
(2, 2),  -- Gateway ID for user2, Storage ID for Storage Location 2
(3, 3);  -- Gateway ID for user3, Storage ID for Storage Location 3

-- Inserting data into entry table
INSERT INTO entry (send_id, height_level, stick_id, temp, time) VALUES
(101, 15, 1, 25, '2023-01-01 12:00:00'),
(102, 25, 2, 28, '2023-01-02 14:30:00'),
(103, 35, 3, 22, '2023-01-03 10:45:00');

select * from seed_types;