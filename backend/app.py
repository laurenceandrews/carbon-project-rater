import logging
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from load_data import register_commands

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
    return jsonify({'projects': [{'id': p.id, 'name': p.name, 'description': p.description, 'rating': p.rating} for p in projects]})

@app.route('/projects', methods=['POST'])
def create_project():
    """Endpoint to create a new project from JSON data."""
    data = request.get_json()
    if not data or 'name' not in data or 'rating' not in data:
        return jsonify({'error': 'Missing data'}), 400
    if not isinstance(data['rating'], int) or data['rating'] < 0 or data['rating'] > 5:
        return jsonify({'error': 'Rating must be an integer between 0 and 5'}), 400
    new_project = CarbonProject(name=data['name'], description=data['description'], rating=data['rating'])
    db.session.add(new_project)
    db.session.commit()
    return jsonify({'message': 'Project created', 'project': {'name': new_project.name, 'description': new_project.description, 'rating': new_project.rating}}), 201

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
                CarbonProject(name='Green Energy Project', description='A project to create sustainable green energy solutions.', rating=5),
                CarbonProject(name='Reforestation Initiative', description='A project aimed at reforesting depleted forests.', rating=4),
                CarbonProject(name='Ocean Cleanup', description='A project to clean plastics and other waste from the oceans.', rating=5)
            ]
            db.session.bulk_save_objects(projects)
            db.session.commit()
            print("Database populated with initial data.")
        else:
            print("Database already populated.")

@app.cli.command("populate_db")
def populate_database_command():
    """Populates the database with initial data."""
    populate_database()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)