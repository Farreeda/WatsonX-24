// src/App.js
import React from "react";
import "./App.css";
import ReciveData from "./components/ReciveData";
import SendData from "./components/SendData";

function App() {
  
  return (
    <div className="App">
      <header className="App-header">
        <h1>My React App</h1>
        <ReciveData />
        <h2>My Form </h2>
        <SendData />
      </header>
    </div>
  );
}

export default App;
