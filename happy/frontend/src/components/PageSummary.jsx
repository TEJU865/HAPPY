import React from 'react';
import './PageSummary.css';

const PageSummary = ({ summary, loading, onSave }) => {
  if (loading) {
    return <div className="summary-loading">Loading summary...</div>;
  }

  if (!summary || !summary.success) {
    return (
      <div className="summary-empty">
        <p>No summary available</p>
      </div>
    );
  }

  return (
    <div className="page-summary">
      <div className="summary-header">
        <h3 className="summary-title">{summary.title}</h3>
        <a href={summary.url} target="_blank" rel="noopener noreferrer" className="summary-link">
          {summary.url.replace(/^https?:\/\//, '').split('/')[0]}
        </a>
      </div>

      <div className="summary-content">
        <div className="summary-text">{summary.summary}</div>

        {summary.key_points && summary.key_points.length > 0 && (
          <div className="key-points">
            <h4>Key Points:</h4>
            <ul>
              {summary.key_points.map((point, index) => (
                <li key={index}>{point}</li>
              ))}
            </ul>
          </div>
        )}

        <div className="summary-meta">
          <span>{summary.word_count} words</span>
          <span>{summary.length} summary</span>
        </div>
      </div>

      <button className="summary-save-btn" onClick={onSave}>
        Save to Memory
      </button>
    </div>
  );
};

export default PageSummary;
