import { Brain, Mic, Settings, Terminal, Shield } from "lucide-react";

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="logo">H</div>

      <nav>
        <button className="nav-btn active">
          <Brain size={20} />
          Brain
        </button>

        <button className="nav-btn">
          <Terminal size={20} />
          Commands
        </button>

        <button className="nav-btn">
          <Mic size={20} />
          Voice
        </button>

        <button className="nav-btn">
          <Shield size={20} />
          Safety
        </button>

        <button className="nav-btn">
          <Settings size={20} />
          Settings
        </button>
      </nav>
    </aside>
  );
}
