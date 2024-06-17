import React from 'react';
import './App.css';
import ProjectList from './components/ProjectList';
import Co2ByIndustry from './components/Co2ByIndustry';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to the Carbon Project Rater</h1>
      </header>
      <main className="container">
        <ProjectList />
        <Co2ByIndustry />
      </main>
    </div>
  );
}

export default App;
