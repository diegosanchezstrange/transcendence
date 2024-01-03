#!/bin/bash

# Connect to the default database and create the 'pong' database
psql -c "CREATE DATABASE pong;"

# Attempt to create the 'postgres' user. Ignore the error if the user already exists.
psql -c "CREATE USER postgres WITH PASSWORD 'postgres';" 2>/dev/null

# Set the password for the 'postgres' user
psql -c "ALTER USER postgres WITH PASSWORD 'postgres';"

