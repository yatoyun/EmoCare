import { useState } from 'react';
import { Container } from '@/components/ui/container';
import { Card } from '@/components/ui/card';

import { MessageList } from '@/features/chat/components/message-list';
import { ChatInput } from '@/features/chat/components/chat-input';
import { useGetChatHistory } from '@/features/chat/api/get-chat-history';
import { useCreateChat } from '@/features/chat/api/create-chat';

function Chat() {
  const { data: serverMessages = [] } = useGetChatHistory();
  const [pendingMessages, setPendingMessages] = useState([]);
  const messages = [...serverMessages, ...pendingMessages];

  const createChat = useCreateChat({
    mutationConfig: {
      onSuccess: (response) => {
        // 保留中のメッセージを更新
        setPendingMessages(prevMessages => {
          if (!response) {
            // エラー時は保留中のメッセージを削除
            return prevMessages.filter(msg => !msg.isLoading);
          }

          const updatedMessages = prevMessages.map(msg => {
            if (msg.isLoading) {
              return {
                role: 'gpt',
                content: response,
              };
            }
            return msg;
          });
          return updatedMessages;
        });
      },
    },
  });

  const handleSendMessage = (message) => {
    if (message.trim()) {
      // 保留中のメッセージを追加
      setPendingMessages([
        ...pendingMessages,
        {
          role: 'user',
          content: message,
        },
        {
          role: 'gpt',
          content: 'AI is typing...',
          isLoading: true,
        }
      ]);
      createChat.mutate({
        data: { message }
      });
    }
  };

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

