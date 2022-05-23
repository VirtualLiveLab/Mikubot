#!/bin/sh
nohup python main.py > ./output_log/main.log &
nohup python button.py > ./output_log/button.log &
