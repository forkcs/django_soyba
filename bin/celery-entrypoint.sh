#!/bin/bash

set -e

# start celery worker
celery -A config worker -l info --concurrency=10
