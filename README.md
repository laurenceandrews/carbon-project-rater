# Carbon Project Rater

## Overview
The Carbon Project Rater is a full-stack application designed to rate carbon offset projects based on their effectiveness in emissions capture, avoidance, and sequestration. This system utilizes a combination of modern technologies to provide a robust backend, a dynamic frontend, and an efficient API layer.

## Technologies Used
- **Backend**: Python, Flask, SQLAlchemy, PostgreSQL
- **API Layer**: Node.js, Express
- **Frontend**: React
- **Containerization**: Docker, Docker Compose
- **Data Transformation**: DBT (Data Build Tool)
- **Deployment**: AWS Services (RDS, Lambda, Amplify)

## Project Structure
- `backend/`: Contains Flask application setup and SQLAlchemy models.
- `api/`: Node.js and Express setup for API management.
- `frontend/`: React application setup including components and services.
- `dbt_project/`: Contains DBT models for data transformation in PostgreSQL.
- `docker-compose.yml`: Defines the services, networks, and volumes for docker containers.

## Features
- Rate carbon offset projects based on predefined criteria.
- Retrieve, create, update, and delete project ratings.
- Interactive frontend for displaying project ratings.
- Data transformation using DBT for efficient data handling and reporting.

## Setup and Installation

### Requirements
- Docker 19.03.0+
- Docker Compose 1.25.0+

### Getting Started
To get the application running locally with Docker:

1. Clone the repository:
   git clone https://github.com/yourusername/carbon-project-rater.git
   cd carbon-project-rater

2. Build and run the containers:
   docker-compose up --build

This command will start all services specified in `docker-compose.yml`. The frontend will be accessible at http://localhost:3000, the API at http://localhost:5002, and the backend at http://localhost:4000. The database will run on the default PostgreSQL port 5432.

## Testing
How to run the automated tests for this system:

- Backend tests:
  cd backend
  python -m unittest

- API tests:
  cd api
  npm test

- Frontend tests:
  cd frontend
  npm test

## Deployment
This application is designed to be deployed using AWS services. Here's a general guide:

- **AWS RDS**: Deploy the PostgreSQL database on RDS.
- **AWS Lambda and API Gateway**: Use Lambda to run the API layer, with API Gateway handling the routing.
- **AWS Amplify**: Deploy the React frontend using Amplify for continuous integration and delivery from your GitHub repository.

## Contributing
Contributions and pull requests are very welcome! Please fork the repository and use a feature branch.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.