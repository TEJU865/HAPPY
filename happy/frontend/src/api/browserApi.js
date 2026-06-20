/**
 * Browser API - Frontend API client for browser operations
 */

import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const browserApi = {
  startBrowser: () =>
    axios.post(`${API_BASE_URL}/browser/start`)
      .then(res => res.data)
      .catch(err => ({ success: false, message: err.message })),

  stopBrowser: () =>
    axios.post(`${API_BASE_URL}/browser/stop`)
      .then(res => res.data)
      .catch(err => ({ success: false, message: err.message })),

  openUrl: (url) =>
    axios.post(`${API_BASE_URL}/browser/open`, null, { params: { url } })
      .then(res => res.data)
      .catch(err => ({ success: false, message: err.message })),

  search: (query) =>
    axios.post(`${API_BASE_URL}/browser/search`, null, { params: { query } })
      .then(res => res.data)
      .catch(err => ({ success: false, query, results: [], message: err.message })),

  readPage: () =>
    axios.post(`${API_BASE_URL}/browser/read`)
      .then(res => res.data)
      .catch(err => ({ success: false, message: err.message })),

  summarizePage: (length = 'medium') =>
    axios.post(`${API_BASE_URL}/browser/summarize`, null, { params: { length } })
      .then(res => res.data)
      .catch(err => ({ success: false, message: err.message })),

  click: (linkText = '', url = '') =>
    axios.post(`${API_BASE_URL}/browser/click`, null, { params: { link_text: linkText, url } })
      .then(res => res.data)
      .catch(err => ({ success: false, message: err.message })),

  getTabs: () =>
    axios.get(`${API_BASE_URL}/browser/tabs`)
      .then(res => res.data)
      .catch(err => ({ success: false, tabs: [], message: err.message })),

  switchTab: (tabId) =>
    axios.post(`${API_BASE_URL}/browser/tab/switch`, null, { params: { tab_id: tabId } })
      .then(res => res.data)
      .catch(err => ({ success: false, message: err.message })),

  closeTab: (tabId) =>
    axios.post(`${API_BASE_URL}/browser/tab/close`, null, { params: { tab_id: tabId } })
      .then(res => res.data)
      .catch(err => ({ success: false, message: err.message })),

  getHistory: (limit = 50, searchTerm = null) => {
    const params = { limit };
    if (searchTerm) params.search_term = searchTerm;
    return axios.get(`${API_BASE_URL}/browser/history`, { params })
      .then(res => res.data)
      .catch(err => ({ success: false, history: [], message: err.message }));
  },

  planWorkflow: (command) =>
    axios.post(`${API_BASE_URL}/browser/workflow`, null, { params: { command } })
      .then(res => res.data)
      .catch(err => ({ success: false, workflow: [], message: err.message }))
};

export default browserApi;

