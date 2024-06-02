import logging
import csv
from flask import current_app

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data():
    from app import db, CarbonProject
    filepath = '/app/data/CO2 Sequestered 2016-2022.csv'
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            project = CarbonProject(
                facility_name=row['Facility Name'],
                city=row['City'],
                state=row['State'],
                zip_code=row['Zip Code'],
                address=row['Address'],
                county=row['County'],
                latitude=float(row['Latitude']),
                longitude=float(row['Longitude']),
                industry_type=row['Industry Type (subparts)'],
                total_mass_co2_sequestered=float(row['2022 Total Mass CO2 Sequestered'])
            )
            db.session.add(project)
        db.session.commit()
    print("Data loaded successfully.")

def register_commands(app):
    @app.cli.command("load-data")
    def load_data_command():
        """Command to load data into the database."""
        load_data()