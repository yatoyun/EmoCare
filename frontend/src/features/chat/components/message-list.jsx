import { useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import { Card } from '@/components/ui/card';
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
          <div
            key={index}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            {message.role === 'gpt' && (
              <div className="w-2 h-2 mt-2 mr-2 rounded-full bg-emerald-500" />
            )}
            <div
              className={`max-w-[80%] rounded-2xl px-5 py-3.5 ${
                message.role === 'user'
                  ? 'bg-blue-600 text-white shadow-md'
                  : 'bg-white text-gray-800 shadow-md border border-gray-100'
              }`}
            >
              {message.content}
            </div>
          </div>
        ))}
        {isLoading && messages.length > 0 && messages[messages.length - 1]?.role === 'user' && (
          <div className="flex justify-start">
            <div className="w-2 h-2 mt-2 mr-2 rounded-full bg-emerald-500" />
            <div className="max-w-[80%] rounded-2xl px-5 py-3.5 bg-white text-gray-800 shadow-md border border-gray-100">
              <LoadingDots />
            </div>
          </div>
        )}
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