#!/usr/bin/env bash
. venv/bin/activate
export FLASK_APP=main
export FLASK_ENV=development
export FLASK_DEBUG=1
if [ "$1" == "revoke" ]; then
  flask revoke-admin $2
elif [ "$1" == "add" ]; then
  flask add-admin $2
else
  echo "Invalid admin command provided!"
fi