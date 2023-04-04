#!/bin/bash

set -e

cd /app/

pip3 install --no-warn-script-location --no-cache-dir -r requirements/dev.txt

# If requirements.txt is newer than the lock file or the lock file doesn't exist.
if [ requirements/base.txt -nt requirements/lock.txt ]|| [ requirements/dev.txt -nt requirements/lock.txt ]; then
  pip3 freeze > requirements/lock.txt
fi

pip3 install --no-warn-script-location --no-cache-dir \
  -r requirements/dev.txt -c requirements/lock.txt
