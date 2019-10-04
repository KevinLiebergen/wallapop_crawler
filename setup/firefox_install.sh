#!/bin/bash

dpkg -s firefox | grep " ok installed" > /dev/null

if [ $? -eq 1 ];
then
    echo "\nInstalando Firefox...\n"
    sudo apt install firefox
else
    echo "\nFirefox ya instalado, omitiendo..."
fi
