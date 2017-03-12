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
	disposed boolean
);
--asset_pk added for requests
-- disposed boolean created to remove assets_at table

CREATE TABLE requests (
	req_pk serial primary key,
	submitter_fk integer REFERENCES users(user_pk),
	submit_dt timestamp,
	source_fk integer REFERENCES facilities(fac_pk),
	destination_fk integer REFERENCES facilities(fac_pk),
	asset_fk integer REFERENCES assets(asset_pk),
	approver_fk integer REFERENCES users(user_pk),
	approved_dt timestamp,
	approved boolean
);
-- I created a pk for requests for users to select wich request they are accepting and to link to transit
--I used foriegn keys heavily, adding the pk's for assignment8
--these will connect tables without fear of spelling errors or redundantcy
--I decided to keep all fo my transit information inside of my request to make the verly long req_approval more simple

CREATE TABLE transits (
	req_fk integer REFERENCES requests(req_pk),
	asset_fk integer REFERENCES assets(asset_pk),
	source_fk integer REFERENCES facilities(fac_pk),
	destination_fk integer REFERENCES facilities(fac_pk),
	load_dt timestamp,
	unload_dt timestamp
);
--the fk is used to link transit with requests,
--all other info is the basic feilds from the description

--initialize database with roles and statuses 
INSERT INTO roles (role) VALUES ('Logistics Officer');
INSERT INTO roles (role) VALUES ('Facilities Officer');
