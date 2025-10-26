import React, { useState } from 'react';
import './Quiz.css';

const Quiz = ({ questions, topic, onBackToForm }) => {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);
  const [score, setScore] = useState(0);

  const handleAnswerSelect = (questionIndex, selectedOption) => {
    setSelectedAnswers({
      ...selectedAnswers,
      [questionIndex]: selectedOption
    });
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      calculateResults();
    }
  };

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const calculateResults = () => {
    let correctAnswers = 0;
    questions.forEach((question, index) => {
      // For demo purposes, we'll assume option C is correct
      // In a real scenario, the API should provide the correct answer
      const correctOption = question.options[2]; // Assuming C is correct
      if (selectedAnswers[index] === correctOption) {
        correctAnswers++;
      }
    });
    setScore(correctAnswers);
    setShowResults(true);
  };

  const resetQuiz = () => {
    setCurrentQuestion(0);
    setSelectedAnswers({});
    setShowResults(false);
    setScore(0);
  };

  const getScoreColor = () => {
    const percentage = (score / questions.length) * 100;
    if (percentage >= 80) return '#28a745';
    if (percentage >= 60) return '#ffc107';
    return '#dc3545';
  };

  if (showResults) {
    return (
      <div className="quiz-container">
        <div className="results-card">
          <h2>Quiz Results</h2>
          <div className="score-display">
            <div className="score-circle" style={{ borderColor: getScoreColor() }}>
              <span className="score-text" style={{ color: getScoreColor() }}>
                {score}/{questions.length}
              </span>
            </div>
            <p className="score-percentage" style={{ color: getScoreColor() }}>
              {Math.round((score / questions.length) * 100)}%
            </p>
          </div>
          
          <div className="results-summary">
            <h3>Topic: {topic}</h3>
            <p>You answered {score} out of {questions.length} questions correctly!</p>
            
            {score === questions.length && (
              <p className="perfect-score">🎉 Perfect Score! Excellent work!</p>
            )}
            {score >= questions.length * 0.8 && score < questions.length && (
              <p className="good-score">👏 Great job! You did very well!</p>
            )}
            {score >= questions.length * 0.6 && score < questions.length * 0.8 && (
              <p className="average-score">👍 Good effort! Keep practicing!</p>
            )}
            {score < questions.length * 0.6 && (
              <p className="low-score">📚 Keep studying! You'll do better next time!</p>
            )}
          </div>

          <div className="results-actions">
            <button onClick={resetQuiz} className="retry-btn">
              Retake Quiz
            </button>
            <button onClick={onBackToForm} className="new-quiz-btn">
              Generate New Quiz
            </button>
          </div>
        </div>
      </div>
    );
  }

  const question = questions[currentQuestion];
  const progress = ((currentQuestion + 1) / questions.length) * 100;

  return (
    <div className="quiz-container">
      <div className="quiz-card">
        <div className="quiz-header">
          <h2>Quiz: {topic}</h2>
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <p className="question-counter">
            Question {currentQuestion + 1} of {questions.length}
          </p>
        </div>

        <div className="question-section">
          <h3 className="question-text">{question.question}</h3>
          
          <div className="options-list">
            {question.options.map((option, index) => (
              <label key={index} className="option-item">
                <input
                  type="radio"
                  name={`question-${currentQuestion}`}
                  value={option}
                  checked={selectedAnswers[currentQuestion] === option}
                  onChange={() => handleAnswerSelect(currentQuestion, option)}
                />
                <span className="option-text">{option}</span>
              </label>
            ))}
          </div>
        </div>

        <div className="quiz-navigation">
          <button 
            onClick={handlePrevious} 
            disabled={currentQuestion === 0}
            className="nav-btn prev-btn"
          >
            Previous
          </button>
          
          <button 
            onClick={handleNext}
            disabled={!selectedAnswers[currentQuestion]}
            className="nav-btn next-btn"
          >
            {currentQuestion === questions.length - 1 ? 'Finish Quiz' : 'Next'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Quiz;