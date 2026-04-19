import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './pages/App';

test('renders apple stock prediction', () => {
  render(<App />);
  const headingElement = screen.getByText(/Apple Stock Price Prediction/i);
  expect(headingElement).toBeInTheDocument();
});
