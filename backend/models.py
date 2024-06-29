# backend/models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CarbonProject(db.Model):
    __tablename__ = 'carbon_project'
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
    total_mass_co2_sequestered_2016 = db.Column(db.Float, nullable=True)
    total_mass_co2_sequestered_2017 = db.Column(db.Float, nullable=True)
    total_mass_co2_sequestered_2018 = db.Column(db.Float, nullable=True)
    total_mass_co2_sequestered_2019 = db.Column(db.Float, nullable=True)
    total_mass_co2_sequestered_2020 = db.Column(db.Float, nullable=True)
    total_mass_co2_sequestered_2021 = db.Column(db.Float, nullable=True)
    total_mass_co2_sequestered_2022 = db.Column(db.Float, nullable=True)
    duration_years = db.Column(db.Integer, nullable=True)

    def calculate_raw_rating(self, all_projects):
        weights = {'total_co2': 0.3, 'duration': 0.2, 'co2_per_year': 0.5}

        max_co2 = max(p.total_mass_co2_sequestered for p in all_projects)
        min_co2 = min(p.total_mass_co2_sequestered for p in all_projects)
        max_duration = max((p.duration_years for p in all_projects if p.duration_years is not None), default=0)
        min_duration = min((p.duration_years for p in all_projects if p.duration_years is not None), default=0)

        yearly_data = [
            self.total_mass_co2_sequestered_2016, self.total_mass_co2_sequestered_2017, 
            self.total_mass_co2_sequestered_2018, self.total_mass_co2_sequestered_2019, 
            self.total_mass_co2_sequestered_2020, self.total_mass_co2_sequestered_2021, 
            self.total_mass_co2_sequestered_2022
        ]
        yearly_data = [data for data in yearly_data if data is not None]

        if yearly_data:
            co2_per_year = (yearly_data[-1] - yearly_data[0]) / (len(yearly_data) - 1) if len(yearly_data) > 1 else yearly_data[0]
        else:
            co2_per_year = 0

        max_co2_per_year = max(((p.total_mass_co2_sequestered_2022 - p.total_mass_co2_sequestered_2016) / (6 - 1) for p in all_projects if p.total_mass_co2_sequestered_2016 is not None), default=0)
        min_co2_per_year = min(((p.total_mass_co2_sequestered_2022 - p.total_mass_co2_sequestered_2016) / (6 - 1) for p in all_projects if p.total_mass_co2_sequestered_2016 is not None), default=0)

        co2_score = (self.total_mass_co2_sequestered - min_co2) / (max_co2 - min_co2) if max_co2 != min_co2 else 0
        duration_score = (self.duration_years - min_duration) / (max_duration - min_duration) if self.duration_years and max_duration != min_duration else 0
        co2_per_year_score = (co2_per_year - min_co2_per_year) / (max_co2_per_year - min_co2_per_year) if max_co2_per_year != min_co2_per_year else 0

        rating = (weights['total_co2'] * co2_score +
                  weights['duration'] * duration_score +
                  weights['co2_per_year'] * co2_per_year_score) * 5

        return rating

    def __repr__(self):
        return f'<CarbonProject {self.facility_name}>'

class TotalCO2ByIndustry(db.Model):
    __tablename__ = 'total_co2_by_industry'
    industry_type = db.Column(db.String(255), primary_key=True)
    total_co2 = db.Column(db.Numeric)