#!/bin/bash

wget -q https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz && \
tar xfz geckodriver-v0.24.0-linux64.tar.gz && \
sudo mv geckodriver /usr/local/bin && \
rm geckodriver-v0.24.0-linux64.tar.gz && \

echo "\n Geckodriver de Firefox instalado correctamente en /usr/local/bin \n"
