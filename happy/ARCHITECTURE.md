# HAPPY Architecture Diagram

## Full Stack Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER (You)                               │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ↓
    ┌──────────────────────────────────────┐
    │   HAPPY FRONTEND (React + Vite)       │
    │   http://localhost:5173               │
    ├──────────────────────────────────────┤
    │ ┌────────────────────────────────┐   │
    │ │    Dashboard Component         │   │
    │ │ ┌──────────────────────────┐   │   │
    │ │ │   Chat Interface         │   │   │
    │ │ │ YOU: open notepad       │   │   │
    │ │ │ HAPPY: Opened notepad   │   │   │
    │ │ └──────────────────────────┘   │   │
    │ │ ┌──────────────────────────┐   │   │
    │ │ │ Command Input [      ][→]│   │   │
    │ │ └──────────────────────────┘   │   │
    │ └──────────────┬──────────────────┘   │
    │ ┌──────────────────────────────────┐  │
    │ │   Sidebar    │   Task Panel        │  │
    │ │   - Brain    │   - Tasks list      │  │
    │ │   - Commands │   - Status          │  │
    │ │   - Voice    │   ┌──────────────┐  │  │
    │ │   - Safety   │   │ Memory Panel │  │  │
    │ │   - Settings │   │ - Memories   │  │  │
    │ │              │   └──────────────┘  │  │
    │ └──────────────────────────────────┘  │
    └──────────────────┬───────────────────┘
                       │
        HTTP POST /command (JSON)
        { "command": "open notepad" }
                       │
                       ↓
    ┌──────────────────────────────────────┐
    │   HAPPY BACKEND (FastAPI)             │
    │   http://localhost:8000               │
    ├──────────────────────────────────────┤
    │ ┌────────────────────────────────┐   │
    │ │  main.py (Request Handler)      │   │
    │ │  POST /command                 │   │
    │ └────────────────┬─────────────────┘   │
    │                  │                      │
    │                  ↓                      │
    │ ┌────────────────────────────────┐   │
    │ │  brain/planner.py              │   │
    │ │  - Parse command               │   │
    │ │  - Detect type (open_app)      │   │
    │ │  - Create plan                 │   │
    │ └────────────────┬─────────────────┘   │
    │                  │                      │
    │                  ↓                      │
    │ ┌────────────────────────────────┐   │
    │ │  Execution Engine               │   │
    │ │  - Read plan steps              │   │
    │ │  - Route to tools               │   │
    │ │  - Execute commands             │   │
    │ └───────────┬────────┬────────┬────┘   │
    │             │        │        │         │
    │   ┌─────────▼┐  ┌────▼──┐ ┌──▼────┐   │
    │   │ AppOpener│  │Memory │ │ File  │   │
    │   │ - Open   │  │ Store │ │Mgr   │   │
    │   │   apps   │  │ SQL   │ │ - Cr  │   │
    │   │ - Launch │  │ Lite  │ │   eate│   │
    │   │ - Execute│  │ DB    │ │ - Del │   │
    │   └─────┬────┘  └───┬───┘ └──┬───┘   │
    │         │           │        │        │
    └──────────┼───────────┼────────┼────────┘
              │           │        │
              ↓           ↓        ↓
         [Notepad]   [SQLite DB]  [Folders]
         [Chrome]    [memories]    [Files]
         [VS Code]   [history]
         [Calc]
                       │
                       │ HTTP Response (JSON)
                       ↓
    ┌──────────────────────────────────────┐
    │   Frontend Display                     │
    │   - Update chat with response          │
    │   - Add task to list                   │
    │   - Save memory if applicable          │
    │   - Show confirmation modal if needed  │
    └──────────────────────────────────────┘
                       │
                       ↓
                   USER SEES RESULT
                (App opens, memory saved, etc)
```

---

## Component Breakdown

### 1. Frontend Layer (React)

```
src/
├── pages/
│   └── Dashboard.jsx           # Main container, state management
├── components/
│   ├── Sidebar.jsx             # Navigation menu
│   ├── ChatBox.jsx             # Messages display
│   ├── CommandInput.jsx        # Input form + send button
│   ├── TaskPanel.jsx           # Task history
│   ├── MemoryPanel.jsx         # Saved memories
│   └── SafetyModal.jsx         # Confirmation popup
├── api/
│   └── happyApi.js             # Axios HTTP client
├── App.jsx                     # Root component
├── main.jsx                    # React entry point
└── styles.css                  # All styling
```

### 2. Backend Layer (FastAPI)

```
backend/
├── main.py                     # Server + routes
├── brain/
│   └── planner.py              # Command parsing logic
├── tools/
│   └── app_opener.py           # App launching
└── memory/
    └── memory_store.py         # SQLite operations
