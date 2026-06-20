# HAPPY V0.1 - Personal Windows AI Automation Assistant

Your personal AI assistant that **thinks, remembers, and controls your PC safely**.

## Current Phase: Phase 1 - Full Stack (Backend + Frontend)

**Status**: 🚀 **Ready to Connect**

### What Works

**Backend** ✅
- FastAPI server running on `http://localhost:8000`
- Accept text commands via `/app` and `/command` endpoints
- Open Windows applications
- Remember and recall facts in SQLite
- Parse intent with simple planner
- Execute tools safely
- CORS enabled for frontend

**Frontend** ✅ (Ready to install)
- React + Vite dashboard UI
- Chat interface
- Command input with send button
- Task & memory panels
- Safety confirmation modal
- Connected to backend API

---

## 🚀 Quick Start (Both Backend + Frontend)

### Terminal 1: Backend Server

```bash
cd c:\Users\DELL\Documents\AI\happy\backend
python -m uvicorn main:app --reload
```

Opens at: `http://127.0.0.1:8000`

### Terminal 2: Frontend Server

**First time only** - Install dependencies:
```bash
cd c:\Users\DELL\Documents\AI\happy\frontend
npm install
```

Then start:
```bash
npm run dev
```

Opens at: `http://localhost:5173`

---

## ✨ Test HAPPY

### 1. Open Frontend
Go to `http://localhost:5173` in your browser

### 2. Type a Command
```
open notepad
```

### 3. Watch It Work
- Frontend sends to backend
- Backend opens Notepad
- Frontend displays result
- **Connection successful!**

---

### Supported Commands (V0.1)

```
open notepad
open calculator
open vscode
remember my name is Alice
what is my name?
create folder test
```

---

## Direct API Tests (if no frontend)

### Health Check
```bash
curl http://127.0.0.1:8000/health
```

### Send Command
```bash
curl -X POST http://127.0.0.1:8000/command \
  -H "Content-Type: application/json" \
  -d '{"command": "open notepad"}'
```

---

## 📁 Project Structure

```
happy/
├─ backend/                 # FastAPI server
│  ├─ main.py              # Server entry point
│  ├─ requirements.txt      # Python dependencies
│  ├─ brain/
│  │  └─ planner.py        # Command parser
│  ├─ tools/
│  │  └─ app_opener.py     # App launcher
│  └─ memory/
│     └─ memory_store.py   # SQLite database
│
├─ frontend/               # React Vite app
│  ├─ package.json        # npm dependencies
│  ├─ vite.config.js      # Vite configuration
│  ├─ index.html          # HTML entry point
│  ├─ src/
│  │  ├─ main.jsx         # React entry
│  │  ├─ App.jsx          # App wrapper
│  │  ├─ styles.css       # Styling
│  │  ├─ api/
│  │  │  └─ happyApi.js   # Backend client
│  │  ├─ components/      # React components
│  │  │  ├─ Sidebar.jsx
│  │  │  ├─ ChatBox.jsx
│  │  │  ├─ CommandInput.jsx
│  │  │  ├─ TaskPanel.jsx
│  │  │  ├─ MemoryPanel.jsx
│  │  │  └─ SafetyModal.jsx
│  │  └─ pages/
│  │     └─ Dashboard.jsx  # Main page
│  └─ README.md           # Frontend docs
│
├─ README.md              # This file
├─ .gitignore            # Git ignore rules
└─ test_happy.py         # Backend test script
```

---

## 🧠 How It Works

### Architecture

```
[React Frontend]
       ↓ (HTTP POST /command)
[FastAPI Backend]
       ↓ (Parse with Planner)
[Tool Execution]
  ├─ AppOpener (launch apps)
  ├─ MemoryStore (save/recall facts)
  ├─ FileManager (create folders)
  └─ More tools coming...
       ↓ (Return result)
[Frontend displays response]
```

### Command Flow

1. **User types**: "open notepad"
2. **Frontend sends**: POST to `/command` with command text
3. **Backend receives**: Command request
4. **Planner analyzes**: Detects command type (open_app)
5. **Tools execute**: AppOpener.open("notepad")
6. **Response returned**: `{ "success": true, "message": "Opened notepad" }`
7. **Frontend displays**: Chat message + task added

---

## 🔌 API Endpoints

### Frontend Routes

```
POST /command
├─ Request: { "command": "open notepad" }
└─ Response: { "success": true, "message": "..." }

GET /health
└─ Response: { "status": "healthy", "version": "0.1.0" }

POST /app (same as /command, for testing)

GET /memory
└─ Response: { "count": 2, "memories": { "name": "Alice" } }

GET /memory/{key}
└─ Response: { "key": "name", "value": "Alice" }
```

