DROP TABLE IF EXISTS organizations;
CREATE TABLE organizations (
org_id SERIAL PRIMARY KEY,
org_name TEXT, 
phone TEXT,
website TEXT,
photo_url TEXT,
street TEXT,
zip_code TEXT,
services TEXT);
-- here service will be a int, other services restricted to 1 for testing, 
-- date will be MM-DD-YYYY, time is 24 hr, days is days of week with hyphens 
-- so monday only to replicate boolean array in postgres(F-T-F-F-F-F-F), 
DROP TABLE IF EXISTS offerings;
CREATE TABLE offerings (
off_id SERIAL PRIMARY KEY,
title TEXT,
days_open TEXT,
days_desc TEXT,
start_time TEXT,
end_time TEXT,
init_date TEXT,
close_date TEXT,
off_service INT,
group_served INT,
off_desc TEXT);
-- 
DROP TABLE IF EXISTS zip_codes;
CREATE TABLE zip_codes (
zip_code TEXT NOT NULL,
city TEXT NOT NULL,
abr_state TEXT NOT NULL);
--
DROP TABLE IF EXISTS services;
CREATE TABLE services (
service_id INT PRIMARY KEY,
service_type TEXT NOT NULL);
--
DROP TABLE IF EXISTS people_groups;
CREATE TABLE people_groups (
group_id SERIAL PRIMARY KEY,
people_group TEXT NOT NULL);
---
DROP TABLE IF EXISTS org_ownership;
CREATE TABLE org_ownership (
org_id INT NOT NULL,
off_id INT NOT NULL);
--
-- test cases
--
INSERT INTO organizations (org_name, phone, website, 
photo_url, street, zip_code, services) 
VALUES ('Heavens Gate Christian Fellowship', '2016006557',
'https://www.facebook.com/HGCFPHOP/', './static/img/HeavensGate.jpeg',
'170 Paulison Ave', '07055', '0'), 
('United Passiac Organization', '8628885525',
'https://unitedpassaic.com', './static/img/UnitedPassiac.png',
'163 Autumn St', '07055', '0'),
('Elijahs Promise', '7325459002',
'https://elijahspromise.org', './static/img/ElijahsPromise.jpeg',
'18 Neilson Street', '08901', '0'),
('Boston Public Market', '6179734909',
'https://bostonpublicmarket.org', '/static/img/BostonPublicMarket.jpeg',
'523 Chestnut St', '07083', '0');

INSERT INTO offerings (title, days_open, days_desc, start_time,
end_time, init_date, close_date, off_service, group_served, off_desc)
VALUES 
('Monthly Food Pantry', 'F-F-T-F-F-F-F', 'Third Friday of the month', 
'7:30', '12:00', '03-26-2023',
NULL, 0, 3, 'description'),
('United Passiac Organization', 'F-T-T-T-T-T-F', NULL, '15:30', '19:00', '03-26-2023',
'07-01-2023', 0, 2, 'description'),
('Elijahs Promise', 'F-T-T-T-T-T-F', NULL, '17:00', '22:00', '03-26-2023',
'06-01-2023', 1, 4, 'description'),
('Elijahs Promise', 'F-T-T-T-T-T-F', NULL, '12:00', '23:59', '03-26-2023',
'06-01-2023', 1, 5, 'description'),
('Boston Public Market', 'T-T-T-T-T-T-T', NULL, '9:00', '17:00', '03-26-2023', 
NULL, 3, 1, 'description');

INSERT INTO zip_codes (zip_code, city, abr_state) VALUES
('07055', 'Passiac', 'NJ'),
('07083', 'New Brunswick', 'MA'),
('08901', 'Union', 'NJ');

INSERT INTO services (service_id, service_type) VALUES
(0, 'Food Pantry'),
(1, 'Soup Kitchen'),
(2, 'Groceries (SNAP)'),
(3, 'Restaurant (SNAP)');

INSERT INTO people_groups (people_group) VALUES
('All'),
('Children'),
('Adults'),
('Families'),
('Seniors');

INSERT INTO org_ownership (org_id, off_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(3, 4),
(4, 5);

-- SELECT public_organizations.photo_url, public_organizations.street, 
-- public_offerings.days_open, public_offerings.start_time 
-- FROM public_organizations, public_offerings, public_ownership
-- WHERE public_ownership.off_id = public_offerings.off_id AND 
-- public_ownership.org_id = public_organizations.org_id
-- ORDER BY public_offerings.start_time;

-- SELECT * FROM public_organizations;