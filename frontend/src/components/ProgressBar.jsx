import './ProgressBar.css';

export default function ProgressBar({ currentStage, loading, timings }) {
  const stages = [
    { id: 1, name: 'Individual Responses', key: 'stage1' },
    { id: 2, name: 'Peer Rankings', key: 'stage2' },
    { id: 3, name: 'Final Answer', key: 'stage3' },
  ];

  const formatTime = (seconds) => {
    if (!seconds) return null;
    if (seconds < 1) return `${Math.round(seconds * 1000)}ms`;
    return `${seconds.toFixed(2)}s`;
  };

  // Determine the current stage index based on what's completed or loading
  const getCurrentStageIndex = () => {
    if (loading?.stage3 || currentStage?.stage3) return 2;
    if (loading?.stage2 || currentStage?.stage2) return 1;
    if (loading?.stage1 || currentStage?.stage1) return 0;
    return -1;
  };

  const getStageStatus = (stageKey, index) => {
    const currentIndex = getCurrentStageIndex();
    
    if (currentStage?.[stageKey]) return 'completed';
    if (loading?.[stageKey]) return 'active';
    if (index < currentIndex) return 'completed';
    if (index === currentIndex) return 'active';
    return 'pending';
  };

  const activeIndex = getCurrentStageIndex();

  return (
    <div className="progress-bar-container">
      <div className="progress-bar">
        {stages.map((stage, index) => {
          const status = getStageStatus(stage.key, index);
          const isActive = index === activeIndex;
          const isCompleted = status === 'completed';
          const isLast = index === stages.length - 1;

          const stageTimings = timings?.[stage.key];
          const hasTiming = stageTimings && typeof stageTimings === 'number';

          return (
            <div key={stage.id} className="progress-stage-wrapper">
              <div className={`progress-stage ${status}`}>
                <div className={`stage-circle ${status} ${hasTiming ? 'has-timing' : ''}`}>
                  {isCompleted ? (
                    <svg className="checkmark" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3">
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                  ) : isActive && loading?.[stage.key] ? (
                    <div className="stage-spinner"></div>
                  ) : (
                    <span className="stage-number">{stage.id}</span>
                  )}
                </div>
                {hasTiming && (
                  <div className="stage-tooltip">
                    <div className="tooltip-content">
                      <div className="tooltip-header">Processing Time</div>
                      <div className="tooltip-time">{formatTime(stageTimings)}</div>
                    </div>
                  </div>
                )}
                <div className="stage-label">{stage.name}</div>
              </div>
              {!isLast && (
                <div className={`progress-connector ${isCompleted ? 'completed' : ''}`}></div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
