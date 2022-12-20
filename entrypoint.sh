#!/bin/bash
cd netapp
python3 netapp_capif_connector.py
chmod +x start_flask.sh
./start_flask.sh
