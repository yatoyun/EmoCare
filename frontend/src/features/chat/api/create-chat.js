import { useMutation } from '@tanstack/react-query';
import { z } from 'zod';

import api from '@/lib/api';


export const createChatInputSchema = z.object({
  message: z.string().min(1, 'Required'),
});

export const createChat = async ({
  data,
}) => {
  const response = await api.post(`chat/`, data);
  return response.data;
};

export const useCreateChat = ({
  mutationConfig,
}) => {

  const { onSuccess, ...restConfig } = mutationConfig || {};

  return useMutation({
    onSuccess: (...args) => {
      onSuccess?.(...args);
    },
    ...restConfig,
    mutationFn: createChat,
  });
};