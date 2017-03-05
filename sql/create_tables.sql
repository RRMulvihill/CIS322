
Create TABLE roles (
	role_pk serial primary key,
	role varchar(18)
);
--the role feild will be either "logistics officer" or "facilities officer" so it only needs 18 characters
--its pk will be used by users, this will kelp minimalize typos and time typing out roles
CREATE TABLE users (
	username varchar(16),
	password varchar(16),
	role_fk integer REFERENCES roles(role_pk)
);
--I chose not to give a primary key at this time as it is not needed, 
--sessons will use the username not an integer id.
--I am creating code that fufills the requsted output,
--so my code is streamlined and not burdened with currenlty unecessary code.
--The varchar feilds are corresponding to the assignemnt instructions "no longer than 16 characters"

);
CREATE TABLE asset_at (
	status_pk serial primary key,
	status varchar(16)
);
--tracks the state of the asset, initialized to hold  "at facility" and "disposed"
--todo: change this table to a boolean status for assets
CREATE TABLE facilities (
	fac_pk serial primary key,
	fac_name varchar(32),
	fac_code varchar(6)
);
--pk is used by assets, I am considering initializing a "disposed" facility to eliminate the asset_at table
CREATE TABLE assets (
	asset_tag varchar(16),
	description text,
	fac_fk integer REFERENCES facilities(fac_pk),
	status_fk integer REFERENCES asset_at(status_pk)
--potentialy status_fk could be a boolean to handle disposed elements

--initialize database with roles and statuses 
INSERT INTO roles (role) VALUES ('Logistics Officer');
INSERT INTO roles (role) VALUES ('Facilities Officer');
INSERT INTO asset_at (status) VALUES ('at_facility');
INSERT INTO asset_at (status) VALUES ('disposed');
