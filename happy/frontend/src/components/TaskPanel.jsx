export default function TaskPanel({ tasks }) {
  return (
    <div className="panel">
      <h2>Tasks</h2>

      {tasks.length === 0 ? (
        <p className="muted">No tasks yet.</p>
      ) : (
        tasks.map((task, index) => (
          <div key={index} className="task-item">
            <span>{task.title}</span>
            <strong>{task.status}</strong>
          </div>
        ))
      )}
    </div>
  );
}
