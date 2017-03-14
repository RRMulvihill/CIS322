begin;
INSERT INTO roles (role) VALUES ('Logistics Officer');
INSERT INTO roles (role) VALUES ('Facilities Officer');

INSERT INTO users (username,password,role_fk) VALUES ('logof1','pass',1);
INSERT INTO users (username,password,role_fk) VALUES ('facof1','pass',2);

INSERT INTO facilities (fac_name,fac_code) VALUES ('Headquarters','hq');
INSERT INTO facilities (fac_name,fac_code) VALUES ('fac1','f1');

INSERT INTO assets (asset_tag,description,fac_fc,disposed) VALUES ('1','thing1',1,'f');
INSERT INTO assets (asset_tag,description,fac_fc,disposed) VALUES ('2','thing2',2,'f');

end;
