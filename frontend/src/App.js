// src/App.js
import React,{useState} from "react";
import "./App.css";
import ReciveData from "./components/ReciveData";
import ChatBox from "./components/ChatBox";
// import io from 'socket.io-client';

// const socket = io('http://localhost:5000');  

function App() {
  const [refreshData, setRefreshData] = useState(false);

  const handleDataSent = () => {
    // Trigger a data refresh
    setRefreshData((prev) => !prev);
  };
  return (
    <div className="App">
      <div className="App-header">
        <h1>DocuBot</h1>
        <ReciveData refresh={refreshData} />
        <ChatBox onDataSent={handleDataSent} />
      </div>
    </div>
  );
}

export default App;
