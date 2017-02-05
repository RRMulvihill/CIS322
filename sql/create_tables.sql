CREATE TABLE products (
  product_pk  integer,
  vendor varchar(50),
  description varchar(128),
  alt_description varchar(128)
);

CREATE TABLE assets (
  assets_pk integer,
  product_fk integer,
  asset_tag varchar(50),
  description varchar(128),
  alt_description varchar(128)
);

CREATE TABLE vehicles(
  vehicle_pk  integer,
  asset_fk  integer
);

CREATE TABLE facilities (
  facility_pk integer,
  fcode varchar(50),
  common_name varchar(50),
  location  varchar(50)
);

CREATE TABLE asset_at (
  asset_fk  integer,
  facility_fk integer,
  arrive_dt timestamp DEFAULT current_timestamp,
  depart_dt timestamp DEFAULT current_timestamp
);

CREATE TABLE convoys (
  convoy_pk integer,
  request varchar(128),
  source_fk integer,
  dest_fk integer,
  arrive_dt timestamp DEFAULT current_timestamp,
  depart_dt timestamp DEFAULT current_timestamp
);

CREATE TABLE used_by (
  vehicle_fk  integer,
  convoy_fk integer
);

CREATE TABLE asset_on (
  asset_fk  integer,
  convoy_fk integer,
  load_dt timestamp DEFAULT current_timestamp,
  unload_dt timestamp DEFAULT current_timestamp
);
  
CREATE TABLE users (
    user_pk integer,
    username varchar(20),
    active  boolean
);  

CREATE TABLE roles (
  role_pk integer,
  title varchar(50)
);

CREATE TABLE user_is (
  user_fk integer,
  role_fk integer
);

CREATE TABLE user_supports (
  user_fk integer,
  facility_fk integer
);

CREATE TABLE levels (
  level_pk  integer,
  abbr  varchar(50),
  comment text
);  

CREATE TABLE compartments (
  compartment_pk integer,
  abbr  varchar(50),
  comment text
);

CREATE TABLE security_tags (
  tag_pk  integer,
  level_fk  integer,
  compartment_fk  integer,
  user_fk integer,
  product_fk  integer,
  asset_fk  integer
);  
