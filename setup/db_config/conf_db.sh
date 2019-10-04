#!/bin/bash

mysql -uroot -proot < db_config/create_db.sql 2>&1 | grep -v "Using a password"

if [ $? -eq 1 ];
then
	echo "\nCreado usuario 'walla_user' y Base de datos 'wallapop_db'"
fi


mysql -uwalla_user -pwalla_user < db_config/create_tb.sql 2>&1 | grep -v "Using a password"
if [ $? -eq 1 ];
then
	echo "\nCreadas las tablas de la base de datos 'wallapop_db'"
fi

echo ""
