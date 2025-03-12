import { useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import { Card } from '@/components/ui/card';
import { TextCard } from '@/components/ui/text-card';
import { LoadingDots } from './loading-dots';

export const MessageList = ({ messages, isLoading }) => {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  return (
    <Card className="h-[500px] p-6 mb-4 overflow-y-auto bg-gray-50">
      <div className="space-y-6">
        {messages.map((message, index) => (
          <TextCard role={message.role} key={index}>
            {message.isLoading ? <LoadingDots /> : message.content}
          </TextCard>
        ))}
        <div ref={messagesEndRef} />
      </div>
    </Card>
  );
};

MessageList.propTypes = {
  messages: PropTypes.arrayOf(
    PropTypes.shape({
      role: PropTypes.oneOf(['user', 'gpt']).isRequired,
      content: PropTypes.string.isRequired,
    }),
  ),
  isLoading: PropTypes.bool,
};