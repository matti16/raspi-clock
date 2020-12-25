#!/bin/bash
pulseaudio --start << EOF
raspberry
EOF

bluetoothctl << EOF
raspberry
connect F4:4E:FD:3A:9F:87
EOF