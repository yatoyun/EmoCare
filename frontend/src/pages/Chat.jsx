import React, { useState, useEffect } from 'react'
import { useSelector } from 'react-redux'
import api from '../configs/api'

function Chat() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const user = useSelector((state) => state.auth.user)

  useEffect(() => {
    // Fetch chat history
    api.get('chat-history/')
      .then((response) => setMessages(response.data))
      .catch((error) => console.error('Error fetching chat history:', error))
  }, [])

  const sendMessage = async () => {
    if (input.trim()) {
      try {
        const response = await api.post('chat/', { message: input })
        setMessages([...messages, { role: 'user', content: input }, response.data])
        setInput('')
      } catch (error) {
        console.error('Error sending message:', error)
      }
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Chat with AI</h2>
      <div className="bg-white rounded-lg shadow-md p-4 mb-4 h-96 overflow-y-auto">
        {messages.map((message, index) => (
          <div key={index} className={`mb-2 ${message.role === 'user' ? 'text-right' : 'text-left'}`}>
            <span className={`inline-block p-2 rounded-lg ${message.role === 'user' ? 'bg-blue-100' : 'bg-gray-100'}`}>
              {message.content}
            </span>
          </div>
        ))}
      </div>
      <div className="flex">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-grow px-3 py-2 border rounded-l"
          placeholder="Type your message..."
        />
        <button
          onClick={sendMessage}
          className="bg-blue-500 text-white px-4 py-2 rounded-r hover:bg-blue-600"
        >
          Send
        </button>
      </div>
    </div>
  )
}

export default Chat

