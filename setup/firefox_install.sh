#!/bin/bash

which firefox > /dev/null

if [ $? -ne 0 ];
then
	echo "\nInstalando Firefox..."
    sudo apt-get install firefox > /dev/null 2>&1

    if [ $? -ne 1 ];
    then
	    sudo apt-get install firefox-esr > /dev/null 2>&1
	   	if [ $? -eq 0 ];
		then
			echo "\nFirefox-esr instalado..."
		else
			echo "\nFallo al instalar Firefox..."
		fi
    else
	    echo "\nFirefox instalado...\n"
    fi

else
    echo "\nFirefox ya instalado, omitiendo..."
fi
