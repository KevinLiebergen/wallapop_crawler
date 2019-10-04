CREATE USER IF NOT EXISTS 'walla_user'@'localhost' IDENTIFIED BY 'walla_user';

GRANT ALL PRIVILEGES ON wallapop_db.* TO 'walla_user'@'localhost';

CREATE DATABASE wallapop_db;
