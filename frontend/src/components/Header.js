import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import './Header.css';

const Header = ({ currentView, onNavigate }) => {
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
  };

  return (
    <header className="app-header">
      <div className="header-content">
        <h1 className="app-title">AI Question Generator</h1>
        
        <nav className="nav-section">
          <button 
            onClick={() => onNavigate && onNavigate('dashboard')}
            className={`nav-btn ${currentView === 'dashboard' ? 'active' : ''}`}
          >
            Dashboard
          </button>
          <button 
            onClick={() => onNavigate && onNavigate('quiz-form')}
            className={`nav-btn ${currentView === 'quiz-form' ? 'active' : ''}`}
          >
            Generate Quiz
          </button>
        </nav>
        
        <div className="user-section">
          <span className="welcome-text">Welcome, {user?.username}!</span>
          <button onClick={handleLogout} className="logout-btn">
            Logout
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;