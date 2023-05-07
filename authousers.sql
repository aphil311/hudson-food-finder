DROP TABLE IF EXISTS authorizedusers;

CREATE TABLE authorizedusers (
	username TEXT,
	organization TEXT
);

INSERT INTO authorizedusers (username, organization) VALUES ('zainahmed1956@gmail.com', '%');
INSERT INTO authorizedusers (username, organization) VALUES ('yousefamin800@gmail.com', '%');
INSERT INTO authorizedusers (username, organization) VALUES ('aidantphil21@gmail.com', '%');
