import React, { useState } from 'react';
import browserApi from '../api/browserApi';
import SearchResults from './SearchResults';
import PageSummary from './PageSummary';
import './BrowserPage.css';

const BrowserPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [currentPage, setCurrentPage] = useState(null);
  const [pageSummary, setPageSummary] = useState(null);
  const [tabs, setTabs] = useState([]);
  const [activeTab, setActiveTab] = useState(0);
  const [loading, setLoading] = useState(false);
  const [summaryLoading, setSummaryLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setLoading(true);
    const result = await browserApi.search(searchQuery);
    setSearchResults(result.results || []);
    setLoading(false);
  };

  const handleResultClick = async (result) => {
    setLoading(true);
    const opened = await browserApi.openUrl(result.url);
    if (opened.success) {
      setCurrentPage(result);
      await loadPageContent();
    }
    setLoading(false);
  };

  const loadPageContent = async () => {
    const pageContent = await browserApi.readPage();
    if (pageContent.success) {
      setCurrentPage(pageContent);
    }
  };

  const handleSummarize = async (length = 'medium') => {
    setSummaryLoading(true);
    const summary = await browserApi.summarizePage(length);
    setPageSummary(summary);
    setSummaryLoading(false);
  };

  const handleSaveToMemory = async () => {
    if (pageSummary && pageSummary.success) {
      // Trigger save to memory
      console.log('Saving to memory:', pageSummary);
    }
  };

  const handleRefreshTabs = async () => {
    const tabsData = await browserApi.getTabs();
    setTabs(tabsData.tabs || []);
  };

  return (
    <div className="browser-page">
      {/* Browser Tabs */}
      <div className="browser-tabs">
        <button className="tab-button active" onClick={handleRefreshTabs}>
          🔄 Refresh Tabs
        </button>
        {tabs.map((tab) => (
          <div
            key={tab.id}
            className={`tab ${tab.is_current ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            <span className="tab-title">{tab.title}</span>
            <button className="tab-close">✕</button>
          </div>
        ))}
      </div>

      {/* Search Bar */}
      <div className="browser-search-section">
        <form onSubmit={handleSearch} className="search-form">
          <input
            type="text"
            className="search-input"
            placeholder="Search the web..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <button type="submit" className="search-button">
            Search
          </button>
        </form>
      </div>

      {/* Main Content Area */}
      <div className="browser-content">
        {searchResults.length > 0 && !currentPage && (
          <SearchResults
            results={searchResults}
            loading={loading}
            onResultClick={handleResultClick}
          />
        )}

        {currentPage && (
          <div className="current-page-view">
            <div className="page-toolbar">
              <h3 className="page-title">{currentPage.title}</h3>
              <div className="page-buttons">
                <button
                  className="page-action-btn"
                  onClick={() => handleSummarize('medium')}
                >
                  📝 Summarize
                </button>
                <button className="page-action-btn">
                  💾 Save
                </button>
              </div>
            </div>

            {pageSummary && pageSummary.success ? (
              <PageSummary
                summary={pageSummary}
                loading={summaryLoading}
                onSave={handleSaveToMemory}
              />
            ) : (
              <div className="page-text-content">
                {currentPage.text && (
                  <p>{currentPage.text.substring(0, 500)}...</p>
                )}
              </div>
            )}
          </div>
        )}

        {!searchResults.length && !currentPage && (
          <div className="browser-welcome">
            <h2>HAPPY Browser</h2>
            <p>Search the web and get instant summaries</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default BrowserPage;
