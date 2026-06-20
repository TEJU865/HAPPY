"""
HAPPY Planner
Simple rule-based command planner
Parses user intent and breaks it into executable steps
"""

from enum import Enum
from dataclasses import dataclass

class CommandType(Enum):
    OPEN_APP = "open_app"
    REMEMBER = "remember"
    RECALL = "recall"
    CREATE_FOLDER = "create_folder"
    OPEN_WEBSITE = "open_website"
    SEARCH_WEB = "search_web"
    READ_FILE = "read_file"
    WRITE_FILE = "write_file"
    LIST_DIR = "list_dir"
    DELETE_FILE = "delete_file"
    MOVE_FILE = "move_file"
    COPY_FILE = "copy_file"
    CLICK_MOUSE = "click_mouse"
    TYPE_TEXT = "type_text"
    PRESS_KEY = "press_key"
    TAKE_SCREENSHOT = "take_screenshot"
    GET_MOUSE_POS = "get_mouse_pos"
    SPEAK_TEXT = "speak_text"
    LISTEN_VOICE = "listen_voice"
    SEMANTIC_RECALL = "semantic_recall"
    UNKNOWN = "unknown"

@dataclass
class Plan:
    """Execution plan for a command"""
    goal: str
    command_type: CommandType
    risk_level: str  # low, medium, high
    needs_confirmation: bool
    parameters: dict
    steps: list

