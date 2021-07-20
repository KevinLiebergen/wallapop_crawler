#!/bin/bash

which chromium-browser > /dev/null

if [ $? -ne 0 ];
then
	echo "\n[+] Instalando Chrome..."
    sudo apt-get install -y chromium-browser > /dev/null 2>&1

    if [ $? -ne 1 ];
    then
	    sudo apt-get install -y chromium-browser > /dev/null 2>&1
	   	if [ $? -eq 0 ];
		then
			echo "\n[+] Chrome instalado..."
		else
			echo "\n\033[91m[+] Fallo al instalar Chrome...\033[0m"
		fi
    else
	    echo "\n[+] Chrome instalado...\n"
    fi

else
    echo "[+] Chrome ya instalado, omitiendo..."
fi
