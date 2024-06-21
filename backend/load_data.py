import logging
import csv

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

industry_types = {}

def load_industry_types():
    global industry_types
    filepath = '/app/data/Industry Types.csv'
    with open(filepath, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames
        logging.debug(f"CSV Headers: {headers}")  # Add logging to check headers
        for row in reader:
            try:
                industry_types[row['Subpart Letter']] = row['Name of industry']
                logging.debug(f"Loaded industry type: {row['Subpart Letter']} -> {row['Name of industry']}")
            except KeyError as e:
                logging.error(f"KeyError: {e} - Row: {row}")  # Log the row that caused the error
    logging.debug("Industry types loaded successfully.")
    logging.debug(f"All loaded industry types: {industry_types}")

def load_data():
    from app import db, CarbonProject
    filepath = '/app/data/CO2 Sequestered 2016-2022.csv'
    with open(filepath, newline='', encoding='utf-8-sig') as csvfile:
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
                total_mass_co2_sequestered=float(row['2022 Total Mass CO2 Sequestered']),
                duration_years=float(row['Duration']) if 'Duration' in row else None,
                additional_benefits=row['Additional Benefits'] if 'Additional Benefits' in row else None
            )
            db.session.add(project)
        db.session.commit()
    logging.debug("Data loaded successfully.")

def register_commands(app):
    @app.cli.command("load-data")
    def load_data_command():
        """Command to load data into the database."""
        load_data()

    @app.cli.command("load-industry-types")
    def load_industry_types_command():
        """Command to load industry types into the dictionary."""
        load_industry_types()
