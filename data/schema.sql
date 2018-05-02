
use ctx_server;

create table servers (
    server_id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    server_ipaddr VARCHAR(64) NOT NULL,
    server_name VARCHAR(64)
);

create table users (
    user_id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(64) NOT NULL,
    full_name VARCHAR(64),
    contact_info VARCHAR(128)
);

create table logins (
    login_id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    login_time DATETIME NOT NULL,
    user_id INTEGER NOT NULL REFERENCES(user.user_id),
    server_id INTEGER NOT NULL REFERENCES(server.server_id)
)

-- TODO: SQL views
-- logins join users join servers
-- logins join servers count users
-- users join logins max last_logged_in_at=login_date, last_logged_into=server_name
