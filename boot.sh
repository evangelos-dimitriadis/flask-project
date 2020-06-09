#!/bin/bash

exec gunicorn --bind :5000 --workers=4 --timeout 240 \
--reload --capture-output --log-level=DEBUG wsgi:app 
