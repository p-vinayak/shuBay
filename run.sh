#!/usr/bin/env bash
export FLASK_APP=main
if [ "$1" == "dev" ]; then
  export FLASK_ENV=development
  export FLASK_DEBUG=1
  flask run
else
  export FLASK_ENV=production
  flask run
fi