class Planner:
    """Simple rule-based planner"""
    
    OPEN_KEYWORDS = ["open", "launch", "start", "run"]
    REMEMBER_KEYWORDS = ["remember", "save", "store", "note"]
    RECALL_KEYWORDS = ["recall", "what is", "who is", "tell me"]
    CREATE_KEYWORDS = ["create", "make", "mkdir", "new folder"]
    BROWSER_KEYWORDS = ["browse", "visit", "go to", "website", "web"]
    SEARCH_KEYWORDS = ["search", "find", "look up", "google"]
    FILE_KEYWORDS = ["file", "read", "write", "delete", "move", "copy", "list", "show"]
    MOUSE_KEYWORDS = ["click", "mouse", "cursor", "position"]
    TYPE_KEYWORDS = ["type", "write", "enter", "input"]
    SCREENSHOT_KEYWORDS = ["screenshot", "capture", "screen"]
    VOICE_KEYWORDS = ["speak", "say", "talk", "voice", "listen", "hear"]
    
    @staticmethod
    def parse_command(user_input: str) -> Plan:
        """
        Parse user command and create execution plan
        
        Args:
            user_input: User's text command
            
        Returns:
            Plan object with execution steps
        """
        input_lower = user_input.lower().strip()
        
        # Detect command type
        command_type = Planner._detect_command_type(input_lower)
        
        if command_type == CommandType.OPEN_APP:
            return Planner._plan_open_app(input_lower, user_input)
        elif command_type == CommandType.REMEMBER:
            return Planner._plan_remember(input_lower, user_input)
        elif command_type == CommandType.RECALL:
            return Planner._plan_recall(input_lower, user_input)
        elif command_type == CommandType.CREATE_FOLDER:
            return Planner._plan_create_folder(input_lower, user_input)
        elif command_type == CommandType.OPEN_WEBSITE:
            return Planner._plan_open_website(input_lower, user_input)
        elif command_type == CommandType.SEARCH_WEB:
            return Planner._plan_search_web(input_lower, user_input)
        elif command_type == CommandType.READ_FILE:
            return Planner._plan_read_file(input_lower, user_input)
        elif command_type == CommandType.WRITE_FILE:
            return Planner._plan_write_file(input_lower, user_input)
        elif command_type == CommandType.LIST_DIR:
            return Planner._plan_list_dir(input_lower, user_input)
        elif command_type == CommandType.DELETE_FILE:
            return Planner._plan_delete_file(input_lower, user_input)
        elif command_type == CommandType.MOVE_FILE:
            return Planner._plan_move_file(input_lower, user_input)
        elif command_type == CommandType.COPY_FILE:
            return Planner._plan_copy_file(input_lower, user_input)
        elif command_type == CommandType.CLICK_MOUSE:
            return Planner._plan_click_mouse(input_lower, user_input)
        elif command_type == CommandType.TYPE_TEXT:
            return Planner._plan_type_text(input_lower, user_input)
        elif command_type == CommandType.PRESS_KEY:
            return Planner._plan_press_key(input_lower, user_input)
        elif command_type == CommandType.TAKE_SCREENSHOT:
            return Planner._plan_take_screenshot(input_lower, user_input)
        elif command_type == CommandType.GET_MOUSE_POS:
            return Planner._plan_get_mouse_pos(input_lower, user_input)
        elif command_type == CommandType.SPEAK_TEXT:
            return Planner._plan_speak_text(input_lower, user_input)
        elif command_type == CommandType.LISTEN_VOICE:
            return Planner._plan_listen_voice(input_lower, user_input)
        elif command_type == CommandType.SEMANTIC_RECALL:
            return Planner._plan_semantic_recall(input_lower, user_input)
        else:
            return Planner._plan_unknown(user_input)
    
    @staticmethod
    def _detect_command_type(input_lower: str) -> CommandType:
        """Detect what type of command this is"""
        
        # Priority: Check REMEMBER first (before RECALL, since both have "is")
        # Remember patterns: "remember X is Y" or "remember X = Y"
        for keyword in Planner.REMEMBER_KEYWORDS:
            if keyword in input_lower:
                # Check if it has "is" or "=" after remember keyword
                if "is" in input_lower or "=" in input_lower:
                    return CommandType.REMEMBER
        
        # Check for recall patterns (what is, who is, tell me)
        # But NOT if it's a remember statement
        # ALSO check for fuzzy/semantic recall with keywords like "find" or "search memory"
        recall_found = False
        for keyword in Planner.RECALL_KEYWORDS:
            if keyword in input_lower:
                recall_found = True
                break
        
        # Also support semantic search patterns
        if ("find" in input_lower or "search memory" in input_lower or "look for" in input_lower) and "file" not in input_lower:
            recall_found = True
            return CommandType.SEMANTIC_RECALL
        
        if recall_found:
            # Make sure it's not "remember ... is"
            has_remember = any(k in input_lower for k in Planner.REMEMBER_KEYWORDS)
            if not has_remember:
                return CommandType.RECALL
        
        # Check for open patterns
        for keyword in Planner.OPEN_KEYWORDS:
            if keyword in input_lower:
                return CommandType.OPEN_APP
        
        # Check for create folder patterns
        for keyword in Planner.CREATE_KEYWORDS:
            if keyword in input_lower and ("folder" in input_lower or "directory" in input_lower):
                return CommandType.CREATE_FOLDER
        
        # Check for search patterns
        for keyword in Planner.SEARCH_KEYWORDS:
            if keyword in input_lower:
                return CommandType.SEARCH_WEB
        
        # Check for browser/website patterns
        for keyword in Planner.BROWSER_KEYWORDS:
            if keyword in input_lower:
                return CommandType.OPEN_WEBSITE
        
        # Check for URLs (contains .com, .org, etc.)
        if any(domain in input_lower for domain in [".com", ".org", ".net", ".edu", ".gov", "http", "www."]):
            return CommandType.OPEN_WEBSITE
        
        # Check for file operations
        if "read" in input_lower and ("file" in input_lower or ".txt" in input_lower or ".md" in input_lower):
            return CommandType.READ_FILE
        if "write" in input_lower and "file" in input_lower:
            return CommandType.WRITE_FILE
        if ("delete" in input_lower or "remove" in input_lower) and "file" in input_lower:
            return CommandType.DELETE_FILE
        if ("move" in input_lower or "rename" in input_lower) and "file" in input_lower:
            return CommandType.MOVE_FILE
        if "copy" in input_lower and "file" in input_lower:
            return CommandType.COPY_FILE
        if ("list" in input_lower or "show" in input_lower) and ("files" in input_lower or "directory" in input_lower or "folder" in input_lower):
            return CommandType.LIST_DIR
        
        # Check for mouse/click commands
        if "click" in input_lower and ("mouse" in input_lower or "screen" in input_lower or any(char.isdigit() for char in input_lower)):
            return CommandType.CLICK_MOUSE
        
        # Check for typing commands
        if any(k in input_lower for k in Planner.TYPE_KEYWORDS) and not "file" in input_lower:
            return CommandType.TYPE_TEXT
        
        # Check for key press commands
        if ("press" in input_lower or "hit" in input_lower) and ("key" in input_lower or len(input_lower.split()) == 2):
            return CommandType.PRESS_KEY
        
        # Check for screenshot commands
        if any(k in input_lower for k in Planner.SCREENSHOT_KEYWORDS):
            return CommandType.TAKE_SCREENSHOT
        
        # Check for mouse position commands
        if ("mouse" in input_lower or "cursor" in input_lower) and ("position" in input_lower or "where" in input_lower):
            return CommandType.GET_MOUSE_POS
        
        # Check for voice commands
        if any(k in input_lower for k in Planner.VOICE_KEYWORDS):
            if "listen" in input_lower or "hear" in input_lower:
                return CommandType.LISTEN_VOICE
            else:
                return CommandType.SPEAK_TEXT
        
        return CommandType.UNKNOWN
    
    @staticmethod
    def _plan_open_app(input_lower: str, original_input: str) -> Plan:
        """Plan: open an app"""
        # Extract app name
        app_name = ""
        for keyword in Planner.OPEN_KEYWORDS:
            if keyword in input_lower:
                app_name = input_lower.split(keyword, 1)[1].strip()
                break
        
        return Plan(
            goal=f"Open {app_name}",
            command_type=CommandType.OPEN_APP,
            risk_level="low",
            needs_confirmation=False,
            parameters={"app_name": app_name},
            steps=[
                {
                    "tool": "app_opener",
                    "action": "open",
                    "input": app_name
                }
            ]
        )
    
    @staticmethod
    def _plan_remember(input_lower: str, original_input: str) -> Plan:
        """Plan: remember something"""
        # Extract key and value (e.g., "remember my name is John" -> key="name", value="John")
        # or "remember project name = HAPPY" -> key="project name", value="HAPPY"
        
        # Remove remember prefix
        content = original_input
        for keyword in Planner.REMEMBER_KEYWORDS:
            if keyword in content.lower():
                idx = content.lower().find(keyword)
                content = content[idx + len(keyword):].strip()
                break
        
        # Split by "is" or "="
        if " is " in content.lower():
            key, value = content.lower().split(" is ", 1)
            key = key.replace("my ", "").strip()
        elif "=" in content:
            key, value = content.split("=", 1)
            key = key.strip()
        else:
            key = "memory"
            value = content
        
        value = value.strip()
        
        return Plan(
            goal=f"Remember {key}",
            command_type=CommandType.REMEMBER,
            risk_level="low",
            needs_confirmation=False,
            parameters={"key": key, "value": value},
            steps=[
                {
                    "tool": "memory_store",
                    "action": "remember",
                    "input": {"key": key, "value": value}
                }
            ]
        )
    
    @staticmethod
    def _plan_recall(input_lower: str, original_input: str) -> Plan:
        """Plan: recall a memory"""
        # Extract what to recall (e.g., "what is my name" -> "name")
        
        # Remove recall keywords
        content = original_input
        for keyword in Planner.RECALL_KEYWORDS:
            if keyword in content.lower():
                idx = content.lower().find(keyword)
                content = content[idx + len(keyword):].strip()
                break
        
        # Clean up "my" prefix
        key = content.replace("my ", "").strip().rstrip("?")
        
        return Plan(
            goal=f"Recall {key}",
            command_type=CommandType.RECALL,
            risk_level="low",
            needs_confirmation=False,
            parameters={"key": key},
            steps=[
                {
                    "tool": "memory_store",
                    "action": "recall",
                    "input": key
                }
            ]
        )
    
    @staticmethod
    def _plan_create_folder(input_lower: str, original_input: str) -> Plan:
        """Plan: create a folder"""
        # Extract folder name
        folder_name = original_input
        for keyword in Planner.CREATE_KEYWORDS:
            if keyword in input_lower:
                folder_name = input_lower.split(keyword, 1)[1].strip()
                break
        
        folder_name = folder_name.replace("folder", "").replace("directory", "").strip()
        
        return Plan(
            goal=f"Create folder '{folder_name}'",
            command_type=CommandType.CREATE_FOLDER,
            risk_level="low",
            needs_confirmation=False,
            parameters={"folder_name": folder_name},
            steps=[
                {
                    "tool": "file_manager",
                    "action": "create_folder",
                    "input": folder_name
                }
            ]
        )
    
    @staticmethod
    def _plan_unknown(user_input: str) -> Plan:
        """Plan: unknown command"""
        return Plan(
            goal="Unknown command",
            command_type=CommandType.UNKNOWN,
            risk_level="low",
            needs_confirmation=False,
            parameters={},
            steps=[]
        )
    
    @staticmethod
    def _plan_open_website(input_lower: str, original_input: str) -> Plan:
        """Plan: open a website"""
        # Extract URL or website name
        url = original_input
        for keyword in Planner.BROWSER_KEYWORDS:
            if keyword in input_lower:
                url = input_lower.split(keyword, 1)[1].strip()
                break
        
        # If no keyword found, assume the whole input is a URL/website
        if url == original_input:
            url = original_input.strip()
        
        return Plan(
            goal=f"Open website {url}",
            command_type=CommandType.OPEN_WEBSITE,
            risk_level="low",
            needs_confirmation=False,
            parameters={"url": url},
            steps=[
                {
                    "tool": "browser_tool",
                    "action": "open_website",
                    "input": url
                }
            ]
        )
    
    @staticmethod
    def _plan_search_web(input_lower: str, original_input: str) -> Plan:
        """Plan: search the web"""
        # Extract search query
        query = original_input
        for keyword in Planner.SEARCH_KEYWORDS:
            if keyword in input_lower:
                query = input_lower.split(keyword, 1)[1].strip()
                break
        
        return Plan(
            goal=f"Search web for '{query}'",
            command_type=CommandType.SEARCH_WEB,
            risk_level="low",
            needs_confirmation=False,
            parameters={"query": query},
            steps=[
                {
                    "tool": "browser_tool",
                    "action": "search_web",
                    "input": query
                }
            ]
        )
    
    @staticmethod
    def _plan_read_file(input_lower: str, original_input: str) -> Plan:
        """Plan: read a file"""
        # Extract file path
        file_path = original_input
        if "read file" in input_lower:
            file_path = input_lower.split("read file", 1)[1].strip()
        elif "read" in input_lower and ".txt" in input_lower:
            file_path = input_lower.split("read", 1)[1].strip()
        
        return Plan(
            goal=f"Read file '{file_path}'",
            command_type=CommandType.READ_FILE,
            risk_level="low",
            needs_confirmation=False,
            parameters={"file_path": file_path},
            steps=[
                {
                    "tool": "file_manager",
                    "action": "read_file",
                    "input": file_path
                }
            ]
        )
    
    @staticmethod
    def _plan_write_file(input_lower: str, original_input: str) -> Plan:
        """Plan: write to a file"""
        # This is complex - need to parse "write 'content' to file.txt"
        # For now, assume simple format
        parts = original_input.split(" to ")
        if len(parts) == 2:
            content = parts[0].replace("write file", "").replace("write", "").strip()
            file_path = parts[1].strip()
        else:
            content = "sample content"
            file_path = "new_file.txt"
        
        return Plan(
            goal=f"Write to file '{file_path}'",
            command_type=CommandType.WRITE_FILE,
            risk_level="medium",
            needs_confirmation=True,
            parameters={"file_path": file_path, "content": content},
            steps=[
                {
                    "tool": "file_manager",
                    "action": "write_file",
                    "input": {"file_path": file_path, "content": content}
                }
            ]
        )
    
    @staticmethod
    def _plan_list_dir(input_lower: str, original_input: str) -> Plan:
        """Plan: list directory contents"""
        dir_path = "."
        if "list files" in input_lower:
            dir_path = input_lower.split("list files", 1)[1].strip() or "."
        elif "show directory" in input_lower:
            dir_path = input_lower.split("show directory", 1)[1].strip() or "."
        
        return Plan(
            goal=f"List directory '{dir_path}'",
            command_type=CommandType.LIST_DIR,
            risk_level="low",
            needs_confirmation=False,
            parameters={"dir_path": dir_path},
            steps=[
                {
                    "tool": "file_manager",
                    "action": "list_directory",
                    "input": dir_path
                }
            ]
        )
    
    @staticmethod
    def _plan_delete_file(input_lower: str, original_input: str) -> Plan:
        """Plan: delete a file"""
        file_path = original_input
        if "delete file" in input_lower:
            file_path = input_lower.split("delete file", 1)[1].strip()
        
        return Plan(
            goal=f"Delete file '{file_path}'",
            command_type=CommandType.DELETE_FILE,
            risk_level="high",
            needs_confirmation=True,
            parameters={"file_path": file_path},
            steps=[
                {
                    "tool": "file_manager",
                    "action": "delete_file",
                    "input": file_path
                }
            ]
        )
    
    @staticmethod
    def _plan_move_file(input_lower: str, original_input: str) -> Plan:
        """Plan: move a file"""
        # Parse "move file.txt to new_location.txt"
        parts = original_input.split(" to ")
        if len(parts) == 2:
            source = parts[0].replace("move file", "").replace("move", "").strip()
            destination = parts[1].strip()
        else:
            source = "file.txt"
            destination = "new_file.txt"
        
        return Plan(
            goal=f"Move file from '{source}' to '{destination}'",
            command_type=CommandType.MOVE_FILE,
            risk_level="medium",
            needs_confirmation=True,
            parameters={"source": source, "destination": destination},
            steps=[
                {
                    "tool": "file_manager",
                    "action": "move_file",
                    "input": {"source": source, "destination": destination}
                }
            ]
        )
    
    @staticmethod
    def _plan_copy_file(input_lower: str, original_input: str) -> Plan:
        """Plan: copy a file"""
        # Parse "copy file.txt to backup.txt"
        parts = original_input.split(" to ")
        if len(parts) == 2:
            source = parts[0].replace("copy file", "").replace("copy", "").strip()
            destination = parts[1].strip()
        else:
            source = "file.txt"
            destination = "copy_file.txt"
        
        return Plan(
            goal=f"Copy file from '{source}' to '{destination}'",
            command_type=CommandType.COPY_FILE,
            risk_level="low",
            needs_confirmation=False,
            parameters={"source": source, "destination": destination},
            steps=[
                {
                    "tool": "file_manager",
                    "action": "copy_file",
                    "input": {"source": source, "destination": destination}
                }
            ]
        )
    
    @staticmethod
    def _plan_click_mouse(input_lower: str, original_input: str) -> Plan:
        """Plan: click mouse at position"""
        # Parse coordinates like "click at 100 200" or "click mouse 500 300"
        import re
        coords = re.findall(r'\d+', original_input)
        
        if len(coords) >= 2:
            x, y = int(coords[0]), int(coords[1])
        else:
            x, y = 100, 100  # Default position
        
        return Plan(
            goal=f"Click mouse at ({x}, {y})",
            command_type=CommandType.CLICK_MOUSE,
            risk_level="medium",
            needs_confirmation=True,
            parameters={"x": x, "y": y},
            steps=[
                {
                    "tool": "windows_automation",
                    "action": "click_at_position",
                    "input": {"x": x, "y": y}
                }
            ]
        )
    
    @staticmethod
    def _plan_type_text(input_lower: str, original_input: str) -> Plan:
        """Plan: type text"""
        # Extract text to type
        text = original_input
        for keyword in Planner.TYPE_KEYWORDS:
            if keyword in input_lower:
                text = input_lower.split(keyword, 1)[1].strip()
                break
        
        if not text or text == original_input:
            text = "Hello World"
        
        return Plan(
            goal=f"Type text '{text}'",
            command_type=CommandType.TYPE_TEXT,
            risk_level="medium",
            needs_confirmation=True,
            parameters={"text": text},
            steps=[
                {
                    "tool": "windows_automation",
                    "action": "type_text",
                    "input": text
                }
            ]
        )
    
    @staticmethod
    def _plan_press_key(input_lower: str, original_input: str) -> Plan:
        """Plan: press a key"""
        # Extract key name
        key = original_input.lower()
        if "press" in key:
            key = key.split("press", 1)[1].strip()
        elif "hit" in key:
            key = key.split("hit", 1)[1].strip()
        
        # Common key names
        key_map = {
            "enter": "enter",
            "return": "enter",
            "space": "space",
            "tab": "tab",
            "escape": "esc",
            "esc": "esc",
            "backspace": "backspace",
            "delete": "delete",
            "up": "up",
            "down": "down",
            "left": "left",
            "right": "right"
        }
        
        key = key_map.get(key, key)
        
        return Plan(
            goal=f"Press key '{key}'",
            command_type=CommandType.PRESS_KEY,
            risk_level="medium",
            needs_confirmation=True,
            parameters={"key": key},
            steps=[
                {
                    "tool": "windows_automation",
                    "action": "press_key",
                    "input": key
                }
            ]
        )
    
    @staticmethod
    def _plan_take_screenshot(input_lower: str, original_input: str) -> Plan:
        """Plan: take a screenshot"""
        filename = "screenshot.png"
        if "as" in input_lower:
            filename = input_lower.split("as", 1)[1].strip()
        
        return Plan(
            goal=f"Take screenshot as '{filename}'",
            command_type=CommandType.TAKE_SCREENSHOT,
            risk_level="low",
            needs_confirmation=False,
            parameters={"filename": filename},
            steps=[
                {
                    "tool": "windows_automation",
                    "action": "take_screenshot",
                    "input": filename
                }
            ]
        )
    
    @staticmethod
    def _plan_get_mouse_pos(input_lower: str, original_input: str) -> Plan:
        """Plan: get mouse position"""
        return Plan(
            goal="Get current mouse position",
            command_type=CommandType.GET_MOUSE_POS,
            risk_level="low",
            needs_confirmation=False,
            parameters={},
            steps=[
                {
                    "tool": "windows_automation",
                    "action": "get_mouse_position",
                    "input": None
                }
            ]
        )
    
    @staticmethod
    def _plan_speak_text(input_lower: str, original_input: str) -> Plan:
        """Plan: speak text"""
        # Extract text to speak
        text = original_input
        for keyword in Planner.VOICE_KEYWORDS:
            if keyword in input_lower:
                text = input_lower.split(keyword, 1)[1].strip()
                break
        
        if not text or text == original_input:
            text = "Hello, I am HAPPY, your personal AI assistant."
        
        return Plan(
            goal=f"Speak text '{text}'",
            command_type=CommandType.SPEAK_TEXT,
            risk_level="low",
            needs_confirmation=False,
            parameters={"text": text},
            steps=[
                {
                    "tool": "voice_output",
                    "action": "speak",
                    "input": text
                }
            ]
        )
    
    @staticmethod
    def _plan_listen_voice(input_lower: str, original_input: str) -> Plan:
        """Plan: listen for voice input"""
        return Plan(
            goal="Listen for voice input and transcribe",
            command_type=CommandType.LISTEN_VOICE,
            risk_level="low",
            needs_confirmation=False,
            parameters={},
            steps=[
                {
                    "tool": "voice_input",
                    "action": "listen_and_transcribe",
                    "input": None
                }
            ]
        )
    
    @staticmethod
    def _plan_semantic_recall(input_lower: str, original_input: str) -> Plan:
        """Plan: semantic search in memory"""
        # Extract search query
        query = original_input
        keywords = ["find", "search", "look for"]
        for keyword in keywords:
            if keyword in input_lower:
                query = input_lower.split(keyword, 1)[1].strip()
                break
        
        return Plan(
            goal=f"Search memory for '{query}'",
            command_type=CommandType.SEMANTIC_RECALL,
            risk_level="low",
            needs_confirmation=False,
            parameters={"query": query},
            steps=[
                {
                    "tool": "memory_store",
                    "action": "semantic_search",
                    "input": query
                }
            ]
        )
