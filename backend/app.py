# backend/app.py

import logging
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, CarbonProject
from load_data import register_commands
from utils import load_industry_types, industry_types
import re
from collections import defaultdict

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:password@carbon-project-rater-db.cb6smiis4efz.eu-north-1.rds.amazonaws.com/carbon_project_rater')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

register_commands(app)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def ensure_industry_types_loaded():
    if not industry_types:
        load_industry_types()

def clean_industry_type(industry_type_str):
    parts = industry_type_str.split(',')
    full_names = []
    for part in parts:
        clean_part = re.sub(r'\([^)]*\)', '', part).strip()
        if clean_part == 'RR':
            full_names.extend(['Geologic Sequestration of Carbon Dioxide', 'CO2 Injection'])
        else:
            full_name = industry_types.get(clean_part, clean_part)
            full_names.append(full_name)
    return full_names

def truncate_with_ellipsis(text, max_length):
    return text if len(text) <= max_length else text[:max_length] + '...'

def format_industry_type(industry_type_str):
    cleaned_names = clean_industry_type(industry_type_str)
    truncated_names = [truncate_with_ellipsis(name, 30) for name in cleaned_names]
    return ',\n'.join(truncated_names)

@app.route('/projects')
def get_projects():
    projects = CarbonProject.query.all()
    if not projects:
        app.logger.debug('No projects found in the database.')

    raw_ratings = [p.calculate_raw_rating(projects) for p in projects]
    if not raw_ratings:
        app.logger.debug('No raw ratings calculated.')

    min_rating = min(raw_ratings, default=0)
    max_rating = max(raw_ratings, default=0)
    normalized_ratings = [(r - min_rating) / (max_rating - min_rating) * 9 + 1 for r in raw_ratings]

    projects_with_ratings = []
    for p, rating in zip(projects, normalized_ratings):
        project_data = {
            'id': p.id,
            'facility_name': p.facility_name or 'N/A',
            'city': p.city or 'N/A',
            'state': p.state or 'N/A',
            'zip_code': p.zip_code or 'N/A',
            'address': p.address or 'N/A',
            'county': p.county or 'N/A',
            'lat_long': f"{p.latitude}, {p.longitude}" if p.latitude and p.longitude else 'N/A',
            'industry': format_industry_type(p.industry_type) if p.industry_type else 'N/A',
            'total_mass_co2_sequestered': round(p.total_mass_co2_sequestered),
            'duration_years': '5+ years' if p.duration_years == 5 else (f"{int(p.duration_years)} years" if p.duration_years else 'N/A'),
            'rating': round(rating * 2) / 2
        }
        projects_with_ratings.append(project_data)

    if not projects_with_ratings:
        app.logger.debug('No projects with ratings found.')

    projects_with_ratings.sort(key=lambda x: x['rating'], reverse=True)
    app.logger.debug(f'Projects with ratings: {projects_with_ratings}')
    return jsonify({'projects': projects_with_ratings})

@app.route('/co2_by_industry')
def get_co2_by_industry():
    ensure_industry_types_loaded()
    co2_by_industry = defaultdict(float)
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM public.total_co2_by_industry"))
            for row in result:
                industry_types_str = row[0]
                total_co2 = row[1]
                for subpart in industry_types_str.split(','):
                    subpart_clean = re.sub(r'\([^)]*\)', '', subpart).strip()
                    subpart_clean = re.sub(r'[^A-Za-z-]', '', subpart_clean)
                    app.logger.debug(f'Processing subpart: "{subpart}" -> Cleaned: "{subpart_clean}"')
                    industry_name = industry_types.get(subpart_clean, subpart_clean)
                    if industry_name == subpart_clean:
                        app.logger.warning(f'No mapping found for subpart "{subpart_clean}", using original subpart "{subpart_clean}"')
                    else:
                        app.logger.debug(f'Mapped subpart "{subpart_clean}" to industry name "{industry_name}"')
                    co2_by_industry[industry_name] += total_co2
    except Exception as e:
        app.logger.error(f'Error fetching CO2 by industry data: {e}')
        return jsonify({'error': 'Error fetching CO2 by industry'}), 500

    co2_by_industry_list = [{'industry_type': industry, 'total_co2': round(total_co2)} for industry, total_co2 in co2_by_industry.items()]
    co2_by_industry_list.sort(key=lambda x: x['total_co2'], reverse=True)
    app.logger.debug('CO2 by industry data: %s', co2_by_industry_list)
    return jsonify({'co2_by_industry': co2_by_industry_list})

