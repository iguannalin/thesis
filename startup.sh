sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-pip

sudo apt install --upgrade python3-setuptools

sudo apt install python3.11-venv
python -m venv env --system-site-packages

source env/bin/activate

sudo apt-get install python3-flask

cd ~
pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo -E env PATH=$PATH python3 raspi-blinka.py

ls /dev/i2c* /dev/spi*