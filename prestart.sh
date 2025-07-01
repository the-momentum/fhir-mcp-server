#!/bin/bash

set -e

if [ -f ./config/.env ]; then
  export DEBUG=$(grep '^DEBUG=' ./config/.env | cut -d '=' -f2-)
fi

bash ./scripts/start/app.sh

# exec "$@"
