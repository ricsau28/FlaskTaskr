/*flasktaskr.sql */

CREATE ROLE flasktaskr LOGIN PASSWORD 'flasktaskr' VALID UNTIL '2-10-2020';
CREATE DATABASE flasktaskr OWNER flasktaskr;

/* TODO For production: CREATE SCHEMA flasktaskr; */

\c flasktaskr;

CREATE SCHEMA dev;
CREATE TABLE dev.users (user_id SERIAL PRIMARY KEY, user_name TEXT NOT NULL);
CREATE TABLE dev.tasks (task_id SERIAL PRIMARY KEY, user_id integer NOT NULL, name TEXT NOT NULL, due_date TEXT NOT NULL, priority INTEGER NOT NULL, status INTEGER NOT NULL);

ALTER TABLE dev.users ADD CONSTRAINT users_unique UNIQUE (user_name);
ALTER TABLE dev.tasks ADD FOREIGN KEY (user_id) REFERENCES dev.users;

GRANT ALL ON SCHEMA dev TO flasktaskr;

REVOKE CONNECT ON DATABASE flasktaskr FROM PUBLIC;
/* REVOKE CONNECT ON DATABASE postgres FROM PUBLIC;    #disallow users from viewing postgres db */
