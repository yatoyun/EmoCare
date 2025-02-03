import { useState } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { Container } from '@/components/ui/container';
import { Card } from '@/components/ui/card';

import { MessageList } from '@/features/chat/components/message-list';
import { ChatInput } from '@/features/chat/components/chat-input';
import { useGetChatHistory } from '@/features/chat/api/get-chat-history';
import { useCreateChat } from '@/features/chat/api/create-chat';

function Chat() {
  const queryClient = useQueryClient();
  const [localMessages, setLocalMessages] = useState([]);
  const { data: serverMessages = [] } = useGetChatHistory();
  const messages = [...serverMessages, ...localMessages];

  const createChat = useCreateChat({
    mutationConfig: {
      onSuccess: () => {
        setLocalMessages([]);
        queryClient.invalidateQueries(['chat-history']);
      },
    },
  });

  const handleSendMessage = (message) => {
    if (message.trim()) {
      // 即座にユーザーメッセージを表示
      setLocalMessages([
        {
          role: 'user',
          content: message,
        }
      ]);
      createChat.mutate({ data: { message } });
    }
  };
  console.log(createChat.isPending)

  return (
    <Container>
      <div className="flex flex-col h-[calc(100vh-8rem)] gap-4">
        <div className="flex-none">
          <h2 className="text-2xl font-bold">Chat with AI</h2>
        </div>
        <div className="flex-1 flex flex-col">
          <MessageList
            messages={messages}
            isLoading={createChat.isPending}
          />
        </div>
        <div className="flex-none">
          <Card className="p-4">
            <ChatInput
              onSendMessage={handleSendMessage}
              isLoading={createChat.isPending}
            />
          </Card>
        </div>
      </div>
    </Container>
  );
}

export default Chat;

