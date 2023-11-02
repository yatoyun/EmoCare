import React, { useState, useEffect } from 'react';
import { Container, ButtonGroup, Button } from 'react-bootstrap';
import Header from './Header';

import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import api from '../api/api';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'top',
        },
        title: {
            display: true,
            text: 'Emotion Statistics',
        },
    },
    scales: {
        x: {
            title: {
                display: true,
                text: 'Date'
            }
        },
        y: {
            title: {
                display: true,
                text: 'Score'
            }
        }
    }
};

export default function Statistics() {
    const [stats, setStats] = useState(null);
    const [displayType, setDisplayType] = useState('week');

    useEffect(() => {
        const fetchStats = async () => {
            const response = await api.get('statistics/');
            setStats(response.data);
            console.log(response.data);
        };

        fetchStats();
    }, []);

    const getGraphData = (dataKey) => {
        if (!stats || !stats[dataKey]) return { labels: [], datasets: [] };

        const labels = stats[dataKey].map((item) => item.date);
        const avgScores = stats[dataKey].map((item) => item.avg_score);
        const maxScores = stats[dataKey].map((item) => item.max_score);
        const minScores = stats[dataKey].map((item) => item.min_score);

        return {
            labels,
            datasets: [
                {
                    label: 'Average Score',
                    data: avgScores,
                    borderColor: 'rgb(255, 99, 132)',
                    backgroundColor: 'rgba(255, 99, 132, 0.5)',
                },
                {
                    label: 'Max Score',
                    data: maxScores,
                    borderColor: 'rgb(53, 162, 235)',
                    backgroundColor: 'rgba(53, 162, 235, 0.5)',
                },
                {
                    label: 'Min Score',
                    data: minScores,
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.5)',
                },
            ],
        };
    };

    return (
        <div>
            <Header />
            <Container style={{ marginTop: '20px', height: '60vh' }}>
                <ButtonGroup aria-label="Time range">
                    <Button variant="outline-primary" onClick={() => setDisplayType('week')}>Week</Button>
                    <Button variant="outline-primary" onClick={() => setDisplayType('month')}>Month</Button>
                </ButtonGroup>
                <div style={{ height: '50vh' }}>
                    <Line options={options} data={getGraphData(displayType === 'week' ? 'daily_stats' : 'monthly_stats')} />
                </div>
                </Container>
        </div>
    );
}
