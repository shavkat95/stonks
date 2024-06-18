#!/bin/sh
pkill -9 -f main.py
nohup python3 main.py > output2.log &

