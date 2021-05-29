#!/bin/bash


which geckodriver > /dev/null

if [ $? -eq 1 ];
then

	echo "\n[+] Instalando Firefox geckodriver..."

	wget -q https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz && \
	tar xfz geckodriver-v0.29.1-linux64.tar.gz && \
	sudo mv geckodriver /usr/local/bin && \
	rm geckodriver-v0.29.1-linux64.tar.gz* && \

	echo "\n[+] Geckodriver de Firefox instalado correctamente en /usr/local/bin"

else
	echo "[+] Geckodriver ya instalado, omitiendo este paso..."

fi
