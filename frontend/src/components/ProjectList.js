import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardBody, CardTitle, CardText, Row, Col } from 'reactstrap';

const ProjectList = () => {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5001/projects')
      .then(response => {
        console.log("Data received:", response.data.projects);
        setProjects(response.data.projects);
      })
      .catch(error => {
        console.error('There was an error fetching the projects!', error);
      });
  }, []);

  return (
    <div>
      <h2>Carbon Projects</h2>
      <Row>
        {projects.map(project => (
          <Col sm="12" md="6" lg="4" key={project.id}>
            <Card className="project-card">
              <CardBody>
                <CardTitle tag="h5">{project.facility_name}</CardTitle>
                <CardText>Location: {project.city}, {project.state} ({project.zip_code})</CardText>
                <CardText>Address: {project.address}</CardText>
                <CardText>County: {project.county}</CardText>
                <CardText>Industry Type: {project.industry_type}</CardText>
                <CardText>Latitude: {project.latitude}, Longitude: {project.longitude}</CardText>
                <CardText>Total Mass of CO2 Sequestered (most recent year): {project.total_mass_co2_sequestered.toFixed(2)} tons</CardText>
                <CardText>Rating: {project.rating}</CardText>
              </CardBody>
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  );
};

export default ProjectList;
