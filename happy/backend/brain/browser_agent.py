"""Browser Agent - High-level browser workflow planning"""

import logging
from typing import List, Dict, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class BrowserStep:
    """Represents a single browser operation step"""
    order: int
    action: str  # search, open, read, summarize, click, save, etc
    target: str  # query, URL, selector, etc
    description: str
    requires_confirmation: bool = False
    expected_result: str = ""


class BrowserAgent:
    """Plans and coordinates browser automation workflows"""

    def __init__(self):
        self.action_templates = {
            'search': {
                'description': 'Search for query using search engine',
                'returns': 'List of search results'
            },
            'open': {
                'description': 'Open URL in browser',
                'returns': 'Page loaded'
            },
            'read': {
                'description': 'Read and extract page content',
                'returns': 'Extracted text, links, buttons'
            },
            'summarize': {
                'description': 'Summarize page content',
                'returns': 'Summary and key points'
            },
            'click': {
                'description': 'Click on link or button',
                'returns': 'Page action executed'
            },
            'save': {
                'description': 'Save page to memory',
                'returns': 'Saved to history'
            },
            'extract': {
                'description': 'Extract specific information',
                'returns': 'Extracted data'
            }
        }

    def plan_workflow(self, user_command: str) -> Dict[str, Any]:
        """
        Plan a complete browser workflow from user command
        
        Example inputs:
        - "search FastAPI tutorial"
        - "research Python async programming"
        - "find and save the best FastAPI guide"
        - "search for Python async tutorial and summarize the top result"
        
        Returns:
            {
                "success": bool,
                "workflow": [BrowserStep objects],
                "total_steps": int,
                "estimated_duration": str,
                "goal": str,
                "message": str
            }
        """
        try:
            command_lower = user_command.lower()
            
            # Detect workflow type
            if self._is_search_workflow(command_lower):
                workflow = self._plan_search_workflow(user_command)
            elif self._is_research_workflow(command_lower):
                workflow = self._plan_research_workflow(user_command)
            elif self._is_find_and_save_workflow(command_lower):
                workflow = self._plan_find_and_save_workflow(user_command)
            elif self._is_compare_workflow(command_lower):
                workflow = self._plan_compare_workflow(user_command)
            else:
                workflow = self._plan_generic_workflow(user_command)
            
            return workflow
            
        except Exception as e:
            logger.error(f"Error planning workflow: {e}")
            return {
                "success": False,
                "workflow": [],
                "message": f"Error planning workflow: {str(e)}"
            }

    def _is_search_workflow(self, command: str) -> bool:
        """Detect simple search workflow"""
        keywords = ['search', 'find', 'look for', 'google']
        return any(kw in command for kw in keywords) and not any(
            kw in command for kw in ['save', 'summarize', 'research']
        )

    def _is_research_workflow(self, command: str) -> bool:
        """Detect research workflow (search + read + summarize)"""
        keywords = ['research', 'learn about', 'tell me about']
        return any(kw in command for kw in keywords)

    def _is_find_and_save_workflow(self, command: str) -> bool:
        """Detect find and save workflow"""
        keywords = ['find', 'save', 'collect', 'gather']
        return all(any(kw in command for kw in k) for k in [
            ['find', 'search', 'look'],
            ['save', 'store', 'collect']
        ])

    def _is_compare_workflow(self, command: str) -> bool:
        """Detect compare workflow"""
        keywords = ['compare', 'vs', 'versus', 'difference', 'similar']
        return any(kw in command for kw in keywords)

    def _plan_search_workflow(self, command: str) -> Dict[str, Any]:
        """Plan simple search: search -> return results"""
        # Extract query
        query = self._extract_query(command, ['search for', 'search', 'find', 'look for'])
        
        steps = [
            BrowserStep(
                order=1,
                action='search',
                target=query,
                description=f"Search for '{query}'",
                expected_result='List of search results'
            )
        ]
        
        return {
            "success": True,
            "workflow": steps,
            "total_steps": len(steps),
            "goal": f"Search for '{query}'",
            "estimated_duration": "10-15 seconds",
            "message": "Search workflow planned"
        }

    def _plan_research_workflow(self, command: str) -> Dict[str, Any]:
        """Plan research: search -> open top result -> read -> summarize"""
        query = self._extract_query(
            command,
            ['research', 'learn about', 'tell me about', 'find information about']
        )
        
        steps = [
            BrowserStep(
                order=1,
                action='search',
                target=query,
                description=f"Search for '{query}'",
                expected_result='Search results'
            ),
            BrowserStep(
                order=2,
                action='open',
                target='{top_result_url}',
                description='Open the best search result',
                expected_result='Page loaded'
            ),
            BrowserStep(
                order=3,
                action='read',
                target='{current_page}',
                description='Extract page content',
                expected_result='Page text, links, structure'
            ),
            BrowserStep(
                order=4,
                action='summarize',
                target='{page_content}',
                description='Summarize the page',
                expected_result='Summary and key points'
            ),
            BrowserStep(
                order=5,
                action='save',
                target='{summary}',
                description='Save result to memory',
                expected_result='Saved to browser history'
            )
        ]
        
        return {
            "success": True,
            "workflow": steps,
            "total_steps": len(steps),
            "goal": f"Research '{query}' and summarize findings",
            "estimated_duration": "1-2 minutes",
            "message": "Research workflow planned"
        }

    def _plan_find_and_save_workflow(self, command: str) -> Dict[str, Any]:
        """Plan find and save: search -> filter -> save multiple results"""
        query = self._extract_query(command, ['find', 'search', 'look for'])
        
        steps = [
            BrowserStep(
                order=1,
                action='search',
                target=query,
                description=f"Search for '{query}'",
                expected_result='Search results'
            ),
            BrowserStep(
                order=2,
                action='extract',
                target='{search_results}',
                description='Extract and filter relevant results',
                expected_result='Filtered result list'
            ),
            BrowserStep(
                order=3,
                action='save',
                target='{filtered_results}',
                description='Save selected results to memory',
                expected_result='Results saved'
            )
        ]
        
        return {
            "success": True,
            "workflow": steps,
            "total_steps": len(steps),
            "goal": f"Find and save '{query}' results",
            "estimated_duration": "30-45 seconds",
            "message": "Find and save workflow planned"
        }

    def _plan_compare_workflow(self, command: str) -> Dict[str, Any]:
        """Plan compare: search both items -> open -> compare"""
        items = self._extract_compare_items(command)
        
        if len(items) < 2:
            return self._plan_search_workflow(command)
        
        steps = [
            BrowserStep(
                order=1,
                action='search',
                target=items[0],
                description=f"Search for '{items[0]}'",
                expected_result='Search results'
            ),
            BrowserStep(
                order=2,
                action='open',
                target='{top_result_for_item1}',
                description=f'Open top result for "{items[0]}"',
                expected_result='Page loaded'
            ),
            BrowserStep(
                order=3,
                action='read',
                target='{current_page}',
                description=f'Extract info about "{items[0]}"',
                expected_result='Extracted content'
            ),
            BrowserStep(
                order=4,
                action='search',
                target=items[1],
                description=f"Search for '{items[1]}'",
                expected_result='Search results'
            ),
            BrowserStep(
                order=5,
                action='open',
                target='{top_result_for_item2}',
                description=f'Open top result for "{items[1]}"',
                expected_result='Page loaded'
            ),
            BrowserStep(
                order=6,
                action='read',
                target='{current_page}',
                description=f'Extract info about "{items[1]}"',
                expected_result='Extracted content'
            ),
            BrowserStep(
                order=7,
                action='summarize',
                target='{comparison}',
                description=f'Compare findings',
                expected_result='Comparison summary'
            )
        ]
        
        return {
            "success": True,
            "workflow": steps,
            "total_steps": len(steps),
            "goal": f"Compare '{items[0]}' vs '{items[1]}'",
            "estimated_duration": "2-3 minutes",
            "message": "Comparison workflow planned"
        }

    def _plan_generic_workflow(self, command: str) -> Dict[str, Any]:
        """Plan generic workflow based on command"""
        steps = [
            BrowserStep(
                order=1,
                action='search',
                target=command,
                description=f"Process command: {command}",
                expected_result='Results'
            )
        ]
        
        return {
            "success": True,
            "workflow": steps,
            "total_steps": len(steps),
            "goal": command,
            "estimated_duration": "15-30 seconds",
            "message": "Generic workflow planned"
        }

    def _extract_query(self, command: str, prefixes: List[str]) -> str:
        """Extract search query from command"""
        for prefix in prefixes:
            if prefix in command.lower():
                idx = command.lower().find(prefix)
                query = command[idx + len(prefix):].strip()
                # Clean up common words
                for word in ['and', 'to', 'about']:
                    if query.startswith(word + ' '):
                        query = query[len(word):].strip()
                return query
        return command

    def _extract_compare_items(self, command: str) -> List[str]:
        """Extract items to compare from command"""
        separators = [' vs ', ' versus ', ' compared to ', ' vs.']
        
        for sep in separators:
            if sep in command.lower():
                parts = command.lower().split(sep)
                return [p.strip() for p in parts if p.strip()]
        
        return command.split()[:2]

    def execute_step(self, step: BrowserStep) -> Dict[str, Any]:
        """
        Execute a single workflow step
        (Note: This would be called by main execution engine)
        """
        return {
            "step": step.order,
            "action": step.action,
            "status": "ready",
            "message": f"Ready to execute: {step.description}"
        }

    def get_step_description(self, step: BrowserStep) -> str:
        """Get human-readable description of a step"""
        return f"Step {step.order}: {step.description}"
