import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import Login from './Login';
import Register from './Register';
import Header from './Header';
import Dashboard from './Dashboard';
import QuestionForm from './QuestionForm';
import Quiz from './Quiz';

const AuthWrapper = () => {
  const { isAuthenticated, loading } = useAuth();
  const [showRegister, setShowRegister] = useState(false);
  const [questions, setQuestions] = useState([]);
  const [topic, setTopic] = useState('');
  const [currentView, setCurrentView] = useState('dashboard'); // dashboard, quiz-form, quiz

  const handleQuestionsGenerated = (generatedQuestions, selectedTopic) => {
    setQuestions(generatedQuestions);
    setTopic(selectedTopic);
    setCurrentView('quiz');
  };

  const handleBackToForm = () => {
    console.log('🔙 Going back to form - clearing quiz data');
    setCurrentView('quiz-form');
    setQuestions([]);
    setTopic('');
    // Clear any resuming quiz ID to ensure fresh start
    localStorage.removeItem('resumingQuizId');
  };

  const handleBackToDashboard = () => {
    console.log('🔙 Going back to dashboard - clearing quiz data');
    setCurrentView('dashboard');
    setQuestions([]);
    setTopic('');
    // Clear any resuming quiz ID
    localStorage.removeItem('resumingQuizId');
  };

  const handleNavigateToQuiz = () => {
    setCurrentView('quiz-form');
  };

  const handleResumeQuiz = (quizQuestions, quizTopic, quizId) => {
    console.log('=== AUTHWRAPPER RESUME ===');
    console.log('Questions received:', quizQuestions?.length || 'undefined');
    console.log('Topic:', quizTopic);
    console.log('Quiz ID:', quizId);
    
    if (!quizQuestions || quizQuestions.length === 0) {
      console.error('No questions provided to resume quiz');
      alert('Error: No questions found for this quiz');
      return;
    }
    
    setQuestions(quizQuestions);
    setTopic(quizTopic);
    localStorage.setItem('resumingQuizId', quizId.toString());
    
    console.log('Setting current view to quiz...');
    setCurrentView('quiz');
    
    console.log('AuthWrapper: Successfully set up resume quiz');
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

  const handleNavigate = (view) => {
    setCurrentView(view);
    setQuestions([]);
    setTopic('');
  };

  // Show main application if authenticated
  return (
    <div>
      <Header currentView={currentView} onNavigate={handleNavigate} />
      {currentView === 'dashboard' && (
        <Dashboard 
          onNavigateToQuiz={handleNavigateToQuiz} 
          onResumeQuiz={handleResumeQuiz}
        />
      )}
      {currentView === 'quiz-form' && (
        <QuestionForm 
          onQuestionsGenerated={handleQuestionsGenerated}
          onBackToDashboard={handleBackToDashboard}
        />
      )}
      {currentView === 'quiz' && (
        <Quiz 
          questions={questions} 
          topic={topic} 
          onBackToForm={handleBackToForm}
          onBackToDashboard={handleBackToDashboard}
        />
      )}
    </div>
  );
};

export default AuthWrapper;