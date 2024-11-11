import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [data, setData] = useState("");
  const [functionName, setFunctionName] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/")
      .then(response => response.json())
      .then(data => {
        setFunctionName(data.function_name); 
        setData(data.text); 
      })
      .catch(error => console.error("Error fetching data:", error));
  }, []);

  return (
    <div className="container">
      <div className="cell">
        <h1>{functionName}</h1>
        <p>{data}</p>
      </div>
    </div>
  );
}

export default App;
