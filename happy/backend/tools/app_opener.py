"""
HAPPY App Opener Tool (Upgraded)
Automatically detects Windows applications and supports multiple command variations.
"""

import subprocess
import os
import winreg
from pathlib import Path
import re

class AppOpener:
    """Dynamically discover and open Windows applications"""
    
    # Pre-defined aliases for common apps to support different user commands
    APP_ALIASES = {
        "code": ["vscode", "vs code", "visual studio code", "editor"],
        "calc.exe": ["calculator", "calc", "compute"],
        "notepad.exe": ["notepad", "text editor", "note"],
        "chrome.exe": ["chrome", "google chrome", "browser"],
        "msedge.exe": ["edge", "microsoft edge", "internet explorer"],
        "firefox.exe": ["firefox", "mozilla firefox"],
        "explorer.exe": ["explorer", "file explorer", "my computer", "files"],
        "powershell.exe": ["powershell", "ps"],
        "cmd.exe": ["cmd", "command prompt", "terminal"],
        "wt.exe": ["terminal", "windows terminal"],
        "taskmgr.exe": ["task manager", "taskmgr", "processes"],
        "mspaint.exe": ["paint", "mspaint", "draw"],
    }

    def __init__(self):
        # This will hold the dynamically scanned system apps
        self.detected_apps = {}
        self.refresh_apps()

    def refresh_apps(self):
        """Scans the system to automatically detect newly installed apps and shortcuts"""
        self.detected_apps = {}
        
        # 1. Scan Windows Start Menu Directories (where 99% of apps put shortcuts)
        start_menu_paths = [
            Path(os.environ.get("ProgramData", "C:\\ProgramData")) / "Microsoft\\Windows\\Start Menu\\Programs",
            Path(os.environ.get("AppData", "")) / "Microsoft\\Windows\\Start Menu\\Programs"
        ]
        
        for path in start_menu_paths:
            if path.exists():
                for file in path.rglob("*.lnk"): # Find all shortcuts
                    name = file.stem.lower().strip()
                    # Map the shortcut name to its path so Windows can launch it directly
                    self.detected_apps[name] = str(file)

        # 2. Inject core system executables and their custom aliases
        for exe, aliases in self.APP_ALIASES.items():
            for alias in aliases:
                # If the alias isn't already pointing to a shortcut, map it to the executable
                if alias not in self.detected_apps:
                    self.detected_apps[alias] = exe

    def open(self, user_command: str) -> dict:
        """
        Open an application based on a flexible user command.
        
        Args:
            user_command: The name or phrase entered by the user (e.g., "vs code", "Calculator")
            
        Returns:
            dict with success status and message
        """
        # Clean up the input string
        clean_command = user_command.lower().strip()
        
        # Remove common filler phrases if the user says something like "open chrome" or "launch notepad"
        clean_command = re.sub(r'^(open|launch|run|start)\s+', '', clean_command)

        # 1. Try an exact or alias match from our dynamic map
        target = self.detected_apps.get(clean_command)

        # 2. If no exact match, try a partial keyword match (e.g., "visual" matches "visual studio code")
        if not target:
            for app_name, app_path in self.detected_apps.items():
                if clean_command in app_name or app_name in clean_command:
                    target = app_path
                    clean_command = app_name  # Update display name to what we found
                    break

        # 3. If still not found, try to run whatever the user typed directly as a fallback
        if not target:
            target = clean_command

        return self._launch_app(target, user_command)

    def _launch_app(self, target: str, display_name: str) -> dict:
        """Launch the targeted file, shortcut, or executable safely"""
        try:
            # os.startfile is perfect for Windows as it handles shortcuts (.lnk), 
            # executables, and registered system paths automatically.
            os.startfile(target)
            return {
                "success": True,
                "message": f"Successfully opened '{display_name}'",
                "target_launched": target
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Could not open '{display_name}'. application not found or access denied.",
                "error": str(e)
            }

# --- Example Usage ---
if __name__ == "__main__":
    opener = AppOpener()
    
    # Test 1: Testing different command variations for one app (VS Code)
    print(opener.open("vs code"))
    print(opener.open("visual studio code"))
    print(opener.open("editor"))
    
    # Test 2: Testing system apps
    print(opener.open("open calculator"))
    
    # Test 3: Automatically detecting a newly installed app 
    # If you install a new game or software, calling refresh_apps or re-initializing will catch it
    # opener.refresh_apps()