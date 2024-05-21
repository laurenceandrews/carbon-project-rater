from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/carbon_project_rater'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class CarbonProject(db.Model):
    """Model for carbon projects."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    rating = db.Column(db.Integer)

    def __repr__(self):
        return f'<CarbonProject {self.name}>'

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
