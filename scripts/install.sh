#!/usr/bin/env bash
python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt
cp ./config_example.json ./config.json
echo "Please edit the created config.json file!"