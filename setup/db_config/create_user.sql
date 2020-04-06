CREATE USER IF NOT EXISTS 'walla_user'@'localhost' IDENTIFIED BY 'walla_password';

GRANT ALL PRIVILEGES ON wallapop_db.* TO 'walla_user'@'localhost';

