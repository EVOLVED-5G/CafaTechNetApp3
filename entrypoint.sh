#!/bin/bash
cd src
chmod +x start_flask.sh
./start_flask.sh &
python3 qos_awereness.py
