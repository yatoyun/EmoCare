import React, { useState, useEffect } from 'react';
import { Container, Tabs, Tab, Nav, Card } from 'react-bootstrap';
import Header from './Header';
import { Chart as ChartJS, registerables } from 'chart.js';
import { Bar, Scatter } from 'react-chartjs-2';
import 'chartjs-adapter-date-fns';
import './Statistics.css';
import api from '../api/api';
import { refreshToken } from '../api/auth'; 
import { useNavigate } from 'react-router-dom';

ChartJS.register(...registerables);

const StatisticsPage = () => {
    // States for data and UI control
    const [dailyEmotionData, setDailyEmotionData] = useState({});
    const [weeklyEmotionData, setWeeklyEmotionData] = useState({});
    const [dailyChatData, setDailyChatData] = useState({});
    const [weeklyChatData, setWeeklyChatData] = useState({});
    const [scatterData, setScatterData] = useState({});
    const [skewness, setSkewness] = useState(0);
    const [kurtosis, setKurtosis] = useState(0);
    const [dailySentimentClassificationData, setDailySentimentClassificationData] = useState({});
    const [weeklySentimentClassificationData, setWeeklySentimentClassificationData] = useState({});
    const [activeMainTab, setActiveMainTab] = useState("emotion_chat");
    const [activeTimeFrame, setActiveTimeFrame] = useState('daily');
    const history = useNavigate();

    useEffect(() => {
        const fetchStats = async () => {
            
            try{
                const response = await api.get('/statistics/')
                if (response.status === 200) {
                    const stats = response.data;

                    setDailyEmotionData(stats.daily_emotion_stats);
                    setWeeklyEmotionData(stats.weekly_emotion_stats);
                    setDailyChatData(stats.daily_chat_stats);
                    setWeeklyChatData(stats.weekly_chat_stats);
                    setScatterData({
                        datasets: [{
                            label: 'Scatter Data',
                            data: stats.scatter_data,
                            backgroundColor: 'rgba(255, 99, 132, 0.2)',
                            borderColor: 'rgba(255, 99, 132, 1)',
                            borderWidth: 1,
                            hoverBackgroundColor: 'rgba(255, 99, 132, 0.4)',
                            hoverBorderColor: 'rgba(255, 99, 132, 1)',
                        }],
                    });
                    setDailySentimentClassificationData(stats.daily_sentiment_classification);
                    setWeeklySentimentClassificationData(stats.weekly_sentiment_classification);
                    // Assuming correlation_score_magnitude is meant for scatterData correlation
                    // This should be integrated into the scatterData state if you want to display it on the chart
                    // For example, as a title or annotation
                    // setCorrelationScoreMagnitude(stats.correlation_score_magnitude);
                    setSkewness(stats.skewness);
                    setKurtosis(stats.kurtosis);
                    // You might want to store the descriptions too, for display purposes
                    // setDescriptionSkewness(stats.skewness.description);
                    // setDescriptionKurtosis(stats.kurtosis.description);
                } else {
                    console.log("Error fetching statistics data");
                    history('/login');
                };
            } catch (error) {
                if (error.response && error.response.status === 401) {
                    const refreshed = await refreshToken();
                    if (refreshed) {
                        fetchStats(); // リフレッシュ成功後、プロファイル情報を再度取得
                    } else {
                        setTimeout(() => {
                            history('/login');
                        }, 100); 
                    }
                } else {
                    console.log('Error fetching profile data:', error);
                    setTimeout(() => {
                        history('/login');
                    }, 100); 
                }
            }
        };
        fetchStats();
    }, [history]);


    // Define chart options and data formats for each type of statistic
    const emotionChatOptions = {
        responsive: true,
        maintainAspectRatio: true, // グラフのアスペクト比を保つが、指定されたコンテナの大きさに合わせる
        aspectRatio: 3, // オプションでアスペクト比を指定することも可能（width : height）
        interaction: {
            mode: 'index',
            intersect: false,
        },
        plugins: {
            title: {
                display: true,
                text: 'Emotion Score and Chat Messages',
            },
            tooltip: {
                mode: 'index',
                intersect: false,
            },
        },
        scales: {
            y: {
                type: 'linear',
                display: true,
                position: 'left',
                title: {
                    display: true,
                    text: 'Emotion Score',
                },
                suggestedMax: 1,
                suggestedMin: -1,
            },
            y1: {
                type: 'linear',
                display: true,
                position: 'right',
                title: {
                    display: true,
                    text: 'Total Messages',
                },
                grid: {
                    drawOnChartArea: false,
                },
                grace: '5%'

            },
        },
    };


    const sentimentClassificationOptions = {
        responsive: true,
        maintainAspectRatio: true,
        aspectRatio: 3,
        scales: {
            x: {
                stacked: true,
            },
            y: {
                stacked: true,
                grace: '5%'
            }
        },
        plugins: {
            title: {
                display: true,
                text: 'Sentiment Classification'
            },
            tooltip: {
                mode: 'index',
                intersect: false
            }
        },
    };



    const scatterChartOptions = {
        responsive: true,
        maintainAspectRatio: true,
        aspectRatio: 3,
        plugins: {
            legend: {
                display: false // Assuming we don't need a legend for scatter plot
            },
            tooltip: {
                callbacks: {
                    label: function (context) {
                        // Custom tooltip label, you can include any data from your dataset
                        const label = context.dataset.label || '';
                        const dataPoint = context.parsed;
                        return `${label}: (Score: ${dataPoint.x}, Magnitude: ${dataPoint.y})`;
                    }
                }
            }
        },
        scales: {
            x: {
                type: 'linear',
                position: 'bottom',
                title: {
                    display: true,
                    text: 'Emotion Score'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Emotion Magnitude'
                },
                grace: '5%'
            }
        },
        elements: {
            point: {
                // Custom styling for points can go here, for example:
                radius: 5, // size of the data points
                backgroundColor: 'rgba(0, 123, 255, 0.5)', // color of the data points
                borderColor: 'rgba(0, 123, 255, 1)' // border color of the data points
            }
        }
    };


    const renderEmotionChatChart = (emotionData, chatData, options, cycle) => {
        // Process Emotion Data
        emotionData = Object.values(emotionData);
        const emotionLabels = cycle === "daily" ? emotionData.map(stat => stat.date) : emotionData.map(stat => stat.week);
        const emotionDatasetData = emotionData.map(stat => stat.avg_score);

        // Process Chat Data
        chatData = Object.values(chatData);
        const chatDatasetData = chatData.map(stat => stat.total_messages);

        // Assume labels are the same for both datasets (emotion and chat)
        const labels = emotionLabels;

        // Format the datasets for the combined chart
        const formattedData = {
            labels: labels,
            datasets: [
                {
                    label: 'Emotion Score',
                    data: emotionDatasetData,
                    type: 'line',
                    fill: false,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1,
                    yAxisID: 'y',
                },
                {
                    label: 'Total Messages',
                    data: chatDatasetData,
                    type: 'bar',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    yAxisID: 'y1',
                }
            ],
        };
        return <Bar data={formattedData} options={options} />;
    };

    const renderSentimentClassificationChart = (data, options, cycle) => {
        data = Object.values(data);
        const labels = cycle === "daily" ? data.map(stat => stat.date) : data.map(stat => stat.week);
        const positiveCounts = data.map(stat => stat.positive);
        const negativeCounts = data.map(stat => stat.negative);
        const neutralCounts = data.map(stat => stat.neutral);
        const mixedCounts = data.map(stat => stat.mixed);

        const chartData = {
            labels: labels,
            datasets: [
                {
                    label: 'Positive',
                    data: positiveCounts, // This should be an array of positive sentiment counts
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Negative',
                    data: negativeCounts, // This should be an array of negative sentiment counts
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Neutral',
                    data: neutralCounts, // This should be an array of neutral sentiment counts
                    backgroundColor: 'rgba(201, 203, 207, 0.2)',
                    borderColor: 'rgba(201, 203, 207, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Mixed',
                    data: mixedCounts, // This should be an array of mixed sentiment counts
                    backgroundColor: 'rgba(153, 102, 255, 0.2)',
                    borderColor: 'rgba(153, 102, 255, 1)',
                    borderWidth: 1
                }
            ]
        };

        return <Bar data={chartData} options={options} />;
    };

    const renderScatterChart = (data, options, correlationCoefficient) => {
        // If a correlation coefficient is provided, add it to the chart title
        if (correlationCoefficient) {
            options.plugins.title = {
                display: true,
                text: `Correlation Coefficient: ${correlationCoefficient.toFixed(2)}`
            };
        }

        return <Scatter data={data} options={options} />;
    };


    const TABS = {
        EMOTION_CHAT: 'emotion_chat',
        SCATTER: 'scatter',
        SENTIMENT_CLASSIFICATION: 'sentiment_classification'
    };

    const TIME_FRAMES = {
        DAILY: 'daily',
        WEEKLY: 'weekly'
    };

    // UI components like tabs and summary dashboard
    const renderTabs = () => {
        // Handle changing the main tabs
        const handleMainTabSelect = (selectedTab) => {
            setActiveMainTab(selectedTab);
        };

        // Handle changing the time frame (daily/weekly)
        const handleTimeFrameSelect = (timeFrame) => {
            setActiveTimeFrame(timeFrame);
        };

        const renderTimeFrameNav = () => {
            return (
                <Nav className="time-frame-nav justify-content nav-pills nav-pills-underline" activeKey={activeTimeFrame} onSelect={handleTimeFrameSelect}>
                    <Nav.Item>
                        <Nav.Link eventKey={TIME_FRAMES.DAILY}>Daily</Nav.Link>
                    </Nav.Item>
                    <Nav.Item>
                        <Nav.Link eventKey={TIME_FRAMES.WEEKLY}>Weekly</Nav.Link>
                    </Nav.Item>
                </Nav>
            );
        };

        return (
            <>
                <Tabs id="main-tabs" className="mb-3" activeKey={activeMainTab} onSelect={handleMainTabSelect}>
                    <Tab eventKey={TABS.EMOTION_CHAT} title="Emotion-Chat" />
                    <Tab eventKey={TABS.SCATTER} title="Scatter" />
                    <Tab eventKey={TABS.SENTIMENT_CLASSIFICATION} title="Sentiment Classification" />
                </Tabs>
                <div className="chart-container">
                    {activeMainTab !== TABS.SCATTER && renderTimeFrameNav()}
                    {activeMainTab === TABS.EMOTION_CHAT && renderEmotionChatChart(
                        activeTimeFrame === TIME_FRAMES.DAILY ? dailyEmotionData : weeklyEmotionData,
                        activeTimeFrame === TIME_FRAMES.DAILY ? dailyChatData : weeklyChatData,
                        emotionChatOptions,
                        activeTimeFrame
                    )}
                    {activeMainTab === TABS.SCATTER && renderScatterChart(scatterData, scatterChartOptions)}
                    {activeMainTab === TABS.SENTIMENT_CLASSIFICATION && renderSentimentClassificationChart(
                        activeTimeFrame === TIME_FRAMES.DAILY ? dailySentimentClassificationData : weeklySentimentClassificationData,
                        sentimentClassificationOptions,
                        activeTimeFrame
                    )}
                </div>
            </>
        );
    };


    const renderSummaryDashboard = () => {
        // Example summary elements. You would replace the content with actual data and elements as needed.
        const previousDayEmotionValue = dailyEmotionData[dailyEmotionData.length - 2]?.avg_score || 0;
        const latestEmotionValue = dailyEmotionData[dailyEmotionData.length - 1]?.avg_score || 0;
        const emotionChange = (latestEmotionValue - previousDayEmotionValue);

        const previousDayChatCount = dailyChatData[dailyChatData.length - 2]?.total_messages || 0;
        const latestChatCount = dailyChatData[dailyChatData.length - 1]?.total_messages || 0;
        const chatsChange = (latestChatCount - previousDayChatCount);

        const formatChange = (change) => {
            return change > 0 ? `+${change.toFixed(2)}` : change.toFixed(2);
        };

        const previousDayComparison = {
            emotion: `${formatChange(emotionChange)} points`,
            chats: `${formatChange(chatsChange)} messages`
        };

        return (
            <Nav variant="tabs" defaultActiveKey="summary">
                <Card style={{ width: '20rem', margin: '1rem' }}>
                    <Card.Body>
                        <Card.Title>Previous Day Comparison</Card.Title>
                        <Card.Text>
                            Emotion Change: {previousDayComparison.emotion}
                            <br />
                            Chat Volume Change: {previousDayComparison.chats}
                        </Card.Text>
                    </Card.Body>
                </Card>
                <Card style={{ width: '18rem', margin: '1rem' }}>
                    <Card.Body>
                        <Card.Title>Mental Trend (Skewness)</Card.Title>
                        <Card.Text>
                            {skewness.value}
                        </Card.Text>
                        <Card.Subtitle>
                            {skewness.description}
                        </Card.Subtitle>
                    </Card.Body>
                </Card>
                <Card style={{ width: '18rem', margin: '1rem' }}>
                    <Card.Body>
                        <Card.Title>Reliability (Kurtosis)</Card.Title>
                        <Card.Text>
                            {kurtosis.value}
                        </Card.Text>
                        <Card.Subtitle>
                            {kurtosis.description}
                        </Card.Subtitle>
                    </Card.Body>
                </Card>
            </Nav>
        );
    };



    // Main render function
    return (
        <div>
            <Header />
            <Container fluid>
                {renderSummaryDashboard()}
                {renderTabs()}

                {/* ...other UI elements */}
            </Container>
        </div>
    );
};
export default StatisticsPage;
