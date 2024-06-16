import React, { useEffect, useState } from 'react';

function Co2ByIndustry() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5001/co2_by_industry')
      .then(response => response.json())
      .then(data => {
        console.log('Fetched data:', data); // Add logging to check the fetched data
        setData(data.co2_by_industry);
      })
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  return (
    <div>
      <h2>Total CO2 Sequestered by Industry</h2>
      <table>
        <thead>
          <tr>
            <th>Industry Type</th>
            <th>Total CO2 Sequestered (tons)</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              <td>{item.industry_type}</td>
              <td>{item.total_co2}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Co2ByIndustry;
