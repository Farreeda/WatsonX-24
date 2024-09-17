// src/components/ChatBox.jsx 
  
import React, { useState } from "react";
import ApiServices from './ApiServices';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button'

export default function ChatBox({ onDataSent }) {
  const [inputData, setInputData] = useState("");

  // Handle change in input field
  const handleChange = (event) => {
    setInputData(event.target.value);
  };

  // Handle form submission
  const handleSubmit = (event) => {
    event.preventDefault(); // Prevent the default form submission behavior

    // Call the SendChat method from ApiServices
    ApiServices.SendChat(inputData)
      .then(response => {
        console.log('Response from server:', response);
      })
      .catch(error => {
        console.error('Error sending data:', error);
      });
      
    onDataSent();  // Notify parent to refresh data

    // Clear the input field after submission (optional)
    setInputData('');


  };
  return (
    
    <Box
      component="form"
      sx={{ '& > :not(style)': { m: 1, width: '70ch' } }}
      noValidate
      onSubmit={handleSubmit}
      autoComplete="off"
    >
        <TextField
          id="filled-textarea"
          label="Ask me"
          placeholder="Placeholder"
          variant="filled"
          value={inputData}
          onChange={handleChange}
        />
      <Button variant="contained" type="submit">
        Send
      </Button>
    </Box>
  );
}