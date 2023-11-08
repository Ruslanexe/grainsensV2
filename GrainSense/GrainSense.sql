CREATE TABLE entry (
    id INT NOT NULL IDENTITY(1,1),
    send_id INT NOT NULL,
    height_level INT NOT NULL,
    stick_id INT NOT NULL,
    temp INT NOT NULL,
    time DATETIME2 NOT NULL,
    CONSTRAINT sensor_pk PRIMARY KEY (id)
);

CREATE TABLE gateway (
    id INT NOT NULL IDENTITY(1,1),
    owner_id INT NOT NULL,
    CONSTRAINT gateway_pk PRIMARY KEY (id)
);

CREATE TABLE owner (
    id INT NOT NULL IDENTITY(1,1),
    username NVARCHAR(45) NOT NULL,
    password NVARCHAR(45) NOT NULL,
    email NVARCHAR(100) NOT NULL,
    first_name NVARCHAR(45) NOT NULL,
    last_name NVARCHAR(45) NOT NULL,
    CONSTRAINT owner_pk PRIMARY KEY (id)
);

CREATE TABLE seed_types (
    id INT NOT NULL IDENTITY(1,1),
    lower_bound INT NOT NULL,
    upper_bound INT NOT NULL,
    name NVARCHAR(45) NOT NULL,
    CONSTRAINT seed_types_pk PRIMARY KEY (id)
);

CREATE TABLE stick (
    id INT NOT NULL IDENTITY(1,1),
    gateway_id INT NOT NULL,
    storage_id INT NOT NULL,
    CONSTRAINT stick_pk PRIMARY KEY (id)
);

CREATE TABLE storage (
    id INT NOT NULL IDENTITY(1,1),
    address NVARCHAR(100) NOT NULL,
    owner_id INT NOT NULL,
    seed_types_id INT NOT NULL,
    CONSTRAINT storage_pk PRIMARY KEY (id)
);

ALTER TABLE gateway ADD CONSTRAINT gateway_owner FOREIGN KEY (owner_id)
    REFERENCES owner (id);

ALTER TABLE entry ADD CONSTRAINT sensor_stick FOREIGN KEY (stick_id)
    REFERENCES stick (id);

ALTER TABLE stick ADD CONSTRAINT stick_gateway FOREIGN KEY (gateway_id)
    REFERENCES gateway (id);

ALTER TABLE stick ADD CONSTRAINT stick_storage FOREIGN KEY (storage_id)
    REFERENCES storage (id);

ALTER TABLE storage ADD CONSTRAINT storage_owner FOREIGN KEY (owner_id)
    REFERENCES owner (id);

ALTER TABLE storage ADD CONSTRAINT storage_seed_types FOREIGN KEY (seed_types_id)
    REFERENCES seed_types (id);
