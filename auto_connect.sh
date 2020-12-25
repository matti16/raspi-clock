#!/bin/bash
sudo -u pi pulseaudio --start << EOF
raspberry
EOF

sudo -u pi bluetoothctl << EOF
raspberry
connect F4:4E:FD:3A:9F:87
EOF