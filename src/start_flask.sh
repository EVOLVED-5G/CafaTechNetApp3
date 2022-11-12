#!/bin/bash
export FLASK_APP=api.py
export FLASK_DEBUG=1
python3 -m flask run --host=0.0.0.0 --port=5555
