#!/bin/bash

sudo python3 manage.py makemigrations crm
sudo python3 manage.py migrate
sudo python3 manage.py runserver 0.0.0.0:80 &