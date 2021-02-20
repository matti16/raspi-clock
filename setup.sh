#!/bin/bash
sudo apt update
sudo apt install -y python3-pip git supervisor vlc
git clone https://github.com/matti16/raspi-clock.git
cd raspi-clock
pip3 install -r requirements.txt