# Carbon Project Rater

## Overview
The Carbon Project Rater is a full-stack application designed to rate carbon offset projects based on their effectiveness in emissions capture, avoidance, and sequestration. This system utilizes a combination of modern technologies to provide a robust backend, a dynamic frontend, and an efficient API layer.

## Technologies Used
- **Backend**: Python, Flask, SQLAlchemy, PostgreSQL
- **API Layer**: Node.js, Express
- **Frontend**: React
- **Data Transformation**: DBT (Data Build Tool)
- **Deployment**: AWS Services (RDS, Lambda, Amplify)

## Project Structure
- `backend/`: Contains Flask application setup and SQLAlchemy models.
- `api/`: Node.js and Express setup for API management.
- `frontend/`: React application setup including components and services.
- `dbt_project/`: Contains DBT models for data transformation in PostgreSQL.

## Features
- Rate carbon offset projects based on predefined criteria.
- Retrieve, create, update, and delete project ratings.
- Interactive frontend for displaying project ratings.
- Data transformation using DBT for efficient data handling and reporting.

## Setup and Installation

### Requirements
- Python 3.8+
- Node.js 14+
- PostgreSQL 13+
- DBT 1.8+

### Backend Setup
1. Navigate to the `backend/` directory.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask application:
   ```bash
   python app.py
   ```

### API Layer Setup
1. Navigate to the `api/` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Express server:
   ```bash
   node server.js
   ```

### Frontend Setup
1. Navigate to the `frontend/` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the React development server:
   ```bash
   npm start
   ```

### DBT Setup
1. Navigate to the `dbt_project/` directory.
2. Run DBT to perform data transformations:
   ```bash
   dbt run
   ```

## Testing
How to run the automated tests for this system:
- Backend tests:
  ```bash
  cd backend
  python -m unittest
  ```
- API tests:
  ```bash
  cd api
  npm test
  ```
- Frontend tests:
  ```bash
  cd frontend
  npm test
  ```

## Deployment
This application is designed to be deployed using AWS services. Here's a general guide:
- **AWS RDS**: Deploy the PostgreSQL database on RDS.
- **AWS Lambda and API Gateway**: Use Lambda to run the API layer, with API Gateway handling the routing.
- **AWS Amplify**: Deploy the React frontend using Amplify for continuous integration and delivery from your GitHub repository.

## Contributing
Contributions and pull requests are very welcome! Please fork the repository and use a feature branch.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.
