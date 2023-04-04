#!/bin/bash

set -e

# start celery worker
python -m celery -A config worker -l info --concurrency=10
