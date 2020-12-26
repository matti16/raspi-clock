#!/bin/bash
sudo -u pi pulseaudio -k
sudo -u pi pulseaudio --start

sudo -u pi bluetoothctl << EOF
connect F4:4E:FD:3A:9F:87
EOF

/home/pi/raspi-clock/venv/bin/python main.py