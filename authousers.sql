DROP TABLE IF EXISTS authorized_users;

CREATE TABLE authorized_users (
	username TEXT,
	organization TEXT
);

INSERT INTO authorized_users (username, organization) VALUES ('zainahmed1956@gmail.com', '%');
INSERT INTO authorized_users (username, organization) VALUES ('yousefamin800@gmail.com', '%');
INSERT INTO authorized_users (username, organization) VALUES ('aidantphil21@gmail.com', '%');
