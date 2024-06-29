import React, { useEffect, useState } from 'react';
import { Table } from 'reactstrap';

function Co2ByIndustry() {
  const [data, setData] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`http://case-study.laurenceandrews.com/api/co2_by_industry`)
      .then(response => response.json())
      .then(data => {
        console.log('Fetched CO2 data:', data);
        setData(data.co2_by_industry);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching CO2 by industry data:', error);
        setError(error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <p>Loading CO2 data...</p>;
  }

  if (error) {
    return <p>Error loading CO2 data: {error.message}</p>;
  }

  return (
    <div className="table-container">
      <h2>Total CO2 Sequestered by Industry</h2>
      <Table striped bordered>
        <thead>
          <tr>
            <th>Industry Type</th>
            <th>Total CO2 Sequestered (tons)</th>
          </tr>
        </thead>
        <tbody>
          {data.length > 0 ? data.map((item, index) => (
            <tr key={index}>
              <td>{item.industry_type}</td>
              <td>{item.total_co2.toLocaleString()}</td>
            </tr>
          )) : <tr><td colSpan="2">No data available</td></tr>}
        </tbody>
      </Table>
    </div>
  );
}

export default Co2ByIndustry;
