#!/usr/bin/env bash
. venv/bin/activate
export FLASK_APP=main
if [ "$1" == "dev" ]; then
  export FLASK_ENV=development
  export FLASK_DEBUG=1
  flask run
elif [ "$1" == "prod" ]; then
  export FLASK_ENV=production
  flask run
else
  echo "Invalid runtime environment provided!"
fi