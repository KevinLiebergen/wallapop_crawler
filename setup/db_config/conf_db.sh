#!/bin/bash

sudo mysql -u root < db_config/create_user.sql 2>&1 | grep -v "Using a password"

if [ $? -eq 1 ];
then
	echo "\nCreado usuario 'walla_user' con contraseña 'walla_password', IMPORTANTE!!!"
fi

sudo mysql -u root < db_config/create_db.sql 

 if [ $? -eq 1 ];
 then
     echo "\nCreado usuario  Base de datos 'wallapop_db'"
 fi


mysql -u walla_user -pwalla_password < db_config/create_tb.sql 2>&1 | grep -v "Using a password"
if [ $? -eq 1 ];
then
	echo "\nCreadas las tablas de la base de datos 'wallapop_db'"
fi

echo ""
