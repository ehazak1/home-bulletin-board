#!/bin/bash
cd /home/pi/picture_frame
port=$(echo `grep tcp_port config.json` | cut -d" " -f2)
sudo gunicorn -b 0.0.0.0:$port -w 2 picture_frame:app &