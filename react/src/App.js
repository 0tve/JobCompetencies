
import React from 'react';
import {
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
} from 'recharts';

const param = [
  {
    subject: 'JavaScript', A: 3.5, fullMark: 10,
  },
  {
    subject: 'React', A: 9.8, fullMark: 10,
  },
  {
    subject: 'CSS', A: 8.6, fullMark: 10,
  },
  {
    subject: 'HTML', A: 6.7, fullMark: 10,
  },
  {
    subject: 'NodeJS', A: 5.1, fullMark: 10,
  },
  {
    subject: 'Pyhone', A: 2.1, fullMark: 10,
  },
];

const App = () => {
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
