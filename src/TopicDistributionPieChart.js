// Importing all the necessary components for Topic Distribution Chart.
import React, { useState, useEffect } from 'react';
import { Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  ArcElement,
  Tooltip,
  Legend,
} from 'chart.js';
import axios from 'axios';

// Declaring the necessary components for Chart.js
ChartJS.register(
    CategoryScale,
    LinearScale,
    ArcElement,
    Tooltip,
    Legend
);

// Topic Pie Chart
const TopicDistributionPieChart = () => {
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [{
      data: [],
      backgroundColor: [],
      hoverBackgroundColor: []
    }]
  });
  const apiUrl = process.env.REACT_APP_API_URL;

  

  useEffect(() => {
    const fetchTopicData = async () => {
      try {
        // Adjusted the endpoint to match the Flask route
        const response = await axios.get(`${apiUrl}/topic-distribution`);
        const data = response.data;
        const topics = Object.keys(data);
        const counts = Object.values(data);

        // Map through the topics to create colors for the chart
        const backgroundColors = topics.map(() => `rgba(${Math.random()*255}, ${Math.random()*255}, ${Math.random()*255}, 0.6)`);
        const hoverBackgroundColors = topics.map(() => `rgba(${Math.random()*255}, ${Math.random()*255}, ${Math.random()*255}, 0.8)`);

        setChartData({
          labels: topics,
          datasets: [{
            data: counts,
            backgroundColor: backgroundColors,
            hoverBackgroundColor: hoverBackgroundColors
          }]
        });
      } catch (error) {
        console.error('Error fetching topic distribution data:', error);
      }
    };

    fetchTopicData();
  }, [apiUrl]);

  const chartOptions = {
    plugins: {
      legend: {
        labels: {
          color: '#000000', 
          font: {
            size: 14 
          }
        }
      }
    }
  };

  return <Pie data={chartData} options={chartOptions} />;
};

export default TopicDistributionPieChart;
