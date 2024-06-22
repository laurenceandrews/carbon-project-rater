import React from 'react';
import './App.css';
import ProjectList from './components/ProjectList';
import Co2ByIndustry from './components/Co2ByIndustry';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to the Carbon Project Rater</h1>
        <p id="intro-paragraph">This application provides a rating for various carbon sequestration projects based on their total mass of CO2 sequestered, the duration of the project to date, and the average CO2 sequestered per year. Please note, this app is an exercise and not based on scientific research.</p>
      </header>
      <main className="container">
        <ProjectList />
        <Co2ByIndustry />
      </main>
    </div>
  );
}

export default App;
