import React from 'react'

export default class ApiServices {

    static SendChat(content){
        return fetch('http://localhost:5000/api/data',{
            'method':'POST',
             headers : {
            'Content-Type':'application/json'
      },
      body:JSON.stringify({content})
    })
    .then(response => response.json())
    .catch(error => console.log(error))
    }

    static GetData() {
        return fetch('http://localhost:5000/api/data', {
            'method': 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    }
}
