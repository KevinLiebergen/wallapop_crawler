#!/bin/bash

which firefox > /dev/null

if [ $? -ne 0 ];
then
	echo "\n[+] Instalando Firefox..."
    sudo apt-get install firefox > /dev/null 2>&1

    if [ $? -ne 1 ];
    then
	    sudo apt-get install firefox-esr > /dev/null 2>&1
	   	if [ $? -eq 0 ];
		then
			echo "\n[+] Firefox-esr instalado..."
		else
			echo "\n[+] Fallo al instalar Firefox..."
		fi
    else
	    echo "\n[+] Firefox instalado...\n"
    fi

else
    echo "[+] Firefox ya instalado, omitiendo..."
fi
