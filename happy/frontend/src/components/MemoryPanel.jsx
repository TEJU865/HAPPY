export default function MemoryPanel({ memories }) {
  return (
    <div className="panel">
      <h2>Memory</h2>

      {memories.length === 0 ? (
        <p className="muted">No memories saved yet.</p>
      ) : (
        memories.map((memory, index) => (
          <div key={index} className="memory-item">
            {typeof memory === "string" ? memory : JSON.stringify(memory)}
          </div>
        ))
      )}
    </div>
  );
}
