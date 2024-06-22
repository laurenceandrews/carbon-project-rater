import logging
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from load_data import register_commands, load_data, load_industry_types, industry_types
from sqlalchemy import text
import re
from collections import defaultdict

app = Flask(__name__)
CORS(app)
register_commands(app)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:password@db/carbon_project_rater')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class CarbonProject(db.Model):
    """Model for carbon projects."""
    id = db.Column(db.Integer, primary_key=True)
    facility_name = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    zip_code = db.Column(db.String(10))
    address = db.Column(db.String(255))
    county = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    industry_type = db.Column(db.String(255))
    total_mass_co2_sequestered = db.Column(db.Float)
    duration_years = db.Column(db.Float, nullable=True)
    additional_benefits = db.Column(db.String(255), nullable=True)

    def calculate_raw_rating(self, all_projects):
        # Define the weights
        weights = {
            'total_co2': 0.4,
            'duration': 0.4,
            'additional_benefits': 0.2
        }

        # Get the ranges for normalization
        max_co2 = max(p.total_mass_co2_sequestered for p in all_projects)
        min_co2 = min(p.total_mass_co2_sequestered for p in all_projects)
        max_duration = max((p.duration_years for p in all_projects if p.duration_years is not None), default=0)
        min_duration = min((p.duration_years for p in all_projects if p.duration_years is not None), default=0)
        max_benefits = max((int(p.additional_benefits) if p.additional_benefits else 0 for p in all_projects), default=0)
        min_benefits = min((int(p.additional_benefits) if p.additional_benefits else 0 for p in all_projects), default=0)

        # Normalize scores to a 0-1 range
        co2_score = (self.total_mass_co2_sequestered - min_co2) / (max_co2 - min_co2) if max_co2 != min_co2 else 0
        duration_score = (self.duration_years - min_duration) / (max_duration - min_duration) if self.duration_years and max_duration != min_duration else 0
        benefits_score = (int(self.additional_benefits) - min_benefits) / (max_benefits - min_benefits) if self.additional_benefits and max_benefits != min_benefits else 0

        # Calculate the raw rating
        rating = (weights['total_co2'] * co2_score +
                  weights['duration'] * duration_score +
                  weights['additional_benefits'] * benefits_score) * 10  # Scale to 10

        return rating

    def __repr__(self):
        return f'<CarbonProject {self.facility_name}>'

def ensure_industry_types_loaded():
    """Ensure industry types are loaded."""
    if not industry_types:
        load_industry_types()

@app.route('/')
def home():
    """Root endpoint returns a greeting."""
    return "Hello, I'm a Carbon Project Rater!"

@app.route('/projects')
def get_projects():
    """Endpoint to retrieve all projects."""
    projects = CarbonProject.query.all()
    raw_ratings = [p.calculate_raw_rating(projects) for p in projects]

    # Normalize the raw ratings to the 1-10 range
    min_rating = min(raw_ratings)
    max_rating = max(raw_ratings)
    normalized_ratings = [(r - min_rating) / (max_rating - min_rating) * 9 + 1 for r in raw_ratings]

    projects_with_ratings = []
    for p, rating in zip(projects, normalized_ratings):
        project_data = {
            'id': p.id,
            'facility_name': p.facility_name,
            'city': p.city,
            'state': p.state,
            'zip_code': p.zip_code,
            'address': p.address,
            'county': p.county,
            'latitude': p.latitude,
            'longitude': p.longitude,
            'industry_type': p.industry_type,
            'total_mass_co2_sequestered': p.total_mass_co2_sequestered,
            'duration_years': p.duration_years,
            'additional_benefits': p.additional_benefits,
            'rating': round(rating * 2) / 2  # Round to nearest 0.5
        }
        projects_with_ratings.append(project_data)
    return jsonify({'projects': projects_with_ratings})

@app.route('/co2_by_industry')
def get_co2_by_industry():
    """Endpoint to retrieve total CO2 sequestered by industry."""
    ensure_industry_types_loaded()  # Ensure industry types are loaded
    with db.engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM public.total_co2_by_industry"))
        co2_by_industry = defaultdict(float)  # Use a default dictionary to aggregate CO2 by industry
        for row in result:
            industry_types_str = row[0]  # Access the industry_type column
            total_co2 = row[1]  # Access the total_co2 column
            for subpart in industry_types_str.split(','):
                subpart_clean = re.sub(r'\([^)]*\)', '', subpart).strip()  # Remove parentheses and their contents
                subpart_clean = re.sub(r'[^A-Za-z-]', '', subpart_clean)  # Remove non-alphabetic characters except hyphen
                app.logger.debug(f'Processing subpart: "{subpart}" -> Cleaned: "{subpart_clean}"')
                # Use industry_types dictionary to get the industry name
                industry_name = industry_types.get(subpart_clean, subpart_clean)
                if industry_name == subpart_clean:
                    app.logger.warning(f'No mapping found for subpart "{subpart_clean}", using original subpart "{subpart_clean}"')
                else:
                    app.logger.debug(f'Mapped subpart "{subpart_clean}" to industry name "{industry_name}"')
                co2_by_industry[industry_name] += total_co2

    co2_by_industry_list = [{'industry_type': industry, 'total_co2': total_co2} for industry, total_co2 in co2_by_industry.items()]
    app.logger.debug('CO2 by industry data: %s', co2_by_industry_list)
    return jsonify({'co2_by_industry': co2_by_industry_list})

@app.route('/projects', methods=['POST'])
def create_project():
    """Endpoint to create a new project from JSON data."""
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
        total_mass_co2_sequestered=float(data.get('total_mass_co2_sequestered')) if data.get('total_mass_co2_sequestered') else None
    )
    db.session.add(new_project)
    db.session.commit()
    return jsonify({'message': 'Project created', 'project': {'id': new_project.id, 'facility_name': new_project.facility_name}}), 201

@app.route('/projects/<int:id>', methods=['PUT'])
def update_project(id):
    """Endpoint to update an existing project by id."""
    project = CarbonProject.query.get_or_404(id)
    data = request.get_json()
    if 'name' in data:
        project.name = data['name']
    if 'description' in data:
        project.description = data['description']
    if 'rating' in data:
        if not isinstance(data['rating'], int) or data['rating'] < 0 or data['rating'] > 5:
            return jsonify({'error': 'Rating must be an integer between 0 and 5'}), 400
        project.rating = data['rating']
    db.session.commit()
    return jsonify({'message': 'Project updated', 'project': {'name': project.name, 'description': project.description, 'rating': project.rating}})

@app.route('/projects/<int:id>', methods=['DELETE'])
def delete_project(id):
    """Endpoint to delete a project by id."""
    project = CarbonProject.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Project deleted'})

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to ensure the service is running."""
    return jsonify({"status": "healthy"}), 200

@app.errorhandler(404)
def not_found(error):
    """Error handler for 404 Not Found."""
    return jsonify({'error': 'Not found'}), 404

def populate_database():
    print("Checking if database needs to be populated...")
    with app.app_context():
        load_industry_types()  # Ensure industry types are loaded
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
                    total_mass_co2_sequestered=5000.0
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
                    total_mass_co2_sequestered=12000.0
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
                    total_mass_co2_sequestered=8000.0
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
    """Populates the database with initial data."""
    populate_database()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
