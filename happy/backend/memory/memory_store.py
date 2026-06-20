"""
HAPPY Memory Store
Handles saving and reading user memories using SQLite
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

class MemoryStore:
    def __init__(self, db_path: str = "happy_memory.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create memories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create command history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS command_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT NOT NULL,
                success BOOLEAN,
                result TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def remember(self, key: str, value: str, category: str = "general") -> bool:
        """Save a memory"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO memories (key, value, category, updated_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ''', (key, value, category))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving memory: {e}")
            return False
    
    def recall(self, key: str) -> str | None:
        """Retrieve a memory"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT value FROM memories WHERE key = ?', (key,))
            result = cursor.fetchone()
            conn.close()
            
            return result[0] if result else None
        except Exception as e:
            print(f"Error recalling memory: {e}")
            return None
    
    def recall_all(self) -> dict:
        """Get all memories"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT key, value FROM memories')
            results = cursor.fetchall()
            conn.close()
            
            return {key: value for key, value in results}
        except Exception as e:
            print(f"Error recalling all memories: {e}")
            return {}
    
    def log_command(self, command: str, success: bool, result: str = "") -> bool:
        """Log a command execution"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO command_history (command, success, result)
                VALUES (?, ?, ?)
            ''', (command, success, result))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error logging command: {e}")
            return False
