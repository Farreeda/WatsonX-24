// src/components/Message.jsx
import React from 'react';
import './Message.css'; 

const Message = ({ text, sender }) => {
  return (
    <div class="input-group mb-3">

    <div className={sender} >
      {text}
    </div>
    </div>
  );
};

export default Message;