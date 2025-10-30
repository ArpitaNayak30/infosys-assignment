import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  ResponsiveContainer
} from 'recharts';
import './Dashboard.css';

const Dashboard = ({ onNavigateToQuiz }) => {
  const [stats, setStats] = useState(null);
  const [recentQuizzes, setRecentQuizzes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const { token } = useAuth();

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError('');
      
      console.log('Fetching dashboard data with token:', token ? 'Token exists' : 'No token');
      
      if (!token) {
        throw new Error('No authentication token available');
      }
      
      const response = await fetch('http://127.0.0.1:8000/api/quiz/recent', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      console.log('Response status:', response.status);
      
      if (response.status === 401) {
        throw new Error('Authentication failed. Please login again.');
      }
      
      if (!response.ok) {
        const errorText = await response.text();
        console.log('Error response:', errorText);
        throw new Error(`HTTP ${response.status}: ${errorText}`);
      }

      const data = await response.json();
      console.log('Dashboard data received:', data);
      
      setStats(data.stats);
      setRecentQuizzes(data.quizzes);
    } catch (err) {
      console.error('Dashboard fetch error:', err);
      
      if (err.message.includes('Authentication failed')) {
        setError('Please logout and login again to refresh your session.');
      } else {
        setError(err.message);
      }
      
      // Set default empty stats if API fails
      setStats({
        total_quizzes: 0,
        completed_quizzes: 0,
        incomplete_quizzes: 0,
        average_score: 0,
        highest_score: 0,
        lowest_score: 0,
        average_percentage: 0
      });
      setRecentQuizzes([]);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusColor = (status) => {
    return status === 'completed' ? '#28a745' : '#ffc107';
  };

  const getScoreColor = (percentage) => {
    if (percentage >= 80) return '#28a745';
    if (percentage >= 60) return '#ffc107';
    return '#dc3545';
  };

  // Prepare chart data
  const pieData = stats ? [
    { name: 'Completed', value: stats.completed_quizzes, color: '#28a745' },
    { name: 'Incomplete', value: stats.incomplete_quizzes, color: '#ffc107' }
  ] : [];

  const recentScoresData = recentQuizzes
    .filter(quiz => quiz.status === 'completed')
    .slice(0, 7)
    .reverse()
    .map((quiz, index) => ({
      name: `Quiz ${index + 1}`,
      score: quiz.score,
      percentage: quiz.percentage,
      topic: quiz.topic
    }));

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="loading-spinner"></div>
        <p>Loading dashboard...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-error">
        <p>Error loading dashboard: {error}</p>
        <button onClick={fetchDashboardData} className="retry-btn">
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        <button onClick={onNavigateToQuiz} className="new-quiz-btn">
          Generate New Quiz
        </button>
      </div>

      {/* Stats Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">📊</div>
          <div className="stat-content">
            <h3>{stats?.total_quizzes || 0}</h3>
            <p>Total Quizzes</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">✅</div>
          <div className="stat-content">
            <h3>{stats?.completed_quizzes || 0}</h3>
            <p>Completed</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">⏳</div>
          <div className="stat-content">
            <h3>{stats?.incomplete_quizzes || 0}</h3>
            <p>Incomplete</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">📈</div>
          <div className="stat-content">
            <h3>{stats?.average_percentage?.toFixed(1) || 0}%</h3>
            <p>Average Score</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">🏆</div>
          <div className="stat-content">
            <h3>{stats?.highest_score || 0}</h3>
            <p>Highest Score</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">📉</div>
          <div className="stat-content">
            <h3>{stats?.lowest_score || 0}</h3>
            <p>Lowest Score</p>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="charts-section">
        <div className="chart-container">
          <h3>Quiz Completion Status</h3>
          {pieData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value}`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div className="no-data">No quiz data available</div>
          )}
        </div>

        <div className="chart-container">
          <h3>Recent Quiz Performance</h3>
          {recentScoresData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={recentScoresData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip 
                  formatter={(value, name) => [
                    name === 'percentage' ? `${value}%` : value,
                    name === 'percentage' ? 'Percentage' : 'Score'
                  ]}
                  labelFormatter={(label) => {
                    const quiz = recentScoresData.find(q => q.name === label);
                    return quiz ? `${label} - ${quiz.topic}` : label;
                  }}
                />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="percentage" 
                  stroke="#8884d8" 
                  strokeWidth={2}
                  dot={{ fill: '#8884d8' }}
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="no-data">No completed quizzes yet</div>
          )}
        </div>
      </div>

      {/* Recent Quizzes Table */}
      <div className="recent-quizzes">
        <h3>Recent Quiz Attempts</h3>
        {recentQuizzes.length > 0 ? (
          <div className="quiz-table">
            <div className="table-header">
              <div>Topic</div>
              <div>Questions</div>
              <div>Score</div>
              <div>Percentage</div>
              <div>Status</div>
              <div>Date</div>
            </div>
            {recentQuizzes.map((quiz) => (
              <div key={quiz.id} className="table-row">
                <div className="quiz-topic">{quiz.topic}</div>
                <div>{quiz.total_questions}</div>
                <div>
                  {quiz.status === 'completed' ? (
                    <span className="score">{quiz.score}/{quiz.total_questions}</span>
                  ) : (
                    <span className="incomplete">-</span>
                  )}
                </div>
                <div>
                  {quiz.status === 'completed' ? (
                    <span 
                      className="percentage"
                      style={{ color: getScoreColor(quiz.percentage) }}
                    >
                      {quiz.percentage?.toFixed(1)}%
                    </span>
                  ) : (
                    <span className="incomplete">-</span>
                  )}
                </div>
                <div>
                  <span 
                    className="status"
                    style={{ color: getStatusColor(quiz.status) }}
                  >
                    {quiz.status}
                  </span>
                </div>
                <div className="quiz-date">
                  {formatDate(quiz.created_at)}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="no-quizzes">
            <p>No quiz attempts yet. Start your first quiz!</p>
            <button onClick={onNavigateToQuiz} className="start-quiz-btn">
              Generate Your First Quiz
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;