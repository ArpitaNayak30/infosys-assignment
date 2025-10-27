import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import Login from './Login';
import Register from './Register';
import Header from './Header';
import QuestionForm from './QuestionForm';
import Quiz from './Quiz';

const AuthWrapper = () => {
  const { isAuthenticated, loading } = useAuth();
  const [showRegister, setShowRegister] = useState(false);
  const [questions, setQuestions] = useState([]);
  const [topic, setTopic] = useState('');
  const [showQuiz, setShowQuiz] = useState(false);

  const handleQuestionsGenerated = (generatedQuestions, selectedTopic) => {
    setQuestions(generatedQuestions);
    setTopic(selectedTopic);
    setShowQuiz(true);
  };

  const handleBackToForm = () => {
    setShowQuiz(false);
    setQuestions([]);
    setTopic('');
  };

  const handleSwitchToRegister = () => {
    setShowRegister(true);
  };

  const handleSwitchToLogin = () => {
    setShowRegister(false);
  };

  // Show loading spinner while checking authentication
  if (loading) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white',
        fontSize: '1.2rem'
      }}>
        Loading...
      </div>
    );
  }

  // Show authentication forms if not authenticated
  if (!isAuthenticated()) {
    return showRegister ? (
      <Register onSwitchToLogin={handleSwitchToLogin} />
    ) : (
      <Login onSwitchToRegister={handleSwitchToRegister} />
    );
  }

  // Show main application if authenticated
  return (
    <div>
      <Header />
      {showQuiz ? (
        <Quiz 
          questions={questions} 
          topic={topic} 
          onBackToForm={handleBackToForm}
        />
      ) : (
        <QuestionForm onQuestionsGenerated={handleQuestionsGenerated} />
      )}
    </div>
  );
};

export default AuthWrapper;