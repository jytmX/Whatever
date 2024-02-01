#!/bin/bash

sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.10

curl https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
sudo python3.10 /tmp/get-pip.py
rm /tmp/get-pip.py

python3.10 --version
pip3.10 --version
