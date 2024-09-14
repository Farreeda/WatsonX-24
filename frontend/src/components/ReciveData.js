// src/ReciveData.js
import React, { useState, useEffect } from 'react';

const ReciveData = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('http://localhost:5000/api/data')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        setData(data);
        setLoading(false);
      })
      .catch(error => {
        setError(error);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <div>
      <h2>Data from Flask API</h2>
      <p>{data.id}</p>
      <ul>
        {data.map((item) => (
          <li key={item.id}>{item.content}</li>
        ))}
      </ul>     
    </div>
  );
};

export default ReciveData;
