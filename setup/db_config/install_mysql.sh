#!/bin/bash

which mysql > /dev/null

if [ $? -eq 1 ];
then
	echo "\n[+] Determinando instalar MySQL o MariaDB..."
	sudo apt-get install -y mysql-server > /dev/null 2>&1
	if [ $? -eq 0 ];
	then
		echo "\n[+] MySQL instalado correctamente"
	else
		echo "\n[+] MySql no se encuentra en los repositorios APT, probando con MariaDB"
		sudo apt-get install -y mariadb-server > /dev/null 2>&1

		if [ $? -eq 0 ];
		then
			echo "\n[+] MariaDB instalado correctamente..."
		else
			echo "\n[+] Error al instalar MariaDB..."
		fi
	fi
	
else
	echo "\n[+] MySQL ya instalado, omitiendo..."
fi
