DROP TABLE IF EXISTS public_organizations;
CREATE TABLE public_organizations (
organization TEXT,
org_id INT, 
photo_url TEXT,
zipcode TEXT, 
phone TEXT, 
website TEXT);
-- here service will be a int, other services restricted to 1 for testing, 
-- date will be MM-DD-YYYY, time is 24 hr, days is days of week with hyphens 
-- so monday only to replicate boolean array in postgres(F-T-F-F-F-F-F), 
DROP TABLE IF EXISTS public_offerings;
CREATE TABLE public_offerings (org_id int, off_id int, service int, other_services int,
 people_group int, description text, start_time int, end_time int, start_date text,
 end_date text, days text);
-- 
DROP TABLE IF EXISTS public_zipcodes;
CREATE TABLE public_zipcodes (zipcode int, city text, state text);
--
DROP TABLE IF EXISTS public_services;
CREATE TABLE public_services (service_id int, service text);
--
DROP TABLE IF EXISTS public_people_groups;
CREATE TABLE public_people_groups (group_id int, people_group text);
--
-- test case
--
INSERT INTO public_zipcodes VALUES (07055, 'Passaic', 'NJ');

INSERT INTO public_services VALUES (1, 'Pantry');

INSERT INTO public_services VALUES (0, 'None');

INSERT INTO public_people_groups VALUES (1, 'Children');

INSERT INTO public_organizations VALUES ('Passaic YMC', 1, 'photo.com', '07055', 
'123-456-7890', 'temp.com');

INSERT INTO public_offerings VALUES (1, 1, 1, 0, 1, 'description', 9, 12, '01-01-2018', '02-01-2018', 'F-T-F-F-F-F-F');