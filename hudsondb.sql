DROP TABLE IF EXISTS public_organizations;
CREATE TABLE public_organizations (
org_id INTEGER PRIMARY KEY,
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
DROP TABLE IF EXISTS public_offerings;
CREATE TABLE public_offerings (
off_id INTEGER PRIMARY KEY,
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
DROP TABLE IF EXISTS public_zip_codes;
CREATE TABLE public_zip_codes (
zip_code TEXT NOT NULL,
city TEXT NOT NULL,
abr_state TEXT NOT NULL);
--
DROP TABLE IF EXISTS public_services;
CREATE TABLE public_services (
service_id INT PRIMARY KEY,
service_type TEXT NOT NULL);
--
DROP TABLE IF EXISTS public_people_groups;
CREATE TABLE public_people_groups (
group_id int PRIMARY KEY,
people_group TEXT NOT NULL);
---
DROP TABLE IF EXISTS public_ownership;
CREATE TABLE public_ownership (
org_id INT NOT NULL,
off_id INT NOT NULL);
--
-- test cases
--
INSERT INTO public_organizations (org_name, phone, website, 
photo_url, street, zip_code, services) 
VALUES ('Heavens Gate Christian Fellowship', '2016006557',
'https://www.facebook.com/HGCFPHOP/', '/static/img/HeavensGate.jpg',
'170 Paulison Ave', '07055', '0'), 
('United Passiac Organization', '8628885525',
'https://unitedpassaic.com', '/static/img/UnitedPassaic.jpg',
'163 Autumn St', '07055', '0'),
('Elijahs Promise', '7325459002',
'https://elijahspromise.org', '/static/img/ElijahsPromise.jpg',
'18 Neilson Street', '08901', '0'),
('Boston Public Market', '6179734909',
'https://bostonpublicmarket.org', '/static/img/BostonPublicMarket.jpg',
'523 Chestnut St', '07083', '0');

INSERT INTO public_offerings (title, days_open, days_desc, start_time,
end_time, init_date, close_date, off_service, group_served, off_desc)
VALUES 
('Monthly Food Pantry', 'F-F-T-F-F-F-F', 'Third Friday of the month', 
'7:30', '12:00', '03-26-2023',
NULL, 0, 2, 'description'),
('United Passiac Organization', 'F-T-T-T-T-T-F', NULL, '15:30', '19:00', '03-26-2023',
'07-01-2023', 0, 1, 'description'),
('Elijahs Promise', 'F-T-T-T-T-T-F', NULL, '17:00', '22:00', '03-26-2023',
'06-01-2023', 1, 3, 'description'),
('Elijahs Promise', 'F-T-T-T-T-T-F', NULL, '12:00', '23:59', '03-26-2023',
'06-01-2023', 1, 4, 'description'),
('Boston Public Market', 'T-T-T-T-T-T-T', NULL, '9:00', '17:00', '03-26-2023', 
NULL, 3, 0, 'description');

INSERT INTO public_zip_codes (zip_code, city, abr_state) VALUES
('07055', 'Passaic', 'NJ'),
('07083', 'New Brunswick', 'MA'),
('08901', 'Union', 'NJ');

INSERT INTO public_services (service_id, service_type) VALUES
(0, 'Food Pantry'),
(1, 'Soup Kitchen'),
(2, 'Groceries (SNAP)'),
(3, 'Restaurant (SNAP)');

INSERT INTO public_people_groups (group_id, people_group) VALUES
(0, 'All'),
(1, 'Children'),
(2, 'Adults'),
(3, 'Families'),
(4, 'Seniors');

INSERT INTO public_ownership (org_id, off_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(3, 4),
(4, 5);

SELECT public_organizations.org_name, public_offerings.title,
public_offerings.days_open, public_offerings.start_time,
public_offerings.end_time, public_offerings.init_date,
public_offerings.close_date, public_services.service_type,
public_people_groups.people_group, public_offerings.off_desc
FROM public_ownership, public_offerings, public_organizations,
public_services, public_people_groups
WHERE public_ownership.org_id = public_organizations.org_id AND
public_ownership.off_id = public_offerings.off_id AND
public_offerings.off_service = public_services.service_id AND
public_offerings.group_served = public_people_groups.group_id;

-- SELECT * FROM public_organizations;