@app.route('/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    if not data or 'facility_name' not in data:
        return jsonify({'error': 'Missing data'}), 400
    new_project = CarbonProject(
        facility_name=data['facility_name'],
        city=data.get('city'),
        state=data.get('state'),
        zip_code=data.get('zip_code'),
        address=data.get('address'),
        county=data.get('county'),
        latitude=float(data.get('latitude')) if data.get('latitude') else None,
        longitude=float(data.get('longitude')) if data.get('longitude') else None,
        industry_type=data.get('industry_type'),
        total_mass_co2_sequestered=float(data.get('total_mass_co2_sequestered')) if data.get('total_mass_co2_sequestered') else None,
        duration_years=None
    )
    db.session.add(new_project)
    db.session.commit()
    return jsonify({'message': 'Project created', 'project': {'id': new_project.id, 'facility_name': new_project.facility_name}}), 201

@app.route('/projects/<int:id>', methods=['PUT'])
def update_project(id):
    project = CarbonProject.query.get_or_404(id)
    data = request.get_json()
    if 'facility_name' in data:
        project.facility_name = data['facility_name']
    if 'city' in data:
        project.city = data['city']
    if 'state' in data:
        project.state = data['state']
    if 'zip_code' in data:
        project.zip_code = data['zip_code']
    if 'address' in data:
        project.address = data['address']
    if 'county' in data:
        project.county = data['county']
    if 'latitude' in data:
        project.latitude = data['latitude']
    if 'longitude' in data:
        project.longitude = data['longitude']
    if 'industry_type' in data:
        project.industry_type = data['industry_type']
    if 'total_mass_co2_sequestered' in data:
        project.total_mass_co2_sequestered = data['total_mass_co2_sequestered']
    db.session.commit()
    return jsonify({'message': 'Project updated', 'project': {'facility_name': project.facility_name}})

@app.route('/projects/<int:id>', methods=['DELETE'])
def delete_project(id):
    project = CarbonProject.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Project deleted'})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

def populate_database():
    print("Checking if database needs to be populated...")
    with app.app_context():
        load_industry_types()
        if not CarbonProject.query.first():
            print("No projects found, populating database...")
            projects = [
                CarbonProject(
                    facility_name='Green Energy Project',
                    city='City A',
                    state='State A',
                    zip_code='12345',
                    address='123 Green St',
                    county='County A',
                    latitude=40.7128,
                    longitude=-74.0060,
                    industry_type='Renewable Energy',
                    total_mass_co2_sequestered=5000.0,
                    duration_years=1
                ),
                CarbonProject(
                    facility_name='Reforestation Initiative',
                    city='City B',
                    state='State B',
                    zip_code='54321',
                    address='456 Forest Ave',
                    county='County B',
                    latitude=34.0522,
                    longitude=-118.2437,
                    industry_type='Reforestation',
                    total_mass_co2_sequestered=12000.0,
                    duration_years=2
                ),
                CarbonProject(
                    facility_name='Ocean Cleanup',
                    city='City C',
                    state='State C',
                    zip_code='67890',
                    address='789 Ocean Blvd',
                    county='County C',
                    latitude=37.7749,
                    longitude=-122.4194,
                    industry_type='Oceanic Preservation',
                    total_mass_co2_sequestered=8000.0,
                    duration_years=3
                )
            ]
            db.session.bulk_save_objects(projects)
            db.session.commit()
            print("Database populated with initial data.")
        else:
            print("Database already populated.")
    load_data()

@app.cli.command("populate_db")
def populate_database_command():
    populate_database()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)