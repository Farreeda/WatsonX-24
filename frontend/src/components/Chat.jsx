// src/components/Chat.js
import React, { useState } from 'react';
import axios from 'axios';
import Message from './Message';
import MessageInput from './MessageInput';
import './Chat.css'; 
import FileTree from './FileTree';

const Chat = () => {

  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false); // State to manage loading

  const sendMessage = async (userInput) => {
    const userMessage = { message: userInput };
    setMessages((prevMessages) => [...prevMessages, { text: userInput, sender: 'user' }]);
    setLoading(true); // Set loading to true before the API call

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/chat', userMessage);
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: response.data.response, sender: 'bot' },
      ]);
    } catch (error) {
      console.error("Error sending message:", error);
      // Handle error appropriately here (e.g., show an error message)
    } finally {
      setLoading(false); // Reset loading state
    }
  };

  const handleClear = async () => {
    const response = await fetch('http://127.0.0.1:5000/api/clear', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: 'Clear!' }),
    });

    if (response.ok) {
      const data = await response.json();
      console.log(data);
    } else {
      console.error('Error:', response.statusText);
    }
    setMessages([]); // Clear messages

  };
;

  return (
    <div className="container text-center">
      <div class="row">
        <div class="col-6">
      <div className="container mt-5">
        <div className="card">
          <div className="card-header">
            <h3>DocuBot</h3>
          </div>

          <div className="card-body" style={{ height: '400px', overflowY: 'scroll' }}>
            {messages.length === 0 ? (
              <p className="text-center">No messages yet!</p>
            ) : (
              <div className="messages">
                {messages.map((msg, index) => (
                  <Message key={index} text={msg.text} sender={msg.sender} />
                ))}
              </div>
            )}
            {loading && <div className="loading">Loading...</div>} {/* Loading indicator */}
          </div>
          <div className="card-footer">
            <MessageInput onSend={sendMessage} />
            <br />
            <button className="btn btn-danger" onClick={handleClear}>Clear Chat</button>
          </div>
        </div>
      </div>
      </div>
      <div className="col">
        <FileTree />
      </div>
      </div>
    </div>
  );
};

export default Chat;
