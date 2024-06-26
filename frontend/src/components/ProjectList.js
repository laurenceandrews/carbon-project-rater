import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardBody, CardTitle, Table, Row, Col } from 'reactstrap';
import ReactStars from "react-rating-stars-component";

const ProjectList = () => {
  const [projects, setProjects] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`http://case-study.laurenceandrews.com/api/projects`)
      .then(response => {
        console.log("Projects data received:", response.data.projects);
        setProjects(response.data.projects);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching projects data!', error);
        setError(error);
        setLoading(false);
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

  if (loading) {
    return <p>Loading projects...</p>;
  }

  if (error) {
    return <p>Error loading projects: {error.message}</p>;
  }

  return (
    <div>
      <Row>
        {projects.length > 0 ? projects.sort((a, b) => b.rating - a.rating).map(project => (
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
        )) : <Col><p>No projects available</p></Col>}
      </Row>
    </div>
  );
};

export default ProjectList;
