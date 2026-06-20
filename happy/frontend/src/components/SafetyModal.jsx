export default function SafetyModal({ request, onConfirm, onCancel }) {
  return (
    <div className="modal-backdrop">
      <div className="safety-modal">
        <h2>Safety Confirmation</h2>

        <p>
          HAPPY wants to perform an action that needs your permission.
        </p>

        <div className="danger-box">
          {request.message || "This action may affect your system."}
        </div>

        <div className="modal-actions">
          <button className="cancel-btn" onClick={onCancel}>
            Cancel
          </button>

          <button className="confirm-btn" onClick={onConfirm}>
            Confirm
          </button>
        </div>
      </div>
    </div>
  );
}
