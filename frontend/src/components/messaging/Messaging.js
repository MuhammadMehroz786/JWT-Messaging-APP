import React, { useState, useEffect } from 'react';
import { messagingAPI } from '../../services/api';
import { getUser } from '../../utils/auth';
import ConversationList from './ConversationList';
import MessageView from './MessageView';
import StartConversationModal from './StartConversationModal';
import './Messaging.css';

function Messaging() {
  const [conversations, setConversations] = useState([]);
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showStartConversationModal, setShowStartConversationModal] = useState(false);
  const currentUser = getUser();

  useEffect(() => {
    fetchConversations();

    // Poll for conversation updates every 5 seconds
    const pollInterval = setInterval(() => {
      fetchConversations();
    }, 5000);

    // Cleanup interval on unmount
    return () => clearInterval(pollInterval);
  }, []);

  const fetchConversations = async () => {
    try {
      const response = await messagingAPI.getConversations();
      setConversations(response.data.conversations);
    } catch (err) {
      setError('Failed to load conversations');
    } finally {
      setLoading(false);
    }
  };

  const handleConversationSelect = (conversation) => {
    setSelectedConversation(conversation);
  };

  const handleMessageSent = () => {
    // Refresh conversations to update last message
    fetchConversations();
  };

  const handleConversationStarted = (conversation) => {
    // Add new conversation to the list and select it
    fetchConversations();
    setSelectedConversation(conversation);
  };

  if (loading) {
    return <div className="loading">Loading conversations...</div>;
  }

  return (
    <div className="messaging-container">
      <div className="messaging-layout">
        <div className="conversation-list-wrapper">
          <ConversationList
            conversations={conversations}
            selectedConversation={selectedConversation}
            onSelectConversation={handleConversationSelect}
            currentUser={currentUser}
          />

          {/* Show "Find Students" button only for employers */}
          {currentUser?.user_type === 'employer' && (
            <button
              className="find-students-button"
              onClick={() => setShowStartConversationModal(true)}
            >
              + Find Students
            </button>
          )}
        </div>

        {selectedConversation ? (
          <MessageView
            conversation={selectedConversation}
            currentUser={currentUser}
            onMessageSent={handleMessageSent}
          />
        ) : (
          <div className="no-conversation-selected">
            <p>Select a conversation to start messaging</p>
            {currentUser?.user_type === 'employer' && (
              <button
                className="start-conversation-button"
                onClick={() => setShowStartConversationModal(true)}
              >
                Find Students
              </button>
            )}
          </div>
        )}
      </div>

      {error && <div className="error-message">{error}</div>}

      {/* Modal for finding students */}
      {showStartConversationModal && (
        <StartConversationModal
          onClose={() => setShowStartConversationModal(false)}
          onConversationStarted={handleConversationStarted}
        />
      )}
    </div>
  );
}

export default Messaging;
