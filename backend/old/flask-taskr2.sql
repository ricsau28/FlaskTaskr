/*flask-taskr.sql */

/* CREATE ROLE flasktaskr2 LOGIN PASSWORD 'flasktaskr2' VALID UNTIL '2-10-2020';
CREATE DATABASE flasktaskr2 OWNER flasktaskr2;
REVOKE CONNECT ON DATABASE flasktaskr2 FROM PUBLIC;
REVOKE CONNECT ON DATABASE postgres FROM PUBLIC;    #disallow users from viewing postgres db
*/

CREATE SCHEMA flasktaskr2;
CREATE TABLE users (user_id SERIAL PRIMARY KEY, user_name TEXT NOT NULL);
CREATE TABLE tasks (task_id SERIAL PRIMARY KEY, user_id integer NOT NULL, name TEXT NOT NULL, due_date TEXT NOT NULL, priority INTEGER NOT NULL, status INTEGER NOT NULL);

ALTER TABLE users ADD CONSTRAINT users_unique UNIQUE (user_name);
ALTER TABLE tasks ADD FOREIGN KEY (user_id) REFERENCES users;

 
