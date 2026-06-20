import { useState } from "react";
import { Send, Mic, MicOff } from "lucide-react";

export default function CommandInput({ onSend, loading }) {
  const [command, setCommand] = useState("");
  const [isListening, setIsListening] = useState(false);

  function handleSubmit(event) {
    event.preventDefault();

    if (!command.trim()) return;

    onSend(command);
    setCommand("");
  }

  async function handleVoiceInput() {
    if (isListening) {
      // Stop listening
      setIsListening(false);
      onSend("listen voice"); // This will trigger voice input on backend
    } else {
      // Start listening
      setIsListening(true);
      setCommand("🎤 Listening...");
      onSend("listen voice");
    }
  }

  return (
    <form className="command-input" onSubmit={handleSubmit}>
      <button
        type="button"
        className={`mic-btn ${isListening ? 'listening' : ''}`}
        onClick={handleVoiceInput}
        disabled={loading}
      >
        {isListening ? <MicOff size={20} /> : <Mic size={20} />}
      </button>

      <input
        value={command}
        onChange={(event) => setCommand(event.target.value)}
        placeholder="Command HAPPY... example: open notepad"
        disabled={loading || isListening}
      />

      <button type="submit" className="send-btn" disabled={loading || isListening}>
        <Send size={20} />
      </button>
    </form>
  );
}
