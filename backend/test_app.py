import unittest
from app import app, db, CarbonProject
from sqlalchemy import text

class BackendTest(unittest.TestCase):
    def setUp(self):
        # Set up test DB and app context
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Teardown DB, handling dependent objects
        with app.app_context():
            # Drop dependent views first
            db.session.execute(text('DROP VIEW IF EXISTS dbt_carbon_project_rater.project_transformation CASCADE;'))
            db.session.commit()

            # Now attempt to drop all tables
            db.drop_all()

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello, I'm a Carbon Project Rater!", response.get_data(as_text=True))

    def test_create_project(self):
        response = self.app.post('/projects', json={
            'name': 'Test Project',
            'description': 'A test project.',
            'rating': 5
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Project created', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
