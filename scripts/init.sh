#!/usr/bin/env bash
. venv/bin/activate
export FLASK_APP=main
export FLASK_ENV=development
export FLASK_DEBUG=1
flask init-db