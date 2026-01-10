import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { getModelColorClass } from '../utils/modelColors';
import './Stage1.css';

export default function Stage1({ responses }) {
  const [activeTab, setActiveTab] = useState(0);
  const [isExpanded, setIsExpanded] = useState(true);

  if (!responses || responses.length === 0) {
    return null;
  }

  return (
    <div className="stage stage1">
      <button
        className="stage-header"
        onClick={() => setIsExpanded(!isExpanded)}
        aria-expanded={isExpanded}
        aria-label="Toggle stage visibility"
      >
        <span className="toggle-icon">{isExpanded ? '▼' : '▶'}</span>
        <h3 className="stage-title">Stage 1: Individual Responses</h3>
      </button>

      {isExpanded && (
        <>
          <div className="tabs">
            {responses.map((resp, index) => (
              <button
                key={index}
                className={`tab ${activeTab === index ? 'active' : ''} ${getModelColorClass(resp.model)}`}
                onClick={() => setActiveTab(index)}
              >
                {resp.model.split('/')[1] || resp.model}
              </button>
            ))}
          </div>

          <div className={`tab-content ${getModelColorClass(responses[activeTab].model)}`}>
            <div className="model-name">{responses[activeTab].model}</div>
            <div className="response-text markdown-content">
              <ReactMarkdown>{responses[activeTab].response}</ReactMarkdown>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
