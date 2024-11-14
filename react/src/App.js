
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
    <RadarChart outerRadius={90} width={500} height={500} data={param} >
      <PolarGrid />
      <PolarAngleAxis dataKey="subject" />
      <PolarRadiusAxis tick={false} axisLine={false} domain={[0, 10]} tickCount={10}/>
      <Radar name="Mike" dataKey="A" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} dot/>
    </RadarChart>
  );
};

export default App;

