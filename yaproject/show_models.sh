#!/bin/bash

python manage.py show_models --tee-stderr 2> $(date '+%Y-%m-%d').dat
