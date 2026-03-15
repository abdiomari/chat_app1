#!/bin/bash
set -e

pip install -r requirements.txt

npm install -D tailwindcss
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --minify

python manage.py collectstatic --noinput

