"""Browser Memory - Stores browser history, queries, and summaries"""

import logging
import sqlite3
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class BrowserMemory:
    """Manages browser history and web search/page memory"""

    def __init__(self, db_path: str = "happy.db"):
        self.db_path = db_path
        self._ensure_tables()

    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_tables(self):
        """Ensure required tables exist"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Web history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS web_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT,
                    url TEXT,
                    title TEXT,
                    summary TEXT,
                    source_engine TEXT,
                    created_at TEXT
                )
            ''')
            
            # Browser actions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS browser_actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action_type TEXT,
                    url TEXT,
                    details TEXT,
                    success INTEGER,
                    created_at TEXT
                )
            ''')
            
            # Create indices for faster queries
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_web_history_url 
                ON web_history(url)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_web_history_query 
                ON web_history(query)
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error ensuring tables: {e}")

    def save_query(self, query: str, source_engine: str = "search") -> Dict[str, Any]:
        """Save a search query"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO web_history (query, source_engine, created_at)
                VALUES (?, ?, ?)
            ''', (query, source_engine, datetime.now().isoformat()))
            
            conn.commit()
            query_id = cursor.lastrowid
            conn.close()
            
            return {
                "success": True,
                "id": query_id,
                "message": f"Query saved: {query}"
            }
            
        except Exception as e:
            logger.error(f"Error saving query: {e}")
            return {
                "success": False,
                "message": f"Error saving query: {str(e)}"
            }

    def save_link(
        self,
        url: str,
        title: str = "",
        query: Optional[str] = None
    ) -> Dict[str, Any]:
        """Save a visited link"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Check if URL already exists
            cursor.execute(
                'SELECT id FROM web_history WHERE url = ?',
                (url,)
            )
            existing = cursor.fetchone()
            
            if existing:
                # Update existing record
                cursor.execute('''
                    UPDATE web_history SET title = ? WHERE id = ?
                ''', (title, existing['id']))
            else:
                # Create new record
                cursor.execute('''
                    INSERT INTO web_history (url, title, query, created_at)
                    VALUES (?, ?, ?, ?)
                ''', (url, title, query, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "url": url,
                "message": f"Link saved: {title or url}"
            }
            
        except Exception as e:
            logger.error(f"Error saving link: {e}")
            return {
                "success": False,
                "message": f"Error saving link: {str(e)}"
            }

    def save_summary(
        self,
        url: str,
        summary: str,
        title: str = ""
    ) -> Dict[str, Any]:
        """Save a page summary"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Check if URL exists
            cursor.execute(
                'SELECT id FROM web_history WHERE url = ?',
                (url,)
            )
            existing = cursor.fetchone()
            
            if existing:
                # Update with summary
                cursor.execute('''
                    UPDATE web_history 
                    SET summary = ?, title = ? 
                    WHERE id = ?
                ''', (summary, title, existing['id']))
            else:
                # Create new record with summary
                cursor.execute('''
                    INSERT INTO web_history (url, title, summary, created_at)
                    VALUES (?, ?, ?, ?)
                ''', (url, title, summary, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "url": url,
                "message": "Summary saved"
            }
            
        except Exception as e:
            logger.error(f"Error saving summary: {e}")
            return {
                "success": False,
                "message": f"Error saving summary: {str(e)}"
            }

    def save_action(
        self,
        action_type: str,
        url: str = "",
        details: str = "",
        success: bool = True
    ) -> Dict[str, Any]:
        """Save a browser action"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO browser_actions 
                (action_type, url, details, success, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                action_type,
                url,
                details,
                1 if success else 0,
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "message": f"Action logged: {action_type}"
            }
            
        except Exception as e:
            logger.error(f"Error saving action: {e}")
            return {
                "success": False,
                "message": f"Error saving action: {str(e)}"
            }

    def get_history(self, limit: int = 50, query: Optional[str] = None) -> Dict[str, Any]:
        """Get browser history"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if query:
                # Search for specific query
                cursor.execute('''
                    SELECT * FROM web_history 
                    WHERE query LIKE ? OR url LIKE ? OR title LIKE ?
                    ORDER BY created_at DESC
                    LIMIT ?
                ''', (f"%{query}%", f"%{query}%", f"%{query}%", limit))
            else:
                # Get all history
                cursor.execute('''
                    SELECT * FROM web_history 
                    ORDER BY created_at DESC
                    LIMIT ?
                ''', (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            history = []
            for row in rows:
                history.append({
                    "id": row['id'],
                    "query": row['query'],
                    "url": row['url'],
                    "title": row['title'],
                    "summary": row['summary'],
                    "created_at": row['created_at']
                })
            
            return {
                "success": True,
                "history": history,
                "count": len(history)
            }
            
        except Exception as e:
            logger.error(f"Error getting history: {e}")
            return {
                "success": False,
                "history": [],
                "message": f"Error retrieving history: {str(e)}"
            }

    def get_recent_queries(self, limit: int = 20) -> List[str]:
        """Get recent search queries"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT DISTINCT query FROM web_history 
                WHERE query IS NOT NULL
                ORDER BY created_at DESC
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [row['query'] for row in rows if row['query']]
            
        except Exception as e:
            logger.error(f"Error getting queries: {e}")
            return []

    def get_saved_links(self, limit: int = 30) -> List[Dict[str, Any]]:
        """Get saved links with summaries"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT url, title, summary, created_at 
                FROM web_history 
                WHERE url IS NOT NULL
                ORDER BY created_at DESC
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            links = []
            for row in rows:
                links.append({
                    "url": row['url'],
                    "title": row['title'] or row['url'],
                    "summary": row['summary'],
                    "saved_at": row['created_at']
                })
            
            return links
            
        except Exception as e:
            logger.error(f"Error getting saved links: {e}")
            return []

    def clear_history(self, older_than_days: Optional[int] = None) -> Dict[str, Any]:
        """Clear browser history"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if older_than_days:
                # Only delete old entries
                from datetime import timedelta
                cutoff_date = (
                    datetime.now() - timedelta(days=older_than_days)
                ).isoformat()
                
                cursor.execute(
                    'DELETE FROM web_history WHERE created_at < ?',
                    (cutoff_date,)
                )
            else:
                # Clear all
                cursor.execute('DELETE FROM web_history')
            
            deleted = cursor.rowcount
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "deleted": deleted,
                "message": f"Deleted {deleted} history entries"
            }
            
        except Exception as e:
            logger.error(f"Error clearing history: {e}")
            return {
                "success": False,
                "message": f"Error clearing history: {str(e)}"
            }

    def search_history(self, term: str) -> List[Dict[str, Any]]:
        """Search through history"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM web_history 
                WHERE query LIKE ? OR title LIKE ? OR summary LIKE ?
                ORDER BY created_at DESC
                LIMIT 30
            ''', (f"%{term}%", f"%{term}%", f"%{term}%"))
            
            rows = cursor.fetchall()
            conn.close()
            
            results = []
            for row in rows:
                results.append({
                    "id": row['id'],
                    "query": row['query'],
                    "url": row['url'],
                    "title": row['title'],
                    "summary": row['summary'],
                    "created_at": row['created_at']
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching history: {e}")
            return []
