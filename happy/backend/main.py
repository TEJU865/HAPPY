"""
HAPPY V0.1 Backend
Main FastAPI server for HAPPY - Personal Windows AI Automation Assistant

Core abilities:
- Accept text commands
- Parse intent with planner
- Execute tools (open apps, save/recall memory)
- Return safe responses
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import json
import os

# Import core modules
from brain.planner import Planner, CommandType
from brain.browser_agent import BrowserAgent
from tools.app_opener import AppOpener
from tools.browser_tool import BrowserTool
from tools.file_manager import FileManager
from tools.windows_automation import WindowsAutomation
from tools.voice_output import VoiceOutput
from tools.voice_input import VoiceInput
from memory.advanced_memory import AdvancedMemoryStore

# Import browser modules
from browser.browser_controller import BrowserController
from browser.search_engine import SearchEngine
from browser.page_reader import PageReader
from browser.page_summarizer import PageSummarizer
from browser.click_agent import ClickAgent
from browser.browser_memory import BrowserMemory
from browser.browser_safety import BrowserSafety

# Initialize FastAPI app
app = FastAPI(
    title="HAPPY Backend",
    description="Personal Windows AI Automation Assistant",
    version="0.1.0"
)

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize modules
memory_store = AdvancedMemoryStore("happy_memory.db")
planner = Planner()
app_opener = AppOpener()
browser_tool = BrowserTool()
file_manager = FileManager()
windows_automation = WindowsAutomation()
voice_output = VoiceOutput()
voice_input = VoiceInput()

# Initialize browser modules
browser_controller = BrowserController()
search_engine = SearchEngine()
page_reader = PageReader()
page_summarizer = PageSummarizer()
click_agent = ClickAgent()
browser_memory = BrowserMemory("happy.db")
browser_safety = BrowserSafety()
browser_agent = BrowserAgent()

# ============ Request/Response Models ============

class CommandRequest(BaseModel):
    """User command request"""
    command: str
    user_id: Optional[str] = "default"

class CommandResponse(BaseModel):
    """Response from HAPPY"""
    success: bool
    message: str
    result: Optional[str] = None
    plan: Optional[dict] = None
    error: Optional[str] = None

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    memory_db: str

# ============ Routes ============

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "memory_db": "happy_memory.db"
    }

@app.post("/command")
async def command_endpoint(request: CommandRequest):
    """
    Frontend command endpoint (alias for /app)
    Accepts commands from React frontend
    """
    return await execute_command(request)

@app.post("/app", response_model=CommandResponse)
async def execute_command(request: CommandRequest):
    """
    Main command execution endpoint
    
    Example commands:
    - "open notepad"
    - "open chrome"
    - "remember my name is Alice"
    - "what is my name"
    - "create folder test"
    """
    
    try:
        command = request.command.strip()
        
        if not command:
            raise HTTPException(status_code=400, detail="Command cannot be empty")
        
        # Parse command with planner
        plan = planner.parse_command(command)
        
        # Execute plan
        result = _execute_plan(plan)
        
        # Log command
        memory_store.log_command(command, result["success"], result.get("message", ""))
        
        return CommandResponse(
            success=result["success"],
            message=result["message"],
            result=result.get("result"),
            plan={
                "goal": plan.goal,
                "command_type": plan.command_type.value,
                "risk_level": plan.risk_level,
                "needs_confirmation": plan.needs_confirmation,
                "parameters": plan.parameters
            },
            error=result.get("error")
        )
        
    except Exception as e:
        return CommandResponse(
            success=False,
            message=f"Error executing command",
            error=str(e)
        )

@app.get("/memory/{key}")
async def get_memory(key: str):
    """Retrieve a memory value"""
    value = memory_store.recall(key)
    
    if value is None:
        raise HTTPException(status_code=404, detail=f"Memory key '{key}' not found")
    
    return {
        "key": key,
        "value": value
    }

@app.get("/memory")
async def get_all_memories():
    """Get all memories"""
    memories = memory_store.recall_all()
    return {
        "count": len(memories),
        "memories": memories
    }

# ============ Browser Routes ============

@app.post("/browser/start")
async def browser_start():
    """Start the browser"""
    import asyncio
    try:
        result = await browser_controller.start()
        return {
            "success": result,
            "message": "Browser started" if result else "Failed to start browser"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error starting browser: {str(e)}"
        }

@app.post("/browser/stop")
async def browser_stop():
    """Stop the browser"""
    import asyncio
    try:
        result = await browser_controller.stop()
        return {
            "success": result,
            "message": "Browser stopped" if result else "Failed to stop browser"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error stopping browser: {str(e)}"
        }

@app.post("/browser/open")
async def browser_open(url: str):
    """Open a URL in the browser"""
    import asyncio
    try:
        result = await browser_controller.open_url(url)
        return result
    except Exception as e:
        return {
            "success": False,
            "message": f"Error opening URL: {str(e)}"
        }

@app.post("/browser/search")
async def browser_search(query: str):
    """Search the web"""
    try:
        result = search_engine.search(query)
        
        # Save query to browser memory
        browser_memory.save_query(query)
        
        return result
    except Exception as e:
        return {
            "success": False,
            "query": query,
            "results": [],
            "message": f"Search error: {str(e)}"
        }

@app.post("/browser/read")
async def browser_read():
    """Read current page content"""
    import asyncio
    try:
        if not browser_controller.current_page:
            return {
                "success": False,
                "message": "No page loaded"
            }
        
        # Get page content
        content = await browser_controller.current_page.content()
        url = await browser_controller.get_page_url()
        
        # Parse with PageReader
        result = page_reader.read(content, url)
        
        # Save to browser memory
        if result.get("success"):
            browser_memory.save_link(url, result.get("title", ""))
        
        return result
    except Exception as e:
        return {
            "success": False,
            "message": f"Error reading page: {str(e)}"
        }

@app.post("/browser/summarize")
async def browser_summarize(length: str = "medium"):
    """Summarize current page"""
    try:
        if not browser_controller.current_page:
            return {
                "success": False,
                "message": "No page loaded"
            }
        
        # Get page content
        import asyncio
        content = await browser_controller.current_page.content()
        url = await browser_controller.get_page_url()
        
        # Parse with PageReader
        page_content = page_reader.read(content, url)
        
        if not page_content.get("success"):
            return page_content
        
        # Summarize
        summary = page_summarizer.summarize(page_content, length)
        
        # Save summary to browser memory
        if summary.get("success"):
            browser_memory.save_summary(
                url,
                summary.get("summary", ""),
                summary.get("title", "")
            )
        
        return summary
    except Exception as e:
        return {
            "success": False,
            "message": f"Error summarizing page: {str(e)}"
        }

@app.post("/browser/click")
async def browser_click(link_text: str = "", url: str = ""):
    """Evaluate and perform a click"""
    try:
        # Assess safety
        assessment = click_agent.safe_click(link_text, url)
        
        return {
            "success": True,
            "safe": assessment["safe"],
            "needs_confirmation": assessment["needs_confirmation"],
            "risk_level": assessment["risk_level"],
            "reason": assessment["reason"],
            "action": assessment["action"]
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error assessing click: {str(e)}"
        }

@app.get("/browser/tabs")
async def browser_tabs():
    """Get all open tabs"""
    import asyncio
    try:
        tabs = await browser_controller.get_tabs()
        return {
            "success": True,
            "tabs": tabs,
            "count": len(tabs)
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error getting tabs: {str(e)}"
        }

@app.post("/browser/tab/switch")
async def browser_switch_tab(tab_id: int):
    """Switch to a specific tab"""
    import asyncio
    try:
        result = await browser_controller.switch_tab(tab_id)
        return result
    except Exception as e:
        return {
            "success": False,
            "message": f"Error switching tab: {str(e)}"
        }

@app.post("/browser/tab/close")
async def browser_close_tab(tab_id: int):
    """Close a specific tab"""
    import asyncio
    try:
        result = await browser_controller.close_tab(tab_id)
        return result
    except Exception as e:
        return {
            "success": False,
            "message": f"Error closing tab: {str(e)}"
        }

@app.get("/browser/history")
async def browser_history(limit: int = 50, search_term: Optional[str] = None):
    """Get browser history"""
    try:
        if search_term:
            results = browser_memory.search_history(search_term)
            return {
                "success": True,
                "history": results,
                "count": len(results)
            }
        else:
            result = browser_memory.get_history(limit)
            return result
    except Exception as e:
        return {
            "success": False,
            "history": [],
            "message": f"Error getting history: {str(e)}"
        }

@app.post("/browser/workflow")
async def browser_workflow(command: str):
    """Plan a browser workflow"""
    try:
        workflow = browser_agent.plan_workflow(command)
        return {
            "success": workflow.get("success", True),
            "workflow": [
                {
                    "order": step.order,
                    "action": step.action,
                    "target": step.target,
                    "description": step.description,
                    "requires_confirmation": step.requires_confirmation
                } for step in workflow.get("workflow", [])
            ],
            "goal": workflow.get("goal", ""),
            "estimated_duration": workflow.get("estimated_duration", ""),
            "total_steps": workflow.get("total_steps", 0)
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error planning workflow: {str(e)}"
        }



def _execute_plan(plan) -> dict:
    """
    Execute a plan and return results
    
    Returns:
        dict with success, message, and optional result
    """
    
    # Unknown command
    if plan.command_type == CommandType.UNKNOWN:
        return {
            "success": False,
            "message": "I don't understand that command. Try 'open notepad', 'remember my name is X', or 'what is my name'?",
            "error": "Unknown command type"
        }
    
    # Execute steps
    for step in plan.steps:
        tool = step.get("tool")
        action = step.get("action")
        input_data = step.get("input")
        
        # APP OPENER
        if tool == "app_opener" and action == "open":
            result = app_opener.open(input_data)
            if not result["success"]:
                return {
                    "success": False,
                    "message": result["message"],
                    "error": result.get("error")
                }
            return {
                "success": True,
                "message": result["message"]
            }
        
        # MEMORY STORE - Remember
        elif tool == "memory_store" and action == "remember":
            key = input_data["key"]
            value = input_data["value"]
            success = memory_store.remember(key, value)
            
            if success:
                return {
                    "success": True,
                    "message": f"I'll remember that {key} is {value}"
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to remember {key}",
                    "error": "Database error"
                }
        
        # MEMORY STORE - Recall
        elif tool == "memory_store" and action == "recall":
            key = input_data
            value = memory_store.recall(key)
            
            if value:
                return {
                    "success": True,
                    "message": f"Your {key} is {value}",
                    "result": value
                }
            else:
                return {
                    "success": False,
                    "message": f"I don't have that in memory yet",
                    "error": f"No memory for '{key}'"
                }
        
        # FILE MANAGER - Create Folder
        elif tool == "file_manager" and action == "create_folder":
            folder_name = input_data
            try:
                os.makedirs(folder_name, exist_ok=True)
                return {
                    "success": True,
                    "message": f"Created folder '{folder_name}'"
                }
            except Exception as e:
                return {
                    "success": False,
                    "message": f"Failed to create folder",
                    "error": str(e)
                }
        
        # BROWSER TOOL - Open Website
        elif tool == "browser_tool" and action == "open_website":
            url = input_data
            result = BrowserTool.open_website_sync(url)
            return {
                "success": result["success"],
                "message": result["message"]
            }
        
        # BROWSER TOOL - Search Web
        elif tool == "browser_tool" and action == "search_web":
            query = input_data
            result = BrowserTool.search_web_sync(query)
            return {
                "success": result["success"],
                "message": result["message"]
            }
        
        # FILE MANAGER - Read File
        elif tool == "file_manager" and action == "read_file":
            file_path = input_data
            result = file_manager.read_file(file_path)
            return {
                "success": result["success"],
                "message": result["message"],
                "result": result.get("content", "")
            }
        
        # FILE MANAGER - Write File
        elif tool == "file_manager" and action == "write_file":
            file_path = input_data["file_path"]
            content = input_data["content"]
            result = file_manager.write_file(file_path, content)
            return {
                "success": result["success"],
                "message": result["message"]
            }
        
        # FILE MANAGER - List Directory
        elif tool == "file_manager" and action == "list_directory":
            dir_path = input_data
            result = file_manager.list_directory(dir_path)
            return {
                "success": result["success"],
                "message": result["message"],
                "result": result.get("items", [])
            }
        
        # FILE MANAGER - Delete File
        elif tool == "file_manager" and action == "delete_file":
            file_path = input_data
            result = file_manager.delete_file(file_path)
            return {
                "success": result["success"],
                "message": result["message"]
            }
        
        # FILE MANAGER - Move File
        elif tool == "file_manager" and action == "move_file":
            source = input_data["source"]
            destination = input_data["destination"]
            result = file_manager.move_file(source, destination)
            return {
                "success": result["success"],
                "message": result["message"]
            }
        
        # FILE MANAGER - Copy File
        elif tool == "file_manager" and action == "copy_file":
            source = input_data["source"]
            destination = input_data["destination"]
            result = file_manager.copy_file(source, destination)
            return {
                "success": result["success"],
                "message": result["message"]
            }
        
        # WINDOWS AUTOMATION - Click Mouse
        elif tool == "windows_automation" and action == "click_at_position":
            x = input_data["x"]
            y = input_data["y"]
            result = windows_automation.click_at_position(x, y)
            return {
                "success": result["success"],
                "message": result["message"]
            }
        
        # WINDOWS AUTOMATION - Type Text
        elif tool == "windows_automation" and action == "type_text":
            text = input_data
            result = windows_automation.type_text(text)
            return {
                "success": result["success"],
                "message": result["message"]
            }
        
        # WINDOWS AUTOMATION - Press Key
        elif tool == "windows_automation" and action == "press_key":
            key = input_data
            result = windows_automation.press_key(key)
            return {
                "success": result["success"],
                "message": result["message"]
            }
        
        # WINDOWS AUTOMATION - Take Screenshot
        elif tool == "windows_automation" and action == "take_screenshot":
            filename = input_data
            result = windows_automation.take_screenshot(filename)
            return {
                "success": result["success"],
                "message": result["message"]
            }
        
        # WINDOWS AUTOMATION - Get Mouse Position
        elif tool == "windows_automation" and action == "get_mouse_position":
            result = windows_automation.get_mouse_position()
            return {
                "success": result["success"],
                "message": result["message"],
                "result": result.get("position", {})
            }
        
        # VOICE OUTPUT - Speak Text
        elif tool == "voice_output" and action == "speak":
            text = input_data
            result = voice_output.speak(text)
            return {
                "success": result["success"],
                "message": result["message"]
            }
        
        # VOICE INPUT - Listen and Transcribe
        elif tool == "voice_input" and action == "listen_and_transcribe":
            result = voice_input.listen_and_transcribe()
            return {
                "success": result["success"],
                "message": result["message"],
                "result": result.get("text", "")
            }
        
        # MEMORY STORE - Semantic Search
        elif tool == "memory_store" and action == "semantic_search":
            query = input_data
            results = memory_store.semantic_search(query, top_k=5)
            
            if results:
                # Format results for display
                memory_list = [f"{m['key']}: {m['value']}" for m in results]
                message = f"Found {len(results)} memories related to '{query}':\n" + "\n".join(memory_list)
                return {
                    "success": True,
                    "message": message,
                    "result": results
                }
            else:
                return {
                    "success": False,
                    "message": f"No memories found related to '{query}'"
                }
    
    return {
        "success": False,
        "message": "No steps to execute",
        "error": "Empty execution plan"
    }

# ============ Startup ============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
