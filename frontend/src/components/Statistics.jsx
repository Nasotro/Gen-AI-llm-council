import { useState, useEffect } from 'react';
import { api } from '../api';
import { getModelColor } from '../utils/modelColors';
import './Statistics.css';

export default function Statistics() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedStage, setSelectedStage] = useState(null);

  useEffect(() => {
    loadStatistics();
  }, []);

  const loadStatistics = async () => {
    try {
      setLoading(true);
      const data = await api.getStatistics();
      setStats(data);
      setError(null);
    } catch (err) {
      setError('Failed to load statistics. Please try again.');
      console.error('Error loading statistics:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (seconds) => {
    if (seconds < 1) return `${Math.round(seconds * 1000)}ms`;
    return `${seconds.toFixed(2)}s`;
  };

  const getStageInfo = (stageName) => {
    const stageData = stats?.timing_stats?.[stageName];
    if (!stageData) return null;

    const stageLabels = {
      stage1: 'Stage 1: Individual Responses',
      stage2: 'Stage 2: Peer Rankings',
      stage3: 'Stage 3: Final Synthesis',
      total: 'Total Processing Time'
    };

    return {
      label: stageLabels[stageName] || stageName,
      ...stageData
    };
  };

  const getPercentage = (value, max) => {
    return (value / max) * 100;
  };

  if (loading) {
    return (
      <div className="statistics-container">
        <div className="statistics-loading">
          <div className="spinner"></div>
          <p>Loading statistics...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="statistics-container">
        <div className="statistics-error">
          <p>{error}</p>
          <button onClick={loadStatistics} className="retry-button">Retry</button>
        </div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="statistics-container">
        <div className="statistics-empty">
          <p>No statistics available yet. Start a conversation to see statistics!</p>
        </div>
      </div>
    );
  }

  // Get max time for scaling the bars
  const maxTime = Math.max(
    stats.timing_stats?.stage1?.max || 0,
    stats.timing_stats?.stage2?.max || 0,
    stats.timing_stats?.stage3?.max || 0
  );

  return (
    <div className="statistics-container">
      <div className="statistics-header">
        <h1>Performance Statistics</h1>
        <button onClick={loadStatistics} className="refresh-button" title="Refresh statistics">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M1 4v6h6M23 20v-6h-6M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"></path>
          </svg>
        </button>
      </div>

      <div className="statistics-summary">
        <div className="stat-card">
          <div className="stat-value">{stats.total_conversations}</div>
          <div className="stat-label">Total Conversations</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{stats.total_messages}</div>
          <div className="stat-label">Messages Processed</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">
            {stats.timing_stats?.total?.avg ? formatTime(stats.timing_stats.total.avg) : 'N/A'}
          </div>
          <div className="stat-label">Avg Processing Time</div>
        </div>
      </div>

      <div className="statistics-section">
        <h2>Stage Processing Times</h2>
        <p className="section-description">
          Click on a bar for detailed information
        </p>
        
        <div className="timing-bars">
          {['stage1', 'stage2', 'stage3'].map((stageName) => {
            const stageInfo = getStageInfo(stageName);
            if (!stageInfo || stageInfo.count === 0) return null;

            const isSelected = selectedStage === stageName;

            return (
              <div 
                key={stageName} 
                className={`timing-bar-container ${isSelected ? 'selected' : ''}`}
                onClick={() => setSelectedStage(selectedStage === stageName ? null : stageName)}
              >
                <div className="timing-bar-header">
                  <span className="timing-bar-label">{stageInfo.label}</span>
                  <span className="timing-bar-avg">{formatTime(stageInfo.avg)}</span>
                </div>
                
                <div className="timing-bar-wrapper">
                  <div 
                    className="timing-bar"
                    style={{ 
                      width: `${getPercentage(stageInfo.avg, maxTime)}%`,
                      backgroundColor: `hsl(${210 + (stageName === 'stage1' ? 0 : stageName === 'stage2' ? 30 : 60)}, 70%, 50%)`
                    }}
                  >
                  </div>
                </div>

                {isSelected && (
                  <div className="timing-details">
                    <h4>Detailed Statistics</h4>
                    <div className="details-grid">
                      <div className="detail-item">
                        <label>Fastest Time:</label>
                        <span>{formatTime(stageInfo.min)}</span>
                      </div>
                      <div className="detail-item">
                        <label>Slowest Time:</label>
                        <span>{formatTime(stageInfo.max)}</span>
                      </div>
                      <div className="detail-item">
                        <label>Range:</label>
                        <span>{formatTime(stageInfo.max - stageInfo.min)}</span>
                      </div>
                      <div className="detail-item">
                        <label>Total Samples:</label>
                        <span>{stageInfo.count}</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {stats.model_stats && stats.model_stats.length > 0 && (
        <div className="statistics-section">
          <h2>Model Performance</h2>
          <div className="model-stats-grid">
            {stats.model_stats.map((model) => (
              <div 
                key={model.name} 
                className="model-stat-card"
                style={{ borderLeftColor: getModelColor(model.name) }}
              >
                <h3 className="model-name">{model.name}</h3>
                <div className="model-metrics">
                  <div className="metric">
                    <span className="metric-label">Responses:</span>
                    <span className="metric-value">{model.response_count}</span>
                  </div>
                  <div className="metric">
                    <span className="metric-label">Avg Length:</span>
                    <span className="metric-value">{model.avg_response_length || 0} chars</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="statistics-section">
        <h2>Total Processing Overview</h2>
        {stats.timing_stats?.total && (
          <div className="overview-card">
            <div className="overview-metric">
              <span className="overview-label">Average Total Time:</span>
              <span className="overview-value highlight">
                {formatTime(stats.timing_stats.total.avg)}
              </span>
            </div>
            <div className="overview-breakdown">
              <div className="breakdown-item">
                <span className="breakdown-label">Fastest:</span>
                <span className="breakdown-value">{formatTime(stats.timing_stats.total.min)}</span>
              </div>
              <div className="breakdown-item">
                <span className="breakdown-label">Slowest:</span>
                <span className="breakdown-value">{formatTime(stats.timing_stats.total.max)}</span>
              </div>
              <div className="breakdown-item">
                <span className="breakdown-label">Consistency:</span>
                <span className="breakdown-value">
                  ±{formatTime((stats.timing_stats.total.max - stats.timing_stats.total.min) / 2)}
                </span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
