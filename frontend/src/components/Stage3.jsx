import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { getModelColorClass } from '../utils/modelColors';
import './Stage3.css';

export default function Stage3({ finalResponse }) {
  const [isExpanded, setIsExpanded] = useState(true);

  if (!finalResponse) {
    return null;
  }

  const modelName = finalResponse.model ? (finalResponse.model.split('/')[1] || finalResponse.model) : 'Unknown';

  return (
    <div className={`stage stage3 ${getModelColorClass(finalResponse.model || '')}`}>
      <button
        className="stage-header"
        onClick={() => setIsExpanded(!isExpanded)}
        aria-expanded={isExpanded}
        aria-label="Toggle stage visibility"
      >
        <span className="toggle-icon">{isExpanded ? '▼' : '▶'}</span>
        <h3 className="stage-title">Stage 3: Final Council Answer</h3>
      </button>
      
      {isExpanded && (
        <div className={`final-response ${getModelColorClass(finalResponse.model || '')}`}>
          <div className="chairman-label">
            Chairman: {modelName}
          </div>
          <div className="final-text markdown-content">
            <ReactMarkdown>{finalResponse.response || ''}</ReactMarkdown>
          </div>
        </div>
      )}
    </div>
  );
}
