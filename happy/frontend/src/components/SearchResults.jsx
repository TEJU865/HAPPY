import React from 'react';
import './SearchResults.css';

const SearchResults = ({ results, loading, onResultClick }) => {
  if (loading) {
    return <div className="search-loading">Searching...</div>;
  }

  if (!results || results.length === 0) {
    return (
      <div className="search-empty">
        <p>No results found. Try a different search.</p>
      </div>
    );
  }

  return (
    <div className="search-results">
      <div className="results-count">
        Found {results.length} results
      </div>
      {results.map((result, index) => (
        <div
          key={index}
          className="search-result-card"
          onClick={() => onResultClick(result)}
        >
          <div className="result-position">#{result.position}</div>
          <div className="result-title">{result.title}</div>
          <div className="result-url">{result.url}</div>
          <div className="result-snippet">{result.snippet}</div>
          <button className="result-open-btn">Open</button>
        </div>
      ))}
    </div>
  );
};

export default SearchResults;
