// Importing all the necessary components for Topic Distribution Chart.
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Chatbot.css';

// Total Queries component.
const TotalQueries = () => {
  const [totalQueries, setTotalQueries] = useState(0);
  const apiUrl = process.env.REACT_APP_API_URL;

  useEffect(() => {
    const fetchTotalQueries = async () => {
      try {
        const response = await axios.get(`${apiUrl}/total-queries`);
        setTotalQueries(response.data.total);
      } catch (error) {
        console.error('Error fetching total queries:', error);
      }
    };

    fetchTotalQueries();
  }, [apiUrl]);

  return (
    <div>
      <h3 style={{ color: 'white' }}>Total User Queries: {totalQueries}</h3>
    </div>
  );
};

export default TotalQueries;

