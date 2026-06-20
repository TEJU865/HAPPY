# HAPPY Frontend V0.1

The control room for HAPPY AI automation assistant.

**Status**: 🚀 Ready to build

## Quick Start

### 1. Install Node.js (if not already installed)

Download from https://nodejs.org/ or use:
```bash
winget install -e --id OpenJS.NodeJS
```

Then restart your terminal to refresh environment variables.

### 2. Install Dependencies

```bash
cd c:\Users\DELL\Documents\AI\happy\frontend
npm install
```

### 3. Start Development Server

```bash
npm run dev
```

Opens at: `http://localhost:5173`

### 4. Make Sure Backend is Running

In a separate terminal:

```bash
cd c:\Users\DELL\Documents\AI\happy\backend
python -m uvicorn main:app --reload
```

Backend runs at: `http://localhost:8000`

---

## Architecture

### Components

- **Dashboard.jsx** - Main page layout, state management
- **Sidebar.jsx** - Navigation menu
- **ChatBox.jsx** - Message display
- **CommandInput.jsx** - Command input form with mic button
- **TaskPanel.jsx** - Shows completed tasks
- **MemoryPanel.jsx** - Shows saved memories
- **SafetyModal.jsx** - Safety confirmation popup

### API

- `src/api/happyApi.js` - Axios client for backend communication

### Styling

- `src/styles.css` - Futuristic dark theme with gradients

---

## How It Works

```
User types command → Frontend sends to /command endpoint → 
Backend executes command → Frontend shows result
```

### Example Flow

1. User types: `open notepad`
2. Frontend sends POST to `http://localhost:8000/command`
3. Backend receives, parses, executes
4. Backend returns: `{ "message": "Opened notepad", "status": "done" }`
5. Frontend displays response in chat

---

## Features (V0.1)

✅ Chat interface
✅ Command input with send button
✅ Voice button placeholder (mic icon)
✅ Task tracking panel
✅ Memory storage panel
✅ Safety confirmation popup
✅ Backend API connection
✅ Futuristic AI dashboard design

---

## Build for Production

```bash
npm run build
```

Creates optimized build in `dist/` folder.

---

## Project Structure

```
frontend/
├── public/               # Static assets
├── src/
│   ├── api/
│   │   └── happyApi.js  # Backend API client
│   ├── components/       # React components
│   │   ├── Sidebar.jsx
│   │   ├── ChatBox.jsx
│   │   ├── CommandInput.jsx
│   │   ├── TaskPanel.jsx
│   │   ├── MemoryPanel.jsx
│   │   └── SafetyModal.jsx
│   ├── pages/
│   │   └── Dashboard.jsx # Main page
│   ├── App.jsx          # App wrapper
│   ├── main.jsx         # React entry point
│   └── styles.css       # All styling
├── index.html           # HTML entry point
├── package.json         # Dependencies
├── vite.config.js       # Vite configuration
└── .gitignore           # Git ignore rules
```

---

## Troubleshooting

### npm install fails
```bash
npm cache clean --force
npm install
```

### Port 5173 already in use?
```bash
npm run dev -- --port 5174
```

### Backend connection fails
1. Make sure backend is running on `http://localhost:8000`
2. Check backend output for errors
3. Verify CORS is enabled in backend

### Hot reload not working
Try deleting `node_modules` and reinstalling:
```bash
rm -r node_modules
npm install
npm run dev
```

---

## Next Steps

After frontend-backend connection works:
1. Connect real commands to backend
2. Display command results properly
3. Add voice input/output
4. Wrap in Electron/Tauri for desktop app
5. Add advanced memory features

---

## Dependencies

- **React** - UI framework
- **Vite** - Build tool
- **Axios** - HTTP client
- **lucide-react** - Icon library

---

**Version**: 0.1.0  
**Status**: Phase 1 - Frontend
