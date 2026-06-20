"""Click Agent - Safe clicking with confirmation for risky actions"""

import logging
from typing import Dict, Any
import re

logger = logging.getLogger(__name__)


class ClickAgent:
    """Handles safe link/button clicking with risk assessment"""

    def __init__(self):
        # Patterns that require confirmation
        self.dangerous_patterns = {
            'payment': [
                r'payment', r'checkout', r'buy', r'purchase', r'subscribe',
                r'credit card', r'billing', r'price', r'cost', r'\$',
                r'stripe', r'paypal', r'amazon pay'
            ],
            'account': [
                r'login', r'sign in', r'register', r'sign up', r'password',
                r'change password', r'account settings', r'profile', r'delete account'
            ],
            'upload': [
                r'upload', r'attach', r'file', r'import', r'submit form',
                r'send', r'post'
            ],
            'external': [
                r'download', r'install', r'exe', r'msi', r'dmg',
                r'click here', r'run'
            ],
            'irreversible': [
                r'delete', r'remove', r'unsubscribe', r'cancel', r'close account',
                r'clear history', r'reset'
            ]
        }

    def safe_click(
        self,
        link_text: str = "",
        url: str = "",
        button_type: str = ""
    ) -> Dict[str, Any]:
        """
        Evaluate if it's safe to click and determine if confirmation needed
        
        Args:
            link_text: Text of the link/button
            url: Target URL
            button_type: Type of button (submit, button, link, etc)
            
        Returns:
            {
                "safe": bool,
                "needs_confirmation": bool,
                "risk_level": "low" | "medium" | "high" | "extreme",
                "reason": str,
                "action": "proceed" | "confirm" | "block"
            }
        """
        try:
            risk_assessment = self._assess_risk(link_text, url, button_type)
            risk_level = risk_assessment['risk_level']
            reasons = risk_assessment['reasons']
            
            return {
                "safe": risk_level != 'extreme',
                "needs_confirmation": risk_level in ['high', 'medium'],
                "risk_level": risk_level,
                "reason": "; ".join(reasons) if reasons else "Safe action",
                "action": self._get_action(risk_level)
            }
            
        except Exception as e:
            logger.error(f"Error assessing click safety: {e}")
            return {
                "safe": False,
                "needs_confirmation": True,
                "risk_level": "unknown",
                "reason": f"Error assessing safety: {str(e)}",
                "action": "confirm"
            }

    def _assess_risk(self, link_text: str, url: str, button_type: str) -> Dict[str, Any]:
        """Assess the risk level of clicking"""
        combined_text = f"{link_text} {url} {button_type}".lower()
        reasons = []
        risk_scores = {}
        
        # Check each danger category
        for category, patterns in self.dangerous_patterns.items():
            for pattern in patterns:
                if re.search(pattern, combined_text):
                    risk_scores[category] = risk_scores.get(category, 0) + 1
                    if category not in [r[0] for r in reasons]:
                        reasons.append(category)
        
        # Determine risk level
        total_matches = sum(risk_scores.values())
        
        if total_matches >= 3:
            return {
                'risk_level': 'extreme',
                'reasons': [f"Multiple dangerous patterns detected: {', '.join(set(reasons))}"]
            }
        elif total_matches == 2:
            return {
                'risk_level': 'high',
                'reasons': [f"High-risk action detected: {', '.join(set(reasons))}"]
            }
        elif total_matches == 1:
            return {
                'risk_level': 'medium',
                'reasons': [f"Potential {reasons[0]} action"]
            }
        else:
            return {
                'risk_level': 'low',
                'reasons': []
            }

    def _get_action(self, risk_level: str) -> str:
        """Get recommended action based on risk level"""
        mapping = {
            'low': 'proceed',
            'medium': 'confirm',
            'high': 'confirm',
            'extreme': 'block'
        }
        return mapping.get(risk_level, 'confirm')

    def is_form_submission(self, button_text: str, button_type: str = "") -> bool:
        """Check if action is a form submission"""
        return button_type == 'submit' or any(
            word in button_text.lower() for word in ['submit', 'send', 'post', 'confirm']
        )

    def is_navigation(self, link_text: str, url: str) -> bool:
        """Check if action is simple navigation"""
        dangerous_keywords = [
            'delete', 'remove', 'payment', 'login', 'upload', 'install'
        ]
        combined = f"{link_text} {url}".lower()
        
        return not any(keyword in combined for keyword in dangerous_keywords)

    def can_auto_click(self, link_text: str, url: str = "") -> bool:
        """Check if this can be clicked automatically without confirmation"""
        assessment = self.safe_click(link_text, url)
        return assessment['risk_level'] == 'low' and not assessment['needs_confirmation']

    def create_confirmation_message(self, link_text: str, url: str) -> str:
        """Create user-friendly confirmation message"""
        assessment = self.safe_click(link_text, url)
        
        message = f"About to click: {link_text}"
        if url:
            message += f"\nTarget: {url}"
        
        if assessment['reason']:
            message += f"\n\nWarning: {assessment['reason']}"
        
        message += "\n\nProceed?"
        
        return message
