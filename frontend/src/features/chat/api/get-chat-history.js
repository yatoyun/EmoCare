import { useQuery } from '@tanstack/react-query';
import { z } from 'zod';

import api from '@/lib/api';

export const chatHistoryResponseSchema = z.array(
  z.object({
    user_message: z.string(),
    gpt_response: z.string(),
  })
);

const getChatHistory = async () => {
  const response = await api.get('chat/history/');
  const validated = chatHistoryResponseSchema.parse(response);
  return validated.reverse().flatMap((entry) => [
    { role: 'user', content: entry.user_message },
    { role: 'gpt', content: entry.gpt_response },
  ]);
};

export const useGetChatHistory = (queryConfig = {}) => {
  return useQuery({
    queryKey: ['chat-history'],
    queryFn: getChatHistory,
    ...queryConfig,
  });
};