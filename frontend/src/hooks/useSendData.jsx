// src/hooks/useSendData.js
import { useState } from "react";

export const useSendData = () => {
  const [error, setError] = useState(null);

  const sendData = async (data) => {
    try {
      const response = await fetch("http://localhost:5000/api/data", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      return await response.json();
    } catch (err) {
      setError(err.message);
      return null;
    }
  };

  return { sendData, error };
};
