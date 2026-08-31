import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { SimulationProvider } from './context/SimulationContext';
import AppRouter from './router/AppRouter';

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <SimulationProvider>
          <AppRouter />
        </SimulationProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
