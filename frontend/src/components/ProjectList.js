import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardBody, CardTitle, Table, Row, Col } from 'reactstrap';
import ReactStars from "react-rating-stars-component";

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

  const formatIndustryText = (text) => {
    return text.split(',').map((item, index) => (
      <span key={index} className="industry-text">
        {item.trim()}
        {index < text.split(',').length - 1 && ','}<br />
      </span>
    ));
  };

  return (
    <div>
      <Row>
        {projects.sort((a, b) => b.rating - a.rating).map(project => (
          <Col sm="12" md="6" lg="4" key={project.id}>
            <Card className="project-card">
              <CardBody>
                <div className="card-header">
                  <CardTitle tag="h5">{project.facility_name}</CardTitle>
                  <ReactStars
                    count={5}
                    value={project.rating}
                    size={24}
                    isHalf={true}
                    emptyIcon={<i className="far fa-star"></i>}
                    halfIcon={<i className="fa fa-star-half-alt"></i>}
                    fullIcon={<i className="fa fa-star"></i>}
                    activeColor="#ffd700"
                    edit={false}
                  />
                </div>
                <Table borderless className="project-table">
                  <tbody>
                    <tr>
                      <td><b>Location:</b></td>
                      <td>{project.city}, {project.state} ({project.zip_code})</td>
                    </tr>
                    <tr>
                      <td><b>Lat/Long:</b></td>
                      <td>{project.lat_long}</td>
                    </tr>
                    <tr>
                      <td><b>Industry:</b></td>
                      <td>{formatIndustryText(project.industry)}</td>
                    </tr>
                    <tr>
                      <td><b>Total CO2 Sequestered:</b></td>
                      <td>{project.total_mass_co2_sequestered.toLocaleString()} tons</td>
                    </tr>
                    <tr>
                      <td><b>Duration:</b></td>
                      <td>{project.duration_years}</td>
                    </tr>
                  </tbody>
                </Table>
              </CardBody>
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  );
};

export default ProjectList;
