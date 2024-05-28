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
            <h2>{project.name}</h2>
            <p>{project.description}</p>
            <p>Rating: {project.rating}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ProjectList;