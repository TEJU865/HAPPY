"""
Advanced Memory Store for HAPPY
Uses FAISS vector database for semantic search and similarity matching
"""

import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional, Tuple
import logging
from datetime import datetime
import sqlite3

logger = logging.getLogger(__name__)

class AdvancedMemoryStore:
    """FAISS-based vector memory store with semantic search"""

    def __init__(self, db_path: str = "happy_memory.db", model_name: str = "all-MiniLM-L6-v2"):
        self.db_path = db_path
        self.model_name = model_name
        self.encoder = None
        self.index = None
        self.memories = []  # List of memory dicts
        self.dimension = 384  # Dimension for all-MiniLM-L6-v2

        self._init_encoder()
        self._init_index()
        self._load_memories()

    def _init_encoder(self):
        """Initialize the sentence transformer model"""
        try:
            self.encoder = SentenceTransformer(self.model_name)
            logger.info(f"Initialized sentence transformer: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize sentence transformer: {e}")
            raise

    def _init_index(self):
        """Initialize FAISS index"""
        try:
            # Use IndexFlatIP for cosine similarity (inner product)
            self.index = faiss.IndexFlatIP(self.dimension)
            logger.info("Initialized FAISS index")
        except Exception as e:
            logger.error(f"Failed to initialize FAISS index: {e}")
            raise

    def _load_memories(self):
        """Load memories from SQLite database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Create table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    vector BLOB
                )
            ''')

            # Load existing memories
            cursor.execute("SELECT id, key, value, timestamp FROM memories ORDER BY timestamp DESC")
            rows = cursor.fetchall()

            self.memories = []
            vectors = []

            for row in rows:
                memory_id, key, value, timestamp = row
                memory = {
                    "id": memory_id,
                    "key": key,
                    "value": value,
                    "timestamp": timestamp
                }
                self.memories.append(memory)

                # If vector exists, add to index
                if len(row) > 4 and row[4]:
                    vector = np.frombuffer(row[4], dtype=np.float32)
                    vectors.append(vector)

            if vectors:
                vectors_array = np.array(vectors).astype('float32')
                self.index.add(vectors_array)

            conn.close()
            logger.info(f"Loaded {len(self.memories)} memories from database")

        except Exception as e:
            logger.error(f"Failed to load memories: {e}")
            self.memories = []

    def _save_memory_to_db(self, key: str, value: str, vector: np.ndarray) -> int:
        """Save memory to SQLite database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Convert vector to bytes
            vector_bytes = vector.tobytes()

            cursor.execute(
                "INSERT INTO memories (key, value, vector) VALUES (?, ?, ?)",
                (key, value, vector_bytes)
            )

            memory_id = cursor.lastrowid
            conn.commit()
            conn.close()

            return memory_id

        except Exception as e:
            logger.error(f"Failed to save memory to database: {e}")
            raise

    def remember(self, key: str, value: str) -> bool:
        """Store a memory with semantic vector"""
        try:
            # Create combined text for embedding
            text_to_embed = f"{key}: {value}"

            # Generate embedding
            vector = self.encoder.encode([text_to_embed])[0].astype('float32')
            vector = vector / np.linalg.norm(vector)  # Normalize for cosine similarity

            # Add to FAISS index
            self.index.add(np.array([vector]))

            # Save to database
            memory_id = self._save_memory_to_db(key, value, vector)

            # Add to memory list
            memory = {
                "id": memory_id,
                "key": key,
                "value": value,
                "timestamp": datetime.now().isoformat()
            }
            self.memories.insert(0, memory)  # Add to beginning

            logger.info(f"Remembered: {key} = {value}")
            return True

        except Exception as e:
            logger.error(f"Failed to remember {key}: {e}")
            return False

    def recall(self, key: str) -> Optional[str]:
        """Recall a memory by exact key match"""
        try:
            for memory in self.memories:
                if memory["key"].lower() == key.lower():
                    return memory["value"]
            return None
        except Exception as e:
            logger.error(f"Failed to recall {key}: {e}")
            return None

    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search memories by semantic similarity"""
        try:
            if self.index.ntotal == 0:
                return []

            # Encode query
            query_vector = self.encoder.encode([query])[0].astype('float32')
            query_vector = query_vector / np.linalg.norm(query_vector)

            # Search FAISS index
            scores, indices = self.index.search(np.array([query_vector]), min(top_k, self.index.ntotal))

            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(self.memories):
                    memory = self.memories[idx].copy()
                    memory["similarity"] = float(score)
                    results.append(memory)

            # Sort by similarity score
            results.sort(key=lambda x: x["similarity"], reverse=True)

            return results

        except Exception as e:
            logger.error(f"Failed to perform semantic search: {e}")
            return []

    def recall_similar(self, query: str, threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Recall memories similar to the query"""
        try:
            results = self.semantic_search(query, top_k=10)

            # Filter by threshold
            filtered_results = [r for r in results if r["similarity"] >= threshold]

            return filtered_results

        except Exception as e:
            logger.error(f"Failed to recall similar memories: {e}")
            return []

    def recall_all(self) -> List[Dict[str, Any]]:
        """Get all memories"""
        return self.memories.copy()

    def forget(self, key: str) -> bool:
        """Remove a memory by key"""
        try:
            # Find and remove from list
            for i, memory in enumerate(self.memories):
                if memory["key"].lower() == key.lower():
                    removed_memory = self.memories.pop(i)

                    # Remove from database
                    conn = sqlite3.connect(self.db_path)
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM memories WHERE id = ?", (removed_memory["id"],))
                    conn.commit()
                    conn.close()

                    # Note: FAISS index doesn't support deletion easily
                    # In production, you'd rebuild the index
                    logger.info(f"Forgot: {key}")
                    return True

            return False

        except Exception as e:
            logger.error(f"Failed to forget {key}: {e}")
            return False

    def log_command(self, command: str, success: bool, message: str):
        """Log command execution (for compatibility)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Create command_history table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS command_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    command TEXT NOT NULL,
                    success BOOLEAN NOT NULL,
                    message TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            cursor.execute(
                "INSERT INTO command_history (command, success, message) VALUES (?, ?, ?)",
                (command, success, message)
            )

            conn.commit()
            conn.close()

        except Exception as e:
            logger.error(f"Failed to log command: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        return {
            "total_memories": len(self.memories),
            "index_size": self.index.ntotal,
            "model_name": self.model_name,
            "dimension": self.dimension
        }