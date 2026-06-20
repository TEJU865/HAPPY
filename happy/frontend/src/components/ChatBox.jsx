export default function ChatBox({ messages, loading }) {
  return (
    <div className="chat-box">
      {messages.map((message, index) => (
        <div
          key={index}
          className={`message ${
            message.role === "user" ? "user-message" : "assistant-message"
          }`}
        >
          <div className="message-role">
            {message.role === "user" ? "YOU" : "HAPPY"}
          </div>
          <div className="message-text">{message.text}</div>
        </div>
      ))}

      {loading && (
        <div className="message assistant-message">
          <div className="message-role">HAPPY</div>
          <div className="message-text">Thinking...</div>
        </div>
      )}
    </div>
  );
}
