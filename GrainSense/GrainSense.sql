drop database if exists GrainSenseDB;

create database if not exists GrainSenseDB;

use GrainSenseDB;

CREATE TABLE if not exists entry (
    id int NOT NULL auto_increment,
    send_id int NOT NULL,
    height_level int NOT NULL,
    stick_id int NOT NULL,
    temp int NOT NULL,
    time timestamp NOT NULL,
    CONSTRAINT sensor_pk PRIMARY KEY (id)
);

CREATE TABLE if not exists gateway (
    id int NOT NULL auto_increment,
    owner_id int NOT NULL,
    CONSTRAINT gateway_pk PRIMARY KEY (id)
);

CREATE TABLE if not exists owner (
    id int NOT NULL auto_increment,
    username varchar(45) NOT NULL,
    password varchar(45) NOT NULL,
    email varchar(100) NOT NULL,
    first_name varchar(45) NOT NULL,
    last_name varchar(45) NOT NULL,
    CONSTRAINT owner_pk PRIMARY KEY (id)
);

CREATE TABLE if not exists seed_types (
    id int NOT NULL auto_increment,
    lower_bound int NOT NULL,
    upper_bound int NOT NULL,
    name varchar(45) NOT NULL,
    CONSTRAINT seed_types_pk PRIMARY KEY (id)
);

CREATE TABLE if not exists stick (
    id int NOT NULL auto_increment,
    gateway_id int NOT NULL,
    storage_id int NOT NULL,
    CONSTRAINT stick_pk PRIMARY KEY (id)
);

CREATE TABLE if not exists storage (
    id int NOT NULL auto_increment,
    address varchar(100) NOT NULL,
    owner_id int NOT NULL,
    seed_types_id int NOT NULL,
    CONSTRAINT storage_pk PRIMARY KEY (id)
);

ALTER TABLE gateway ADD CONSTRAINT gateway_owner FOREIGN KEY gateway_owner (owner_id)
    REFERENCES owner (id);

ALTER TABLE entry ADD CONSTRAINT sensor_stick FOREIGN KEY sensor_stick (stick_id)
    REFERENCES stick (id);

ALTER TABLE stick ADD CONSTRAINT stick_gateway FOREIGN KEY stick_gateway (gateway_id)
    REFERENCES gateway (id);

ALTER TABLE stick ADD CONSTRAINT stick_storage FOREIGN KEY stick_storage (storage_id)
    REFERENCES storage (id);

ALTER TABLE storage ADD CONSTRAINT storage_owner FOREIGN KEY storage_owner (owner_id)
    REFERENCES owner (id);

ALTER TABLE storage ADD CONSTRAINT storage_seed_types FOREIGN KEY storage_seed_types (seed_types_id)
    REFERENCES seed_types (id);
