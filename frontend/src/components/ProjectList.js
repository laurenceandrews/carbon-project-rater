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
      <p>This application provides a rating for various carbon sequestration projects based on their total mass of CO2 sequestered and duration. Note that this is an exercise and not based on scientific research.</p>
      <Row>
        {projects.sort((a, b) => b.rating - a.rating).map(project => (
          <Col sm="12" md="6" lg="4" key={project.id}>
            <Card className="project-card">
              <CardBody>
                <CardTitle tag="h5">{project.facility_name}</CardTitle>
                <CardText><b>Location:</b> {project.city}, {project.state} ({project.zip_code})</CardText>
                <CardText><b>Address:</b> {project.address}</CardText>
                <CardText><b>County:</b> {project.county}</CardText>
                <CardText><b>Industry Type:</b> {project.industry_type}</CardText>
                <CardText><b>Latitude:</b> {project.latitude}, <b>Longitude:</b> {project.longitude}</CardText>
                <CardText><b>Total CO2 Sequestered:</b> {project.total_mass_co2_sequestered.toLocaleString()} tons</CardText>
                <CardText><b>Duration:</b> {project.duration_years}</CardText>
                <CardText><b>Rating:</b> {project.rating}</CardText>
              </CardBody>
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  );
};

export default ProjectList;
