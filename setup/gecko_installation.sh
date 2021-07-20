#!/bin/bash


which geckodriver > /dev/null

if [ $? -eq 1 ];
then

	echo "\n[+] Instalando Chrome driver..."

  # Al principio tenia firefoex geckodriver, por problemas de compatibilidad con raspberry lo cambie a chrome
	# wget -q https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz && \
	# tar xfz geckodriver-v0.29.1-linux64.tar.gz && \
	# sudo mv geckodriver /usr/local/bin && \
	# rm geckodriver-v0.29.1-linux64.tar.gz* && \

  # Probado con raspberry, no con ubuntu
	sudo apt install chromium-chromedriver

	echo "\n[+] Chrome driver instalado correctamente "

else
	echo "[+] Chrome driver ya instalado, omitiendo este paso..."

fi
