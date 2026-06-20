import { useState } from "react";
import Sidebar from "../components/Sidebar.jsx";
import ChatBox from "../components/ChatBox.jsx";
import CommandInput from "../components/CommandInput.jsx";
import TaskPanel from "../components/TaskPanel.jsx";
import MemoryPanel from "../components/MemoryPanel.jsx";
import SafetyModal from "../components/SafetyModal.jsx";
import { sendCommand } from "../api/happyApi.js";

export default function Dashboard() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "HAPPY is online. Give me a command.",
    },
  ]);

  const [tasks, setTasks] = useState([]);
  const [memories, setMemories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [safetyRequest, setSafetyRequest] = useState(null);

  async function handleCommand(command) {
    if (!command.trim()) return;

    const userMessage = {
      role: "user",
      text: command,
    };

    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const result = await sendCommand(command);

      if (result.needs_confirmation) {
        setSafetyRequest(result);
        setLoading(false);
        return;
      }

      // Handle voice transcription
      if (command.toLowerCase().includes("listen voice") && result.result) {
        // Voice transcription received - update the input with transcribed text
        // This is a bit hacky, but we'll treat the transcribed text as a new command
        const transcribedText = result.result;
        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            text: `Heard: "${transcribedText}"`,
          },
        ]);

        // Automatically execute the transcribed command
        if (transcribedText && transcribedText !== command) {
          setTimeout(() => handleCommand(transcribedText), 500);
          setLoading(false);
          return;
        }
      }

      const assistantMessage = {
        role: "assistant",
        text: result.message || "Command completed.",
      };

      setMessages((prev) => [...prev, assistantMessage]);

      setTasks((prev) => [
        {
          title: command,
          status: result.status || "done",
        },
        ...prev,
      ]);

      if (result.memory) {
        setMemories((prev) => [result.memory, ...prev]);
      }
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "Backend connection failed. Check if FastAPI is running on http://localhost:8000",
        },
      ]);
    }

    setLoading(false);
  }

  function confirmSafetyAction() {
    setMessages((prev) => [
      ...prev,
      {
        role: "assistant",
        text: "Safety action confirmed. Executing command.",
      },
    ]);

    setSafetyRequest(null);
  }

  function cancelSafetyAction() {
    setMessages((prev) => [
      ...prev,
      {
        role: "assistant",
        text: "Action cancelled. Good call if you were unsure.",
      },
    ]);

    setSafetyRequest(null);
  }

  return (
    <div className="app-shell">
      <Sidebar />

      <main className="main-area">
        <header className="topbar">
          <div>
            <h1>HAPPY AI</h1>
            <p>Windows automation assistant</p>
          </div>

          <div className="status-pill">
            <span className="status-dot"></span>
            ONLINE
          </div>
        </header>

        <section className="dashboard-grid">
          <div className="chat-section">
            <ChatBox messages={messages} loading={loading} />
            <CommandInput onSend={handleCommand} loading={loading} />
          </div>

          <aside className="right-panel">
            <TaskPanel tasks={tasks} />
            <MemoryPanel memories={memories} />
          </aside>
        </section>
      </main>

      {safetyRequest && (
        <SafetyModal
          request={safetyRequest}
          onConfirm={confirmSafetyAction}
          onCancel={cancelSafetyAction}
        />
      )}
    </div>
  );
}
