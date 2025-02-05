import { useQuery } from '@tanstack/react-query';
import { z } from 'zod';

import api from '@/lib/api';

export const statisticsResponseSchema = z.object({
  daily_emotion_stats: z.array(z.object({
    date: z.string(),
    avg_score: z.number(),
    count: z.number()
  })),
  daily_chat_stats: z.array(z.object({
    date: z.string(),
    total_messages: z.number()
  })),
  weekly_emotion_stats: z.array(z.object({
    week: z.string(),
    avg_score: z.number(),
    count: z.number()
  })),
  weekly_chat_stats: z.array(z.object({
    week: z.string(),
    total_messages: z.number()
  })),
  daily_sentiment_classification: z.array(z.object({
    date: z.string(),
    positive: z.number(),
    negative: z.number(),
    neutral: z.number(),
    mixed: z.number()
  })),
  weekly_sentiment_classification: z.array(z.object({
    week: z.string(),
    positive: z.number(),
    negative: z.number(),
    neutral: z.number(),
    mixed: z.number()
  })),
  correlation_score_magnitude: z.number(),
  skewness: z.object({
    value: z.number(),
    description: z.string()
  }),
  kurtosis: z.object({
    value: z.number(),
    description: z.string()
  }),
  scatter_data: z.array(z.tuple([z.number(), z.number()])),
});

const getStatistics = async () => {
  try {
    const response = await api.get('statistics/');

    console.log('Statistics API response:', response);
    const validated = statisticsResponseSchema.safeParse(response);
    if (!validated.success) {
      console.error('Validation errors:', validated.error);
      throw new Error('Data validation failed');
    }

    return validated.data;
  } catch (error) {
    console.error('Statistics API error:', error);
    throw error;
  }
};

export const useGetStatistics = (queryConfig = {}) => {
  return useQuery({
    queryKey: ['statistics'],
    queryFn: getStatistics,
    ...queryConfig,
    retry: 1, // リトライ回数を制限
  });
};