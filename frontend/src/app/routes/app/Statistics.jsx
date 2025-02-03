import { useState } from 'react';
import { Chart as ChartJS, registerables } from 'chart.js';
import 'chartjs-adapter-date-fns';
import { Button } from '@/components/ui/button';
import { Container } from '@/components/ui/container';
import { useGetStatistics } from '@/features/statistics/api/get-statistics';
import EmotionChatChart from '@/features/statistics/components/EmotionChatChart';
import SentimentChart from '@/features/statistics/components/SentimentChart';
import ScatterChart from '@/features/statistics/components/ScatterChart';

ChartJS.register(...registerables);

function Statistics() {
  const { data: stats, isLoading, error } = useGetStatistics();
  const [timeRange, setTimeRange] = useState('daily');
  const [chartType, setChartType] = useState('emotion-chat');

  if (isLoading) {
    return <div>Loading statistics...</div>;
  }

  if (error) {
    return (
      <Container>
        <div className="p-4 bg-red-50 border border-red-200 rounded-md">
          <h3 className="text-lg font-semibold text-red-800">Error loading statistics</h3>
          <p className="text-red-600">{error.message}</p>
          {error.cause && (
            <pre className="mt-2 text-sm text-red-500 bg-red-50 p-2 rounded">
              {JSON.stringify(error.cause, null, 2)}
            </pre>
          )}
        </div>
      </Container>
    );
  }

  if (!stats || Object.keys(stats).length === 0) {
    return <div>No statistics data available</div>;
  }

  const renderChart = () => {
    switch (chartType) {
      case 'emotion-chat':
        return (
          <EmotionChatChart
            emotionData={timeRange === 'daily' ? stats.daily_emotion_stats : stats.weekly_emotion_stats}
            chatData={timeRange === 'daily' ? stats.daily_chat_stats : stats.weekly_chat_stats}
            timeKey={timeRange === 'daily' ? 'date' : 'week'}
          />
        );
      case 'sentiment':
        return (
          <SentimentChart
            data={timeRange === 'daily' ? stats.daily_sentiment_classification : stats.weekly_sentiment_classification}
            timeKey={timeRange === 'daily' ? 'date' : 'week'}
          />
        );
      case 'scatter':
        return (
          <ScatterChart
            scatterData={stats.scatter_data}
            correlationScore={stats.correlation_score_magnitude}
          />
        );
      default:
        return null;
    }
  };

  return (
    <Container>
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Your Mood Statistics</h2>
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="space-y-3">
          <div className="flex gap-2 p-1 bg-orange-50 rounded-lg w-fit">
            <Button
              variant={timeRange === 'daily' ? 'default' : 'ghost'}
              onClick={() => setTimeRange('daily')}
              className={`transition-all duration-200 ${
                timeRange === 'daily' ? 'shadow-md' : ''
              }`}
            >
              Daily
            </Button>
            <Button
              variant={timeRange === 'weekly' ? 'default' : 'ghost'}
              onClick={() => setTimeRange('weekly')}
              className={`transition-all duration-200 ${
                timeRange === 'weekly' ? 'shadow-md' : ''
              }`}
            >
              Weekly
            </Button>
          </div>
          <div className="flex gap-2 p-1 bg-orange-50 rounded-lg w-fit">
            <Button
              variant={chartType === 'emotion-chat' ? 'default' : 'ghost'}
              onClick={() => setChartType('emotion-chat')}
              className={`transition-all duration-200 ${
                chartType === 'emotion-chat' ? 'shadow-md' : ''
              }`}
            >
              Emotion-Chat
            </Button>
            <Button
              variant={chartType === 'sentiment' ? 'default' : 'ghost'}
              onClick={() => setChartType('sentiment')}
              className={`transition-all duration-200 ${
                chartType === 'sentiment' ? 'shadow-md' : ''
              }`}
            >
              Sentiment
            </Button>
            <Button
              variant={chartType === 'scatter' ? 'default' : 'ghost'}
              onClick={() => setChartType('scatter')}
              className={`transition-all duration-200 ${
                chartType === 'scatter' ? 'shadow-md' : ''
              }`}
            >
              Scatter
            </Button>
          </div>
        </div>
        <div className="mt-3">
          {renderChart()}
        </div>
      </div>
    </Container>
  );
}

export default Statistics;
