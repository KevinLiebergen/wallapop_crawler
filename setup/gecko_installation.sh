#!/bin/bash


which geckodriver > /dev/null

if [ $? -eq 1 ];
then

	wget -q https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz && \
	tar xfz geckodriver-v0.24.0-linux64.tar.gz && \
	sudo mv geckodriver /usr/local/bin && \
	rm geckodriver-v0.24.0-linux64.tar.gz* && \

	echo "\nGeckodriver de Firefox instalado correctamente en /usr/local/bin"

else
	echo "\nGeckodriver ya instalado, omitiendo este paso..."

fi
