import { useState, useEffect } from 'react';
import './Sidebar.css';

export default function Sidebar({
  conversations,
  currentConversationId,
  onSelectConversation,
  onNewConversation,
  theme,
  onThemeToggle,
  currentView,
  onViewChange,
}) {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <div className="header-top">
          <h1>LLM Council</h1>
          <button className="theme-toggle-btn" onClick={onThemeToggle} title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}>
            {theme === 'light' ? '🌙' : '☀️'}
          </button>
        </div>
        <button className="new-conversation-btn" onClick={onNewConversation}>
          + New Conversation
        </button>
        
        <div className="view-tabs">
          <button 
            className={`view-tab ${currentView === 'chat' ? 'active' : ''}`}
            onClick={() => onViewChange('chat')}
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
            </svg>
            Conversations
          </button>
          <button 
            className={`view-tab ${currentView === 'statistics' ? 'active' : ''}`}
            onClick={() => onViewChange('statistics')}
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="12" y1="20" x2="12" y2="10"></line>
              <line x1="18" y1="20" x2="18" y2="4"></line>
              <line x1="6" y1="20" x2="6" y2="16"></line>
            </svg>
            Statistics
          </button>
        </div>
      </div>

      <div className="conversation-list">{currentView === 'chat' && (
        <>
          {conversations.length === 0 ? (
            <div className="no-conversations">No conversations yet</div>
          ) : (
            conversations.map((conv) => (
              <div
                key={conv.id}
                className={`conversation-item ${
                  conv.id === currentConversationId ? 'active' : ''
                }`}
                onClick={() => onSelectConversation(conv.id)}
              >
                <div className="conversation-title">
                  {conv.title || 'New Conversation'}
                </div>
                <div className="conversation-meta">
                  {conv.message_count} messages
                </div>
              </div>
            ))
          )}
        </>
      )}
      </div>
    </div>
  );
}
