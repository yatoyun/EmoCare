import React, { useEffect, useState } from 'react';
import { Bar, Scatter } from 'react-chartjs-2';
import { Chart as ChartJS, registerables } from 'chart.js';
import 'chartjs-adapter-date-fns';
import api from '../configs/api';

ChartJS.register(...registerables);

function Statistics() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    api.get('statistics/')
      .then((response) => setStats(response.data))
      .catch((error) => console.error('Error fetching user stats:', error));
  }, []);

  if (!stats) {
    return <div>Loading statistics...</div>;
  }

  // Daily and Weekly Emotion-Chat Chart Data
  const processEmotionChatData = (emotionData, chatData, timeKey) => {
    const labels = emotionData.map(stat => stat[timeKey]);
    const emotionScores = emotionData.map(stat => stat.avg_score);
    const totalMessages = chatData.map(stat => stat.total_messages);

    return {
      labels,
      datasets: [
        {
          label: 'Emotion Score',
          data: emotionScores,
          type: 'line',
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1,
          yAxisID: 'y',
        },
        {
          label: 'Total Messages',
          data: totalMessages,
          type: 'bar',
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgba(54, 162, 235, 1)',
          yAxisID: 'y1',
        },
      ],
    };
  };

  const emotionChatOptions = {
    responsive: true,
    scales: {
      y: {
        type: 'linear',
        position: 'left',
        title: { text: 'Emotion Score', display: true },
      },
      y1: {
        type: 'linear',
        position: 'right',
        title: { text: 'Total Messages', display: true },
        grid: { drawOnChartArea: false },
      },
    },
    plugins: {
      title: { display: true, text: 'Emotion-Chat Overview' },
    },
  };

  const dailyEmotionChatData = processEmotionChatData(
    stats.daily_emotion_stats,
    stats.daily_chat_stats,
    'date'
  );
  const weeklyEmotionChatData = processEmotionChatData(
    stats.weekly_emotion_stats,
    stats.weekly_chat_stats,
    'week'
  );

  // Sentiment Classification Chart Data
  const processSentimentClassificationData = (data, timeKey) => {
    const labels = data.map(stat => stat[timeKey]);
    return {
      labels,
      datasets: [
        { label: 'Positive', data: data.map(stat => stat.positive), backgroundColor: 'rgba(75, 192, 192, 0.2)' },
        { label: 'Negative', data: data.map(stat => stat.negative), backgroundColor: 'rgba(255, 99, 132, 0.2)' },
        { label: 'Neutral', data: data.map(stat => stat.neutral), backgroundColor: 'rgba(201, 203, 207, 0.2)' },
        { label: 'Mixed', data: data.map(stat => stat.mixed), backgroundColor: 'rgba(153, 102, 255, 0.2)' },
      ],
    };
  };

  const sentimentClassificationOptions = {
    responsive: true,
    scales: {
      x: { stacked: true },
      y: { stacked: true },
    },
    plugins: {
      title: { display: true, text: 'Sentiment Classification' },
    },
  };

  const dailySentimentData = processSentimentClassificationData(
    stats.daily_sentiment_classification,
    'date'
  );
  const weeklySentimentData = processSentimentClassificationData(
    stats.weekly_sentiment_classification,
    'week'
  );

  // Scatter Chart Data
  const scatterData = {
    datasets: [
      {
        label: 'Scatter Data',
        data: stats.scatter_data.map(([x, y]) => ({ x, y })),
        backgroundColor: 'rgba(0, 123, 255, 0.5)',
      },
    ],
  };

  const scatterOptions = {
    responsive: true,
    scales: {
      x: { title: { display: true, text: 'Emotion Score' } },
      y: { title: { display: true, text: 'Emotion Magnitude' } },
    },
    plugins: {
      title: {
        display: true,
        text: `Scatter Plot (Correlation Coefficient: ${stats.correlation_score_magnitude || 'N/A'})`,
      },
    },
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Your Mood Statistics</h2>
      <div className="bg-white rounded-lg shadow-md p-4">
        <div className="mb-4">
          <h3 className="text-lg font-semibold">Daily Emotion-Chat</h3>
          <Bar data={dailyEmotionChatData} options={emotionChatOptions} />
        </div>
        <div className="mb-4">
          <h3 className="text-lg font-semibold">Weekly Emotion-Chat</h3>
          <Bar data={weeklyEmotionChatData} options={emotionChatOptions} />
        </div>
        <div className="mb-4">
          <h3 className="text-lg font-semibold">Daily Sentiment Classification</h3>
          <Bar data={dailySentimentData} options={sentimentClassificationOptions} />
        </div>
        <div className="mb-4">
          <h3 className="text-lg font-semibold">Weekly Sentiment Classification</h3>
          <Bar data={weeklySentimentData} options={sentimentClassificationOptions} />
        </div>
        <div className="mb-4">
          <h3 className="text-lg font-semibold">Scatter Plot</h3>
          <Scatter data={scatterData} options={scatterOptions} />
        </div>
      </div>
    </div>
  );
}

export default Statistics;
