import logging
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from load_data import register_commands, load_data
from sqlalchemy import text

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

    def __repr__(self):
        return f'<CarbonProject {self.facility_name}>'

@app.route('/')
def home():
    """Root endpoint returns a greeting."""
    return "Hello, I'm a Carbon Project Rater!"

@app.route('/projects')
def get_projects():
    """Endpoint to retrieve all projects."""
    projects = CarbonProject.query.all()
    return jsonify({'projects': [
        {
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
            'rating': None  # Assuming this will be calculated or set later
        } for p in projects
    ]})

@app.route('/co2_by_industry')
def get_co2_by_industry():
    """Endpoint to retrieve total CO2 sequestered by industry."""
    with db.engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM public.total_co2_by_industry"))
        co2_by_industry = [{'industry_type': row[0], 'total_co2': row[1]} for row in result]
    app.logger.debug('CO2 by industry data: %s', co2_by_industry)
    return jsonify({'co2_by_industry': co2_by_industry})

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
    # Ensure the load_data function is called here
    load_data()

@app.cli.command("populate_db")
def populate_database_command():
    """Populates the database with initial data."""
    populate_database()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)