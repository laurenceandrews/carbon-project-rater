import React, { useState, useEffect } from 'react';
import axios from 'axios';

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
      <h1>Carbon Projects</h1>
      <ul>
        {projects.map(project => (
          <li key={project.id}>
            <h2>{project.facility_name}</h2>
            <p>Location: {project.city}, {project.state} ({project.zip_code})</p>
            <p>Address: {project.address}</p>
            <p>County: {project.county}</p>
            <p>Industry Type: {project.industry_type}</p>
            <p>Latitude: {project.latitude}, Longitude: {project.longitude}</p>
            <p>Total Mass of CO2 Sequestered (most recent year): {project.total_mass_co2_sequestered.toFixed(2)} tons</p>
            <p>Rating: {project.rating}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ProjectList;