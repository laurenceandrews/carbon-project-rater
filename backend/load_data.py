# backend/load_data.py

import logging
import os
import csv
from sqlalchemy import text, inspect
from models import db, CarbonProject, TotalCO2ByIndustry
from utils import load_industry_types, industry_types

def load_data():
    filepath = os.path.join(os.path.dirname(__file__), 'data', 'CO2 Sequestered 2016-2022.csv')
    with open(filepath, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            existing_project = CarbonProject.query.filter_by(facility_name=row['Facility Name']).first()
            if existing_project:
                continue
            duration_years = sum(1 for year in ['2016 Total Mass CO2 Sequestered', '2017 Total Mass CO2 Sequestered', 
                                                '2018 Total Mass CO2 Sequestered', '2019 Total Mass CO2 Sequestered',
                                                '2020 Total Mass CO2 Sequestered', '2021 Total Mass CO2 Sequestered',
                                                '2022 Total Mass CO2 Sequestered'] if row[year])
            duration_years = min(duration_years, 5)
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
                total_mass_co2_sequestered=float(row['2022 Total Mass CO2 Sequestered']),
                total_mass_co2_sequestered_2016=float(row['2016 Total Mass CO2 Sequestered']) if row['2016 Total Mass CO2 Sequestered'] else None,
                total_mass_co2_sequestered_2017=float(row['2017 Total Mass CO2 Sequestered']) if row['2017 Total Mass CO2 Sequestered'] else None,
                total_mass_co2_sequestered_2018=float(row['2018 Total Mass CO2 Sequestered']) if row['2018 Total Mass CO2 Sequestered'] else None,
                total_mass_co2_sequestered_2019=float(row['2019 Total Mass CO2 Sequestered']) if row['2019 Total Mass CO2 Sequestered'] else None,
                total_mass_co2_sequestered_2020=float(row['2020 Total Mass CO2 Sequestered']) if row['2020 Total Mass CO2 Sequestered'] else None,
                total_mass_co2_sequestered_2021=float(row['2021 Total Mass CO2 Sequestered']) if row['2021 Total Mass CO2 Sequestered'] else None,
                total_mass_co2_sequestered_2022=float(row['2022 Total Mass CO2 Sequestered']) if row['2022 Total Mass CO2 Sequestered'] else None,
                duration_years=duration_years
            )
            db.session.add(project)
        db.session.commit()
    logging.debug("Data loaded successfully.")

def create_total_co2_table():
    inspector = inspect(db.engine)
    if not inspector.has_table('total_co2_by_industry'):
        logging.info('Creating total_co2_by_industry table...')
        db.create_all()
        initial_data = [
            {'industry_type': 'Geologic Sequestration of CO2', 'total_co2': 100000},
            {'industry_type': 'CO2 Injection', 'total_co2': 50000},
        ]
        for data in initial_data:
            co2_entry = TotalCO2ByIndustry(**data)
            db.session.add(co2_entry)
        db.session.commit()
        logging.info('total_co2_by_industry table created and populated.')
    else:
        logging.info('total_co2_by_industry table already exists.')

def register_commands(app):
    @app.cli.command("load-data")
    def load_data_command():
        load_data()

    @app.cli.command("load-industry-types")
    def load_industry_types_command():
        load_industry_types()

    @app.cli.command("create-total-co2-table")
    def create_total_co2_table_command():
        create_total_co2_table()