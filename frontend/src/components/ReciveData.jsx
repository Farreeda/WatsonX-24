// src/ReciveData.js
import React, { useState, useEffect } from 'react';
import ApiServices from './ApiServices';

const ReciveData = ({refresh}) => {
  const [data, setData] = useState(null); // State to store fetched data
  const [loading, setLoading] = useState(true); // State to manage loading status
  const [error, setError] = useState(null); // State to manage error status

  useEffect(() => {
    // Call FetchData when the component mounts
    ApiServices.GetData()
      .then((fetchedData) => {
        setData(fetchedData); // Update state with the fetched data
        setLoading(false); // Set loading to false once data is fetched
      })
      .catch((error) => {
        setError(error); // Update state with any error
        setLoading(false); // Set loading to false even if there's an error
      });
  }, [refresh]); // Empty dependency array means this useEffect runs once when the component mounts

  if (loading) return <p>Loading...</p>; // Display loading message
  if (error) return <p>Error: {error.message}</p>; // Display error message
  if (!data) return <p>No data available</p>; // Display if no data

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
