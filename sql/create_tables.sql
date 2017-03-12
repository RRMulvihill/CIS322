Create TABLE roles (
	role_pk serial primary key,
	role varchar(18)
);
--the role feild will be either "logistics officer" or "facilities officer" so it only needs 18 characters
--its pk will be used by users, this will kelp minimalize typos and time typing out roles
CREATE TABLE users (
	user_pk serial primary key,
	username varchar(16),
	password varchar(16),
	role_fk integer REFERENCES roles(role_pk)
);
--I have now added a pk to users for requests
--sessons will use the username not an integer id.
--The varchar feilds are corresponding to the assignemnt instructions "no longer than 16 characters"

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
	asset_pk serial primary key,
	asset_tag varchar(16),
	description text,
	fac_fk integer REFERENCES facilities(fac_pk),
	status_fk integer REFERENCES asset_at(status_pk)
);
--asset_pk added for requests
--potentialy status_fk could be a boolean to handle disposed elements

CREATE TABLE requests (
	req_pk serial primary key,
	submitter_fk integer REFERENCES users(user_pk),
	req_tag varchar(16),
	submit_dt timestamp,
	source_fk integer REFERENCES facilities(fac_pk),
	destination_fk integer REFERENCES facilities(fac_pk),
	asset_fk integer REFERENCES assets(asset_pk),
	approver_fk integer REFERENCES users(user_pk),
	approved_dt timestamp
	aprroved boolean
);
-- I created a tag for requests for users to select wich request they are accepting
--I used foriegn keys heavily, adding the pk's for assignment8
--these will connect tables without fear of spelling errors or redundantcy
--I decided to keep all fo my transit information inside of my request to make the verly long req_approval more simple

CREATE TABLE transit (
	req_fk integer REFERENCES requests(req_pk),
	source_fk integer REFERENCES facilities(fac_pk),
	destination_fk integer REFERENCES facilities(fac_pk),
	load_dt timestamp,
	unload_dt timestamp
);
--the fk is ussed to link transit with requests,
--all other info is the basic feilds from the description

--initialize database with roles and statuses 
INSERT INTO roles (role) VALUES ('Logistics Officer');
INSERT INTO roles (role) VALUES ('Facilities Officer');
INSERT INTO asset_at (status) VALUES ('at_facility');
INSERT INTO asset_at (status) VALUES ('disposed');
