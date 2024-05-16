from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/carbon_project_rater'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class CarbonProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    rating = db.Column(db.Integer)

    def __repr__(self):
        return f'<CarbonProject {self.name}>'

@app.route('/')
def home():
    return "Hello, I'm a Carbon Project Rater!"

@app.route('/projects')
def get_projects():
    projects = CarbonProject.query.all()
    return { 'projects': [{ 'name': p.name, 'description': p.description, 'rating': p.rating } for p in projects] }

if __name__ == '__main__':
    app.run(debug=True)
