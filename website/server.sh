#!/bin/bash

export PROD_MODE="True"

./env/bin/gunicorn --workers 1 --log-file=gunicorn.log --bind unix:starthack2019.sock website.wsgi:application
