#!/bin/bash


echo "[+] Actualizando repositorios..."
sudo apt-get update > /dev/null

sh chrome_install.sh

sh gecko_installation.sh

sh db_config/install_mysql.sh

sh db_config/conf_db.sh
