import React from 'react';

const TestApp: React.FC = () => {
  return (
    <div style={{ padding: '20px', fontSize: '18px', color: 'blue' }}>
      <h1>Test Page - If you can see this, React is working!</h1>
      <p>Current time: {new Date().toLocaleString()}</p>
    </div>
  );
};

export default TestApp;
