"""Page Summarizer - Extracts key information from page content"""

import logging
from typing import Dict, Any, List
import re

logger = logging.getLogger(__name__)


class PageSummarizer:
    """Summarizes page content into concise form"""

    def __init__(self):
        self.length_settings = {
            'short': 3,
            'medium': 5,
            'long': 10
        }

    def summarize(self, page_content: Dict[str, Any], length: str = 'medium') -> Dict[str, Any]:
        """
        Summarize page content
        
        Args:
            page_content: Page content dict from PageReader.read()
            length: 'short', 'medium', or 'long'
            
        Returns:
            {
                "success": bool,
                "summary": str,
                "key_points": [str],
                "length": str,
                "word_count": int,
                "message": str
            }
        """
        try:
            if not isinstance(page_content, dict) or 'text' not in page_content:
                return {
                    "success": False,
                    "message": "Invalid page content"
                }
            
            text = page_content.get('text', '')
            if not text:
                return {
                    "success": False,
                    "message": "No text content to summarize"
                }
            
            # Validate length parameter
            if length not in self.length_settings:
                length = 'medium'
            
            # Extract key points
            key_points = self._extract_key_points(text, length)
            
            # Generate summary
            summary = self._generate_summary(text, key_points)
            
            # Calculate word count
            word_count = len(summary.split())
            
            return {
                "success": True,
                "summary": summary,
                "key_points": key_points,
                "length": length,
                "word_count": word_count,
                "title": page_content.get('title', ''),
                "url": page_content.get('url', ''),
                "message": f"Summary generated ({word_count} words)"
            }
            
        except Exception as e:
            logger.error(f"Error summarizing: {e}")
            return {
                "success": False,
                "message": f"Summarization error: {str(e)}"
            }

    def _extract_key_points(self, text: str, length: str = 'medium') -> List[str]:
        """Extract key sentences from text"""
        try:
            # Split text into sentences
            sentences = self._split_sentences(text)
            
            if not sentences:
                return []
            
            # Get number of key points to extract
            num_points = self.length_settings.get(length, 5)
            num_points = min(num_points, len(sentences))
            
            # Score sentences by position and content
            scored_sentences = []
            
            for idx, sentence in enumerate(sentences):
                # Calculate importance score
                score = 0
                
                # Position score (earlier sentences weighted higher)
                position_score = (1 - (idx / len(sentences))) * 2
                score += position_score
                
                # Length score (moderate length sentences)
                word_count = len(sentence.split())
                if 10 <= word_count <= 50:
                    score += 2
                
                # Keyword score
                keywords = ['important', 'key', 'main', 'significant', 'critical', 'essential']
                for keyword in keywords:
                    if keyword in sentence.lower():
                        score += 1
                
                scored_sentences.append((sentence, score))
            
            # Sort by score and take top N
            top_sentences = sorted(scored_sentences, key=lambda x: x[1], reverse=True)[:num_points]
            
            # Re-order by original position
            key_points = [sent for sent, _ in sorted(
                top_sentences,
                key=lambda x: sentences.index(x[0])
            )]
            
            return [self._clean_sentence(s) for s in key_points]
            
        except Exception as e:
            logger.error(f"Error extracting key points: {e}")
            return []

    def _generate_summary(self, text: str, key_points: List[str]) -> str:
        """Generate a summary from key points"""
        try:
            if not key_points:
                # Fallback: return first 200 characters
                return text[:200].rstrip() + "..."
            
            # Combine key points into a summary
            summary = " ".join(key_points)
            
            # Limit length
            if len(summary) > 1000:
                summary = summary[:1000].rsplit(' ', 1)[0] + "..."
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return text[:200]

    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        try:
            # Simple sentence splitting by punctuation
            sentences = re.split(r'[.!?]+', text)
            
            # Clean and filter sentences
            cleaned = []
            for sentence in sentences:
                sentence = sentence.strip()
                if sentence and len(sentence) > 10:  # Minimum length
                    cleaned.append(sentence)
            
            return cleaned
            
        except Exception as e:
            logger.error(f"Error splitting sentences: {e}")
            return []

    def _clean_sentence(self, sentence: str) -> str:
        """Clean and normalize sentence"""
        try:
            # Remove extra whitespace
            sentence = ' '.join(sentence.split())
            
            # Ensure proper capitalization
            if sentence and not sentence[0].isupper():
                sentence = sentence[0].upper() + sentence[1:]
            
            # Ensure ends with punctuation
            if sentence and not sentence.endswith(('.', '!', '?')):
                sentence += '.'
            
            return sentence
            
        except:
            return sentence

    def extract_metadata(self, page_content: Dict[str, Any]) -> Dict[str, Any]:
        """Extract metadata from page content"""
        return {
            "title": page_content.get('title', ''),
            "url": page_content.get('url', ''),
            "num_links": len(page_content.get('links', [])),
            "num_images": len(page_content.get('images', [])),
            "has_login": hasattr(page_content, 'has_login_form'),
            "has_payment": hasattr(page_content, 'has_payment_form')
        }

    def create_outline(self, text: str) -> List[str]:
        """Create an outline from text"""
        try:
            lines = text.split('\n')
            outline = []
            
            for line in lines[:20]:  # First 20 lines
                line = line.strip()
                if line and len(line) > 5:
                    outline.append(f"• {line[:80]}")
            
            return outline
            
        except Exception as e:
            logger.error(f"Error creating outline: {e}")
            return []
