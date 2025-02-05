import { Bar } from 'react-chartjs-2';
import PropTypes from 'prop-types';

const SentimentChart = ({ data, timeKey }) => {
  const labels = data.map(stat => stat[timeKey]);
  const chartData = {
    labels,
    datasets: [
      { label: 'Positive', data: data.map(stat => stat.positive), backgroundColor: 'rgba(75, 192, 192, 0.2)' },
      { label: 'Negative', data: data.map(stat => stat.negative), backgroundColor: 'rgba(255, 99, 132, 0.2)' },
      { label: 'Neutral', data: data.map(stat => stat.neutral), backgroundColor: 'rgba(201, 203, 207, 0.2)' },
      { label: 'Mixed', data: data.map(stat => stat.mixed), backgroundColor: 'rgba(153, 102, 255, 0.2)' },
    ],
  };

  const options = {
    responsive: true,
    scales: {
      x: { stacked: true },
      y: { stacked: true },
    },
    plugins: {
      title: { display: true, text: 'Sentiment Classification' },
    },
  };

  return <Bar data={chartData} options={options} />;
};
SentimentChart.propTypes = {
  data: PropTypes.array.isRequired,
  timeKey: PropTypes.string.isRequired,
};

export default SentimentChart;
