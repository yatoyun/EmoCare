import { Scatter } from 'react-chartjs-2';
import PropTypes from 'prop-types';

const ScatterChart = ({ scatterData, correlationScore }) => {
  const data = {
    datasets: [
      {
        label: 'Scatter Data',
        data: scatterData.map(([x, y]) => ({ x, y })),
        backgroundColor: 'rgba(0, 123, 255, 0.5)',
      },
    ],
  };

  const options = {
    responsive: true,
    scales: {
      x: { title: { display: true, text: 'Emotion Score' } },
      y: { title: { display: true, text: 'Emotion Magnitude' } },
    },
    plugins: {
      title: {
        display: true,
        text: `Scatter Plot (Correlation Coefficient: ${correlationScore || 'N/A'})`,
      },
    },
  };

  return <Scatter data={data} options={options} />;
};
ScatterChart.propTypes = {
  scatterData: PropTypes.array.isRequired,
  correlationScore: PropTypes.number,
};

export default ScatterChart;
