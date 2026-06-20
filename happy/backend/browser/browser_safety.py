"""Browser Safety - Safety checks for browser automation"""

import logging
import re
from typing import Dict, Any, List
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class BrowserSafety:
    """Handles safety checks for browser operations"""

    def __init__(self):
        # URLs/patterns to block
        self.blocked_domains = [
            'malware', 'phishing', 'scam', 'hack', 'trojan',
            'virus', 'ransomware', 'bitcoin', 'crypto'
        ]
        
        self.blocked_paths = [
            'system32', 'windows', 'registry', '/root', '/etc', '/bin',
            'cmd.exe', 'powershell.exe'
        ]
        
        # Login/payment sites that need confirmation
        self.sensitive_patterns = {
            'login': [
                'login', 'sign in', 'signin', 'sign-in', 'auth', 'authenticate',
                'password', 'credentials'
            ],
            'payment': [
                'payment', 'checkout', 'billing', 'credit card', 'cvv',
                'stripe', 'paypal', 'amazon pay', 'buy', 'purchase', 'subscribe'
            ],
            'personal': [
                'ssn', 'social security', 'passport', 'driver license',
                'bank account', 'routing number'
            ],
            'upload': [
                'upload', 'attach', 'file', 'form submit', 'send file'
            ]
        }
        
        self.safe_domains = [
            'github.com', 'stackoverflow.com', 'wikipedia.org', 'python.org',
            'google.com', 'duckduckgo.com', 'wikipedia.org'
        ]

    def check_url(self, url: str) -> Dict[str, Any]:
        """
        Check if a URL is safe to visit
        
        Returns:
            {
                "safe": bool,
                "reason": str,
                "needs_confirmation": bool,
                "risk_level": "low" | "medium" | "high" | "extreme"
            }
        """
        try:
            url_lower = url.lower()
            
            # Block dangerous domains
            for blocked in self.blocked_domains:
                if blocked in url_lower:
                    return {
                        "safe": False,
                        "reason": f"Domain contains blocked keyword: {blocked}",
                        "needs_confirmation": False,
                        "risk_level": "extreme",
                        "action": "block"
                    }
            
            # Check for suspicious patterns
            if re.search(r'[;|&><()$`]', url):
                return {
                    "safe": False,
                    "reason": "URL contains suspicious characters (injection attempt?)",
                    "needs_confirmation": False,
                    "risk_level": "extreme",
                    "action": "block"
                }
            
            # Parse URL
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            # Check for whitelisted safe domains
            for safe_domain in self.safe_domains:
                if safe_domain in domain:
                    return {
                        "safe": True,
                        "reason": f"Whitelisted domain: {domain}",
                        "needs_confirmation": False,
                        "risk_level": "low",
                        "action": "proceed"
                    }
            
            # Check for sensitive content
            for category, patterns in self.sensitive_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, url_lower):
                        return {
                            "safe": True,
                            "reason": f"Site may require {category} information",
                            "needs_confirmation": True,
                            "risk_level": "high",
                            "action": "confirm"
                        }
            
            # Default: safe but monitor
            return {
                "safe": True,
                "reason": "URL appears safe",
                "needs_confirmation": False,
                "risk_level": "low",
                "action": "proceed"
            }
            
        except Exception as e:
            logger.error(f"Error checking URL: {e}")
            return {
                "safe": False,
                "reason": f"Error checking URL safety: {str(e)}",
                "needs_confirmation": True,
                "risk_level": "unknown",
                "action": "confirm"
            }

    def check_content(self, html: str, url: str = "") -> Dict[str, Any]:
        """
        Check page content for suspicious elements
        
        Returns:
            {
                "safe": bool,
                "warnings": [str],
                "has_login_form": bool,
                "has_payment_form": bool,
                "has_file_upload": bool,
                "risk_level": "low" | "medium" | "high"
            }
        """
        try:
            html_lower = html.lower()
            warnings = []
            
            has_login_form = False
            has_payment_form = False
            has_file_upload = False
            
            # Check for login forms
            if re.search(r'<input[^>]*type=["\']?password', html_lower):
                has_login_form = True
                warnings.append("Page contains password input field")
            
            if re.search(r'<form[^>]*login|sign.?in', html_lower):
                has_login_form = True
                warnings.append("Page contains login form")
            
            # Check for payment forms
            if re.search(r'credit.?card|cvv|expir|stripe|paypal', html_lower):
                has_payment_form = True
                warnings.append("Page contains payment information fields")
            
            # Check for file uploads
            if re.search(r'<input[^>]*type=["\']?file', html_lower):
                has_file_upload = True
                warnings.append("Page contains file upload field")
            
            # Determine risk level
            if has_payment_form and has_file_upload:
                risk_level = "high"
            elif has_login_form or has_payment_form or has_file_upload:
                risk_level = "medium"
            else:
                risk_level = "low"
            
            return {
                "safe": risk_level != "high",
                "warnings": warnings,
                "has_login_form": has_login_form,
                "has_payment_form": has_payment_form,
                "has_file_upload": has_file_upload,
                "risk_level": risk_level
            }
            
        except Exception as e:
            logger.error(f"Error checking content: {e}")
            return {
                "safe": True,
                "warnings": [f"Could not fully analyze page: {str(e)}"],
                "has_login_form": False,
                "has_payment_form": False,
                "has_file_upload": False,
                "risk_level": "unknown"
            }

    def is_safe_action(self, action: str, target: str = "") -> Dict[str, Any]:
        """Check if an action is safe"""
        actions_requiring_confirmation = {
            'click_payment_button': 'Payment action requires confirmation',
            'submit_form_with_password': 'Form with password requires confirmation',
            'upload_file': 'File upload requires confirmation',
            'download_file': 'File download may require confirmation',
            'fill_payment_form': 'Entering payment info requires confirmation'
        }
        
        if action in actions_requiring_confirmation:
            return {
                "safe": True,
                "needs_confirmation": True,
                "reason": actions_requiring_confirmation[action],
                "risk_level": "high"
            }
        
        dangerous_actions = {
            'delete_file': 'Cannot delete files',
            'install_software': 'Cannot install software',
            'modify_registry': 'Cannot modify system registry',
            'run_script': 'Cannot run scripts'
        }
        
        if action in dangerous_actions:
            return {
                "safe": False,
                "needs_confirmation": False,
                "reason": dangerous_actions[action],
                "risk_level": "extreme"
            }
        
        # Default safe
        return {
            "safe": True,
            "needs_confirmation": False,
            "reason": "Action appears safe",
            "risk_level": "low"
        }

    def should_block_redirect(self, source_url: str, target_url: str) -> bool:
        """Check if redirect should be blocked"""
        # Block redirects to file:// or unusual protocols
        if target_url.startswith(('file://', 'data:', 'javascript:')):
            return True
        
        # Block redirects to different domain from https to http (downgrade)
        source_domain = urlparse(source_url).netloc
        target_domain = urlparse(target_url).netloc
        
        if source_domain != target_domain:
            source_https = source_url.startswith('https')
            target_https = target_url.startswith('https')
            
            if source_https and not target_https:
                return True  # HTTPS downgrade
        
        return False

    def sanitize_input(self, user_input: str) -> str:
        """Sanitize user input for safety"""
        # Remove dangerous characters
        dangerous_chars = [';', '|', '&', '<', '>', '(', ')', '$', '`', '\n', '\r']
        
        for char in dangerous_chars:
            user_input = user_input.replace(char, '')
        
        # Limit length
        user_input = user_input[:500]
        
        return user_input.strip()

    def get_safety_report(self, url: str, html: str = "") -> Dict[str, Any]:
        """Generate comprehensive safety report"""
        url_check = self.check_url(url)
        content_check = self.check_content(html, url) if html else None
        
        warnings = []
        if url_check.get('reason'):
            warnings.append(url_check['reason'])
        
        if content_check:
            warnings.extend(content_check.get('warnings', []))
        
        # Determine overall risk
        risks = [url_check.get('risk_level', 'low')]
        if content_check:
            risks.append(content_check.get('risk_level', 'low'))
        
        risk_levels = {'extreme': 3, 'high': 2, 'medium': 1, 'low': 0}
        max_risk = max(risk_levels.get(r, 0) for r in risks)
        risk_mapping = {3: 'extreme', 2: 'high', 1: 'medium', 0: 'low'}
        overall_risk = risk_mapping.get(max_risk, 'low')
        
        return {
            "url": url,
            "overall_safe": overall_risk in ['low', 'medium'],
            "overall_risk": overall_risk,
            "warnings": list(set(warnings)),  # Remove duplicates
            "url_check": url_check,
            "content_check": content_check,
            "needs_confirmation": overall_risk in ['high', 'medium']
        }
