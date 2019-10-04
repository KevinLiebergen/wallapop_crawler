#!/bin/bash

which mysql > /dev/null

if [ $? -eq 1 ];
then
	sudo apt update > /dev/null 2>&1
	sudo apt install mysql-server > /dev/null 2>&1
	echo "\nMySQL instalado correctamente"
else
	echo "\nMySQL ya instalado, omitiendo..."
fi
