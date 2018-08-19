#!/usr/bin/env bash
cd /home/pi/picture_frame
arr=$(echo `grep tcp_port config.json` | tr ":" "\n")
sudo gunicorn -b 0.0.0.0:${arr[1]} -w 2 picture_frame:app &