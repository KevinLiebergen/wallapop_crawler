#!/bin/bash

which firefox > /dev/null

if [ $? -ne 0 ];
then
	echo "\n[+] Instalando Firefox..."
    sudo apt-get install -y firefox > /dev/null 2>&1

    if [ $? -ne 1 ];
    then
	    sudo apt-get install -y firefox-esr > /dev/null 2>&1
	   	if [ $? -eq 0 ];
		then
			echo "\n[+] Firefox-esr instalado..."
		else
			echo "\n\033[91m[+] Fallo al instalar Firefox...\033[0m"
		fi
    else
	    echo "\n[+] Firefox instalado...\n"
    fi

else
    echo "[+] Firefox ya instalado, omitiendo..."
fi
