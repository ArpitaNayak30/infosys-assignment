import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import './QuestionForm.css';

const QuestionForm = ({ onQuestionsGenerated, onBackToDashboard }) => {
  const [topic, setTopic] = useState('');
  const [numberQuestions, setNumberQuestions] = useState(5);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const { token } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!topic.trim()) {
      setError('Please enter a topic');
      return;
    }

    if (numberQuestions < 1 || numberQuestions > 20) {
      setError('Number of questions must be between 1 and 20');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch('http://127.0.0.1:8000/api/generate-questions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          topic: topic.trim(),
          number_questions: numberQuestions
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      onQuestionsGenerated(data.questions, topic);
    } catch (err) {
      setError(`Failed to generate questions: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="question-form-container">
      <div className="question-form">
        <div className="form-header">
          <button onClick={onBackToDashboard} className="back-btn">
            ← Back to Dashboard
          </button>
        </div>
        <h1>AI Question Generator</h1>
        <p>Generate quiz questions on any topic using AI</p>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="topic">Topic:</label>
            <input
              type="text"
              id="topic"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="Enter a topic (e.g., History, Chemistry, Math)"
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="numberQuestions">Number of Questions:</label>
            <input
              type="number"
              id="numberQuestions"
              value={numberQuestions}
              onChange={(e) => setNumberQuestions(parseInt(e.target.value))}
              min="1"
              max="20"
              disabled={loading}
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button type="submit" disabled={loading} className="generate-btn">
            {loading ? 'Generating Questions...' : 'Generate Questions'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default QuestionForm;