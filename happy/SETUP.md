# HAPPY Frontend Setup Guide

## Step-by-Step Installation & Testing

This guide walks you through getting HAPPY's React frontend running and connected to the backend.

---

## Prerequisites

- **Python 3.10+** (for backend)
- **Node.js 18+** (for frontend)
- **Windows 10/11**

---

## Step 1: Check Node.js Installation

Open PowerShell and run:

```powershell
node --version
npm --version
```

**Expected output:**
```
v20.x.x (or higher)
10.x.x (or higher)
```

### If Node.js is NOT installed

#### Option A: Using Windows Package Manager (winget)

```powershell
winget install -e --id OpenJS.NodeJS
```

After installation, **close and reopen PowerShell** to refresh environment variables.

#### Option B: Manual Installation

Download from https://nodejs.org/ and install the LTS version.

After installation, **restart your computer** to ensure environment variables are updated.

#### Verify Installation

```powershell
node --version
npm --version
```

---

## Step 2: Verify Backend is Running

In one PowerShell terminal, navigate to backend and start it:

```powershell
cd C:\Users\DELL\Documents\AI\happy\backend
python -m uvicorn main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

Test it:
```powershell
curl http://127.0.0.1:8000/health
```

You should get:
```json
{"status":"healthy","version":"0.1.0","memory_db":"happy_memory.db"}
```

✅ Backend is ready

---

## Step 3: Install Frontend Dependencies

Open a **NEW PowerShell terminal** (keep backend running in the other).

```powershell
cd C:\Users\DELL\Documents\AI\happy\frontend
npm install
```

This may take 1-2 minutes. You should see:
```
added 200+ packages in 1m 45s
```

---

## Step 4: Start Frontend Dev Server

In the same terminal:

```powershell
npm run dev
```

You should see:
```
  VITE v4.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

✅ Frontend is running

---

## Step 5: Open in Browser

Click or open: **http://localhost:5173/**

You should see:
- **HAPPY AI** title at the top
- Dark futuristic dashboard
- Empty chat with "HAPPY is online. Give me a command."
- Command input box at the bottom
- Task and Memory panels on the right

---

## Step 6: Test Connection

Type a command in the input box:

```
open notepad
```

Press **Send** (or press Enter).

You should see:
1. Your message appears in chat: "YOU: open notepad"
2. Notepad opens on your PC
3. Response appears: "HAPPY: HAPPY received command: open notepad"

### If it works:
✅ **Full stack is connected!**

### If it doesn't work:

**Error**: "Backend connection failed..."

**Solutions:**
1. Check backend is still running (should say "Application startup complete")
2. Check port 8000 is not blocked
3. Try a simple command like `hello` to see error details
4. Check browser console (F12) for CORS errors

---

## Step 7: Test More Commands

### Remember a fact

```
remember my name is Alice
```

**Response:** "I'll remember that name is alice"

### Recall the fact

```
what is my name
```

**Response:** "Your name is alice"

### Create a folder

```
create folder HAPPY_TEST
```

**Response:** "Created folder 'happy_test'"

Check your current directory - you'll see a new folder!

### View all memories

In browser, visit: **http://localhost:8000/memory**

You should see all saved memories as JSON.

---

## Step 8: View Task History

In the **Tasks** panel on the right, you'll see all completed commands:

```
open notepad          done
remember my name... done
create folder HA...  done
```

---

## Step 9: (Optional) Close & Restart

To stop everything:

**Backend terminal:** Press `Ctrl+C`  
**Frontend terminal:** Press `Ctrl+C`

To start again:

**Terminal 1 (Backend):**
```powershell
cd C:\Users\DELL\Documents\AI\happy\backend
python -m uvicorn main:app --reload
```

**Terminal 2 (Frontend):**
```powershell
cd C:\Users\DELL\Documents\AI\happy\frontend
npm run dev
```

Then open `http://localhost:5173/`

---

## Troubleshooting

### Problem: "npm: command not found"

**Solution:**
- Restart PowerShell/terminal completely
- Or use full path: `C:\Program Files\nodejs\npm install`

### Problem: Port 5173 already in use

**Solution:**
```powershell
npm run dev -- --port 5174
```

Then open `http://localhost:5174/`

### Problem: Port 8000 already in use

**Solution:**
```powershell
python -m uvicorn main:app --reload --port 8001
```

Then update frontend API: `src/api/happyApi.js` line:
```javascript
const API_BASE_URL = "http://localhost:8001";
```

### Problem: "Cannot find module 'react'"

**Solution:**
```powershell
cd C:\Users\DELL\Documents\AI\happy\frontend
rm -r node_modules
npm cache clean --force
npm install
npm run dev
```

### Problem: No network request from frontend

**Check:**
1. Browser console (F12 → Console tab)
2. Look for red errors
3. Check if `http://localhost:8000/health` works in curl
4. Restart both servers

### Problem: Backend shows CORS error

The backend should already have CORS enabled. If you get CORS errors:

In `backend/main.py`, check:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

If it's missing, add it before `@app.get("/health")`.

---

## What You've Built

✅ **HAPPY V0.1 Full Stack:**

| Component | Status | Location |
|-----------|--------|----------|
| Backend Server | Running | `http://localhost:8000` |
| Frontend UI | Running | `http://localhost:5173` |
| API Connection | Working | POST `/command` |
| Chat Interface | Working | Chat box |
| Command Execution | Working | Open apps, remember facts |
| Memory Storage | Working | SQLite database |

---

## Next Steps

Now that the frontend is running:

1. **Explore the UI** - Try different commands
2. **Check memory** - Visit http://localhost:8000/memory
3. **Read code** - Look at `frontend/src/components/` and `backend/main.py`
4. **Add more tools** - Extend `backend/tools/` for more capabilities
5. **Customize UI** - Edit `frontend/src/styles.css` for your colors
6. **Add voice** - Implement speech input (Phase 3)

---

## Quick Commands Reference

### Backend Setup
```powershell
cd C:\Users\DELL\Documents\AI\happy\backend
python -m uvicorn main:app --reload
```

### Frontend Setup  
```powershell
cd C:\Users\DELL\Documents\AI\happy\frontend
npm install
npm run dev
```

### Test Backend
```powershell
curl http://127.0.0.1:8000/health
```

### Test Full Stack
- Open http://localhost:5173
- Type: `open notepad`
- Press Send
- Watch Notepad open

---

## Support

- **Backend issues?** Check `backend/README.md`
- **Frontend issues?** Check `frontend/README.md`
- **Full setup?** Read main `README.md`

---

**Version**: 0.1.0  
**Status**: Phase 1 - Full Stack Setup ✅

You now have HAPPY running. Make it yours.