```

### 3. Database Layer

```
happy_memory.db (SQLite)
├── memories table
│   ├── key (TEXT)
│   ├── value (TEXT)
│   ├── category (TEXT)
│   └── timestamps
└── command_history table
    ├── command (TEXT)
    ├── success (BOOLEAN)
    ├── result (TEXT)
    └── timestamp
```

---

## Data Flow Example: "open notepad"

### Step 1: User Input
```
Frontend → User types "open notepad" in input box
```

### Step 2: API Request
```
Frontend → POST /command
{
  "command": "open notepad",
  "user_id": "default"
}
```

### Step 3: Backend Processing
```
main.py → Routes to execute_command()
          ↓
planner.py → Parses "open notepad"
           → Detects CommandType.OPEN_APP
           → Creates plan with AppOpener tool
           ↓
main.py → _execute_plan()
        → Finds "app_opener" tool
        → Calls app_opener.open("notepad")
        → Returns result
```

### Step 4: Tool Execution
```
AppOpener.open("notepad")
↓
subprocess.Popen("notepad.exe")
↓
Notepad launches on user's PC
```

### Step 5: Response
```
Backend → Returns JSON
{
  "success": true,
  "message": "Opened notepad",
  "plan": {...}
}
```

### Step 6: Frontend Update
```
Frontend → Parse response
         → Add user message to chat
         → Add HAPPY response to chat
         → Add task to TaskPanel
         → Display in UI
```

### Step 7: User Sees Result
```
Chat shows:
YOU: open notepad
HAPPY: Opened notepad

Task shows:
open notepad    done

Real world: Notepad is open on PC
```

---

## Communication Protocols

### Frontend → Backend

**HTTP POST /command**
```json
{
  "command": "string",
  "user_id": "optional"
}
```

### Backend → Frontend

**HTTP 200 Response**
```json
{
  "success": boolean,
  "message": "string",
  "result": "string or null",
  "plan": {
    "goal": "string",
    "command_type": "string",
    "risk_level": "low|medium|high",
    "needs_confirmation": boolean,
    "parameters": {}
  },
  "error": "string or null"
}
```

---

## Execution Flow Diagram

```
┌─────────────────┐
│   User Input    │
│  "open notepad" │
└────────┬────────┘
         │
         ↓
┌─────────────────────────────┐
│  CommandInput Component      │
│  - Get user text            │
│  - Call onSend(command)     │
│  - Clear input box          │
└────────┬────────────────────┘
         │
         ↓
┌─────────────────────────────┐
│  Dashboard (state update)    │
│  - Add user message to msgs │
│  - Set loading = true       │
└────────┬────────────────────┘
         │
         ↓
┌─────────────────────────────┐
│  happyApi.sendCommand()     │
│  - axios.post(/command)     │
│  - Wait for response        │
└────────┬────────────────────┘
         │
         ↓
     ┌───────────────────────────────────────────┐
     │    NETWORK REQUEST TO BACKEND              │
     │    POST http://localhost:8000/command      │
     │    { "command": "open notepad" }           │
     └───────────┬───────────────────────────────┘
                 │
                 ↓
     ┌───────────────────────────────────────────┐
     │    BACKEND PROCESSING (see above)          │
     │    Notepad opens on user's PC!             │
     └───────────┬───────────────────────────────┘
                 │
                 ↓
     ┌───────────────────────────────────────────┐
     │    NETWORK RESPONSE FROM BACKEND           │
     │    { "success": true, ... }                │
     └───────────┬───────────────────────────────┘
         │
         ↓
┌─────────────────────────────┐
│  Handle Response            │
│  - Get result JSON          │
│  - Add response to messages │
│  - Add task to tasks list   │
│  - Update Memory panel      │
│  - Set loading = false      │
└────────┬────────────────────┘
         │
         ↓
┌─────────────────────────────┐
│  React Re-render            │
│  - ChatBox updates          │
│  - Shows new messages       │
│  - TaskPanel updates        │
│  - Shows new task           │
└────────┬────────────────────┘
         │
         ↓
┌─────────────────────────────┐
│   User Sees Results         │
│   - Chat updated            │
│   - Task listed             │
│   - Notepad is open         │
└─────────────────────────────┘
```

---

## The Beautiful Thing

All of this happens in **milliseconds**.

The whole chain:
1. User types
2. Frontend sends request
3. Backend parses and executes
4. Tool (AppOpener) runs
5. Response comes back
6. Frontend updates
7. User sees result

Is **instant** (under 500ms for most commands).

That's the magic of a well-designed system.

---

**Architecture Version**: 0.1.0  
**Philosophy**: Keep it simple. Make it work. Make it fast.
