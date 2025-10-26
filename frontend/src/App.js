import React, { useState } from 'react';
import QuestionForm from './components/QuestionForm';
import Quiz from './components/Quiz';
import './App.css';

function App() {
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

  return (
    <div className="App">
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
}

export default App;
