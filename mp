#! /bin/sh

source venv6/bin/activate
mavproxy.py --master=/dev/ttyS0 --out=udp:127.0.0.1:14550
