import React, { useState, useEffect, useRef } from 'react';
import { messagingAPI } from '../../services/api';
import './Messaging.css';

function MessageView({ conversation, currentUser, onMessageSent }) {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [fileError, setFileError] = useState('');
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  const MAX_FILE_SIZE = 50 * 1024 * 1024; // 50MB in bytes

  useEffect(() => {
    fetchMessages();
    markAsRead();

    // Poll for new messages every 3 seconds
    const pollInterval = setInterval(() => {
      fetchMessages();
    }, 3000);

    // Cleanup interval on unmount or conversation change
    return () => clearInterval(pollInterval);
  }, [conversation.id]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const fetchMessages = async () => {
    try {
      const response = await messagingAPI.getMessages(conversation.id);
      setMessages(response.data.messages);
    } catch (err) {
      console.error('Failed to load messages:', err);
    } finally {
      setLoading(false);
    }
  };

  const markAsRead = async () => {
    try {
      await messagingAPI.markAsRead(conversation.id);
    } catch (err) {
      console.error('Failed to mark as read:', err);
    }
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    setFileError('');

    if (file) {
      if (file.size > MAX_FILE_SIZE) {
        setFileError('File size must be less than 50MB');
        setSelectedFile(null);
        e.target.value = '';
        return;
      }
      setSelectedFile(file);
    }
  };

  const handleRemoveFile = () => {
    setSelectedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();

    if (!newMessage.trim() && !selectedFile) return;

    setSending(true);
    setFileError('');

    try {
      const response = await messagingAPI.sendMessage(
        conversation.id,
        newMessage,
        selectedFile
      );

      // Add new message to the list
      setMessages([...messages, response.data.data]);
      setNewMessage('');
      setSelectedFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }

      // Notify parent component
      onMessageSent();
    } catch (err) {
      console.error('Failed to send message:', err);
      setFileError(err.response?.data?.error || 'Failed to send message');
    } finally {
      setSending(false);
    }
  };

  const handleDownloadFile = async (filename, originalFilename) => {
    try {
      const response = await messagingAPI.downloadFile(filename);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', originalFilename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Failed to download file:', err);
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  };

  const formatMessageTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const isImageFile = (filename) => {
    const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp'];
    return imageExtensions.some(ext => filename.toLowerCase().endsWith(ext));
  };

  const otherParticipant = conversation.other_participant;

  return (
    <div className="message-view">
      <div className="message-view-header">
        <div className="conversation-avatar">
          {otherParticipant?.username?.charAt(0).toUpperCase() || '?'}
        </div>
        <div>
          <h3>
            {otherParticipant?.full_name ||
              otherParticipant?.username ||
              'Unknown User'}
          </h3>
          <span className="user-type-badge">
            {otherParticipant?.user_type}
          </span>
        </div>
      </div>

      <div className="messages-container">
        {loading ? (
          <div className="loading">Loading messages...</div>
        ) : messages.length === 0 ? (
          <div className="no-messages-placeholder">
            <p>No messages yet. Start the conversation!</p>
          </div>
        ) : (
          <>
            {messages.map((message) => {
              const isSentByMe = message.sender_id === currentUser.id;
              return (
                <div
                  key={message.id}
                  className={`message ${
                    isSentByMe ? 'sent' : 'received'
                  } ${message.is_system_message ? 'system' : ''}`}
                >
                  {message.content && (
                    <div className="message-content">
                      {message.content}
                    </div>
                  )}

                  {message.has_attachment && (
                    <div className="file-attachment">
                      <div className="file-icon">📎</div>
                      <div className="file-info">
                        <div className="file-name">{message.file_name}</div>
                        <div className="file-size">
                          {formatFileSize(message.file_size)}
                        </div>
                      </div>
                      <button
                        className="download-btn"
                        onClick={() =>
                          handleDownloadFile(
                            message.file_path,
                            message.file_name
                          )
                        }
                      >
                        ↓
                      </button>
                    </div>
                  )}

                  <div className="message-time">
                    {formatMessageTime(message.created_at)}
                  </div>
                </div>
              );
            })}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      <form onSubmit={handleSendMessage} className="message-input-form">
        <div className="input-wrapper">
          {selectedFile && (
            <div className="selected-file-preview">
              <span className="file-preview-name">
                📎 {selectedFile.name} ({formatFileSize(selectedFile.size)})
              </span>
              <button
                type="button"
                onClick={handleRemoveFile}
                className="remove-file-btn"
              >
                ✕
              </button>
            </div>
          )}

          {fileError && <div className="file-error">{fileError}</div>}

          <div className="input-row">
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileSelect}
              className="file-input-hidden"
              id="file-input"
            />
            <label htmlFor="file-input" className="file-input-label">
              📎
            </label>

            <input
              type="text"
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              placeholder="Type a message..."
              disabled={sending}
              className="message-input"
            />

            <button
              type="submit"
              disabled={sending || (!newMessage.trim() && !selectedFile)}
              className="send-button"
            >
              {sending ? 'Sending...' : 'Send'}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}

export default MessageView;
