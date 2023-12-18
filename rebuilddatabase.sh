#!/bin/bash
echo ---Deleting Old Database---
rm sqlite3.db

echo ---Deleting Current Migrations---
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

echo ---Creating Migrations with Django---
./manage.py makemigrations

echo ---Applying Migrations With Django---
./manage.py migrate
sleep 1

echo ---Running SQL Queries to Populate Inital Rows In The Database---
sqlite3 sqlite3.db < Queries.sql

