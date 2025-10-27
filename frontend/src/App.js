import React from 'react';
import { AuthProvider } from './contexts/AuthContext';
import AuthWrapper from './components/AuthWrapper';
import './App.css';

function App() {
  return (
    <div className="App">
      <AuthProvider>
        <AuthWrapper />
      </AuthProvider>
    </div>
  );
}

export default App;
