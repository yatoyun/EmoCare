import { Bar } from 'react-chartjs-2';
import PropTypes from 'prop-types';

const EmotionChatChart = ({ emotionData, chatData, timeKey }) => {
  const labels = emotionData.map(stat => stat[timeKey]);
  const emotionScores = emotionData.map(stat => stat.avg_score);
  const totalMessages = chatData.map(stat => stat.total_messages);

  const data = {
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

  const options = {
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

  return <Bar data={data} options={options} />;
};
EmotionChatChart.propTypes = {
  emotionData: PropTypes.array.isRequired,
  chatData: PropTypes.array.isRequired,
  timeKey: PropTypes.string.isRequired,
};

export default EmotionChatChart;