---

## 🛠️ Setup Instructions

### Requirements
- Python 3.10+
- Node.js 18+
- Windows 10/11

### Backend Setup

```bash
# Navigate to backend
cd happy/backend

# Install Python packages
pip install -r requirements.txt

# Run server
python -m uvicorn main:app --reload

# Backend runs on http://localhost:8000
```

### Frontend Setup

```bash
# Navigate to frontend
cd happy/frontend

# Install npm packages (first time only)
npm install

# Start dev server
npm run dev

# Frontend runs on http://localhost:5173
```

---

## 🧪 Testing

### Test Backend Only

```bash
# Run test script
python test_happy.py

# Or use curl
curl http://localhost:8000/health
```

### Test Full Stack

1. Open `http://localhost:5173` in browser
2. Type command: `open notepad`
3. See message appear in chat
4. Notepad opens
5. ✅ Success!

---

## 🎨 Frontend Features (V0.1)

- ✅ Dark futuristic theme with gradients
- ✅ Real-time chat interface
- ✅ Command input with send button
- ✅ Voice button placeholder
- ✅ Task history panel
- ✅ Memory storage display
- ✅ Safety confirmation modal
- ✅ Responsive design (mobile/tablet)

---

## 🔐 Safety Features

HAPPY has built-in safety:
- Commands are parsed before execution
- Dangerous operations require confirmation
- No credentials stored
- No internet by default (local first)
- Easy to sandbox/limit capabilities

---

## 🚀 Next Steps (Phase 2)

After V0.1 frontend-backend connection works:

1. **Browser Automation**
   - Open websites (Chrome, Firefox, Edge)
   - Search Google
   - Click buttons and links

2. **File Management**
   - Create/delete files
   - Search files by name
   - Open files in apps

3. **Windows Automation**
   - Click mouse
   - Type text
   - Take screenshots
   - Control keyboard

4. **Voice Assistant**
   - Speech-to-text input
   - Text-to-speech output
   - Voice command loop

5. **Advanced Memory**
   - Vector embeddings (FAISS)
   - Semantic search
   - Context understanding

6. **Desktop App**
   - Wrap in Tauri/Electron
   - Windows native app
   - System tray integration

7. **Local LLM**
   - Mistral 7B integration
   - Ollama support
   - No cloud dependency

---

## 🐛 Troubleshooting

### Frontend Won't Connect to Backend
```
Error: "Backend connection failed"
```

**Solutions:**
1. Check backend is running: `http://localhost:8000/health`
2. Check CORS enabled in backend
3. Restart frontend dev server
4. Check no port conflicts

### npm install fails
```bash
npm cache clean --force
npm install
```

### Port 5173 already in use
```bash
npm run dev -- --port 5174
```

### Port 8000 already in use
```bash
python -m uvicorn main:app --reload --port 8001
```

### Python module not found
```bash
cd happy/backend
pip install -r requirements.txt
```

### Commands not working
1. Check backend planner parsing
2. Check tool execution
3. Check error message in response
4. Run `python test_happy.py` for diagnostics

---

## 📚 Documentation

- **Backend**: [backend/README.md](backend/README.md)
- **Frontend**: [frontend/README.md](frontend/README.md)
- **Test Script**: [test_happy.py](test_happy.py)

---

## 🎯 Design Philosophy

**Brick by Brick, Not Hype Dust**

We're not building AGI. We're building:
1. One working ability at a time
2. From the foundation up
3. With safety first
4. That actually runs on your PC

No:
- Fake features
- Broken AI
- Bloated frameworks
- Vaporware promises

Yes:
- Simple, working code
- Clear separation of concerns
- Easy to test
- Easy to extend

**HAPPY should be:**
- **Helpful** - Does what you ask
- **Autonomous** - Works without asking every step
- **Progressive** - Learns from commands
- **Personalized** - Remembers your preferences
- **Yoked** (accountable) - Won't delete your files without confirmation

---

## 📊 Phase 1 Completion Status

### ✅ Completed
- FastAPI backend server
- Command parsing with planner
- App opener tool
- SQLite memory store
- CORS setup
- React Vite frontend
- Chat interface
- Command input
- Task & memory panels
- Safety modal
- Frontend-backend API connection

### ⏳ In Progress
- Full integration testing
- npm installation documentation

### ⏸️ TODO (Phase 2+)
- Browser automation
- File management
- Windows control
- Voice interface
- Advanced memory
- Desktop UI
- Local LLM

---

**Version**: 0.1.0  
**Status**: Phase 1 - Full Stack Working ✅

Built with ❤️ for Windows automation

HAPPY is alive. Now watch it learn.
