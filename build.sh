#!/usr/bin/env bash
# Exit immediately if any command fails
set -o errexit

# Install all dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate