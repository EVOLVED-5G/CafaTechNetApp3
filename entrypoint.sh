#!/bin/bash
cd netapp
chmod +x start_flask.sh
chmod +x prepare.sh
./start_flask.sh &
./prepare.sh
