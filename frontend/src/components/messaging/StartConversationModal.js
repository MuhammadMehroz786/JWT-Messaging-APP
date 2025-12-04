import React, { useState, useEffect } from 'react';
import { usersAPI, messagingAPI } from '../../services/api';
import './StartConversationModal.css';

function StartConversationModal({ onClose, onConversationStarted }) {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [startingConversation, setStartingConversation] = useState(null);

  useEffect(() => {
    fetchStudents();
  }, []);

  const fetchStudents = async () => {
    try {
      const response = await usersAPI.getStudents();
      setStudents(response.data.students);
    } catch (err) {
      setError('Failed to load students');
    } finally {
      setLoading(false);
    }
  };

  const handleStartConversation = async (studentId) => {
    setStartingConversation(studentId);
    setError('');

    try {
      const response = await messagingAPI.startConversation(studentId);

      // Close modal and notify parent
      onConversationStarted(response.data.conversation);
      onClose();
    } catch (err) {
      setError(
        err.response?.data?.error || 'Failed to start conversation'
      );
    } finally {
      setStartingConversation(null);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Find Students</h2>
          <button className="close-button" onClick={onClose}>
            ×
          </button>
        </div>

        <div className="modal-body">
          {error && <div className="error-message">{error}</div>}

          {loading ? (
            <div className="loading">Loading students...</div>
          ) : students.length === 0 ? (
            <div className="no-students">
              <p>No students registered yet.</p>
            </div>
          ) : (
            <div className="students-list">
              {students.map((student) => (
                <div key={student.id} className="student-item">
                  <div className="student-avatar">
                    {student.username?.charAt(0).toUpperCase() || 'S'}
                  </div>
                  <div className="student-info">
                    <div className="student-name">
                      {student.full_name || student.username}
                    </div>
                    <div className="student-email">{student.email}</div>
                  </div>
                  <button
                    onClick={() => handleStartConversation(student.id)}
                    disabled={startingConversation === student.id}
                    className="message-button"
                  >
                    {startingConversation === student.id
                      ? 'Starting...'
                      : 'Message'}
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default StartConversationModal;
