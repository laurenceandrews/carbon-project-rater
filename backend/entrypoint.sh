#!/bin/sh

# Set PostgreSQL environment variables
export PGUSER=postgres
export PGPASSWORD=password

# Wait for the PostgreSQL database to be ready
dockerize -wait tcp://carbon-project-rater-db.cb6smiis4efz.eu-north-1.rds.amazonaws.com:5432 -timeout 60s

# Check if the database exists, and create it if it doesn't
echo "Checking if database exists..."
DB_EXIST=$(psql -h carbon-project-rater-db.cb6smiis4efz.eu-north-1.rds.amazonaws.com -lqt | cut -d \| -f 1 | grep -w carbon_project_rater | wc -l)

if [ $DB_EXIST -eq 0 ]; then
    echo "Database does not exist. Creating database..."
    createdb -h carbon-project-rater-db.cb6smiis4efz.eu-north-1.rds.amazonaws.com carbon_project_rater
else
    echo "Database already exists."
fi

# Run migrations and populate the database
flask db upgrade

# Load industry types and data
flask load-industry-types
flask load-data

# Create the total_co2_by_industry table if it doesn't exist and load data
flask create-total-co2-table

# Start the backend application
flask run --host=0.0.0.0 --port=5002
