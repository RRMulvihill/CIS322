CREATE TABLE users (
	username varchar(16),
	password varchar(16),
	role_fk integer
);
--I chose not to give a primary key at this time as it is not needed, 
--sessons will use the username not an integer id.
--I am creating code that fufills the requsted output,
--so my code is streamlined and not burdened with currenlty unecessary code.
--The varchar feilds are corresponding to the assignemnt instructions "no longer than 16 characters"
Create TABLE roles (
	role_pk integer,
	role varchar(25)
);
CREATE TABLE assets (
	asset_tag varchar(16),
	description text
	facility_fk integer,
	status integer
);
CREATE TABLE asset_at (
	status_pk serial primary key,
	status varchar(16)
);
CREATE TABLE facilities (
	fac_pk serial primary key,
	fac_name varchar(32),
	fac_code varchar(6)
);
