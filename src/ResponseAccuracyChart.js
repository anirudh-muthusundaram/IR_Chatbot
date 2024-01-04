// Importing all the necessary components for Accuracy Chart.
import React, { useState, useEffect } from 'react';
import { Bar } from 'react-chartjs-2';

// Accuracy Chart
const ResponseAccuracyChart = () => {
    const [data, setData] = useState({});
    const apiUrl = process.env.REACT_APP_API_URL;

    useEffect(() => {
        fetch(`${apiUrl}/response-accuracy`)
            .then(response => response.json())
            .then(data => setData(data))
            .catch(error => console.error('Error fetching data:', error));
    }, [apiUrl]);

    const accuracyChartData = {
        labels: Object.keys(data),
        datasets: [
            {
                label: 'Right Responses',
                data: Object.values(data).map(item => item.right),
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
            },
            {
                label: 'Wrong Responses',
                data: Object.values(data).map(item => item.wrong),
                backgroundColor: 'rgba(255, 99, 132, 0.6)',
            },
        ],
    };
    
    const options = {
        scales: {
            x: {
                ticks: {
                    color: 'white'
                }
            },
            y: {
                ticks: {
                    color: 'black'
                }
            }
        },
        plugins: {
            legend: {
                labels: {
                    color: 'black'
                }
            },
            BackgroundStatic: {
                id: 'BackgroundStatic',
                beforeDraw(chart, args, options) {
                    const {ctx, chartArea: {left, top, width, height}} = chart;
                    ctx.save();
                    ctx.fillStyle = 'white';
                    ctx.fillRect(left, top, width, height);
                    ctx.restore();
                }
            }
        }
    };

     return <Bar data={accuracyChartData} options={options} plugins={[options.plugins.BackgroundStatic]} />;
};

export default ResponseAccuracyChart;