import React, { useEffect, useState } from 'react';
import {
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Legend,
} from 'recharts';

const testCompetencyData = {
  "Data Analytics": [
    ["Data Cleaning", 1.2],
    ["Statistical Analysis", 9.8],
    ["Data Visualization", 3.9],
    ["Machine Learning", 7.1],
    ["Data Mining", 5.8]
  ],
  "Web Development": [
    ["HTML/CSS", 8.6],
    ["JavaScript", 9.9],
    ["React", 7.1]
  ],
  "Backend": [
    ["Node.js", 8.5],
    ["Python (Django)", 1.8],
    ["Java (Spring)", 5.9],
    ["T", 3.7]
  ],
  "Machine Learning": [
    ["Python", 6.4],
    ["TensorFlow", 8.2],
    ["Keras", 7.5],
    ["R", 4.1],
    ["Pandas", 9.3]
  ]
};

const CompetencyRadarChart = () => {
  const [competencies, setCompetencies] = useState([]);

  useEffect(() => {
    const chartData = Object.entries(testCompetencyData).map(([competencyName, skills]) => ({
      competencyName,
      skillsData: skills.map(([skillName, skillLevel]) => ({ subject: skillName, value: skillLevel })),
    }));
    setCompetencies(chartData);
  }, []);

  return (
    <div>
      {competencies.map(({ competencyName, skillsData }) => (
        <div key={competencyName}>
          <RadarChart outerRadius={90} width={400} height={355} data={skillsData}>
            <PolarGrid />
            <PolarAngleAxis dataKey="subject" />
            <PolarRadiusAxis tick={false} axisLine={false} domain={[0, 10]} />
            <Radar
              name={competencyName}
              dataKey="value"
              stroke="#8884d8"
              fill="#8884d8"
              fillOpacity={0.6}
              dot
            />
            <Legend verticalAlign="bottom" height={55} />
          </RadarChart>
        </div>
      ))}
    </div>
  );
};

export default CompetencyRadarChart;
