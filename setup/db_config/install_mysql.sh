#!/bin/bash

which mysql > /dev/null

if [ $? -eq 1 ];
then
	echo "\nDeterminando instalar MySQL o MariaDB..."
	sudo apt-get install mysql-server > /dev/null 2>&1
	if [ $? -eq 0 ];
	then
		echo "\nMySQL instalado correctamente"
	else
		sudo apt-get install -y mariadb-server > /dev/null 2>&1

		if [ $? -eq 0 ];
		then
			echo "\nMariaDB instalado correctamente..."
		else
			echo "\nError al instalar MySQL..."
		fi
	fi
	
else
	echo "\nMySQL ya instalado, omitiendo..."
fi
