CREATE OR REPLACE FUNCTION register_user(user_name TEXT, user_email TEXT, user_pwd)
RETURNS integer AS
$$
INSERT INTO dev.users (user_name, email, password) VALUES (user_name, user_email, user_pwd)
RETURNING user_id;
$$
LANGUAGE 'sql' VOLATILE;
