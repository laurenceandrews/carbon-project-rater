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
        logging.debug(f"CSV Headers: {headers}")
        for row in reader:
            try:
                industry_types[row['Subpart Letter']] = row['Name of industry']
                logging.debug(f"Loaded industry type: {row['Subpart Letter']} -> {row['Name of industry']}")
            except KeyError as e:
                logging.error(f"KeyError: {e} - Row: {row}")
    logging.debug("Industry types loaded successfully.")
    logging.debug(f"All loaded industry types: {industry_types}")

def load_data():
    from app import db, CarbonProject
    filepath = '/app/data/CO2 Sequestered 2016-2022.csv'
    with open(filepath, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Check if the project already exists
            existing_project = CarbonProject.query.filter_by(facility_name=row['Facility Name']).first()
            if existing_project:
                continue  # Skip adding if the project already exists

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

def register_commands(app):
    @app.cli.command("load-data")
    def load_data_command():
        load_data()

    @app.cli.command("load-industry-types")
    def load_industry_types_command():
        load_industry_types()
