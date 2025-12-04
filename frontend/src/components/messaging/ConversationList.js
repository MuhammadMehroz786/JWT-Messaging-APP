import React from 'react';
import './Messaging.css';

function ConversationList({
  conversations,
  selectedConversation,
  onSelectConversation,
  currentUser,
}) {
  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString();
  };

  return (
    <div className="conversation-list">
      <div className="conversation-list-header">
        <h3>Messages</h3>
      </div>

      {conversations.length === 0 ? (
        <div className="no-conversations">
          <p>No conversations yet</p>
        </div>
      ) : (
        <div className="conversations">
          {conversations.map((conversation) => {
            const isSelected =
              selectedConversation?.id === conversation.id;
            const otherParticipant = conversation.other_participant;

            return (
              <div
                key={conversation.id}
                className={`conversation-item ${
                  isSelected ? 'selected' : ''
                }`}
                onClick={() => onSelectConversation(conversation)}
              >
                <div className="conversation-avatar">
                  {otherParticipant?.username?.charAt(0).toUpperCase() ||
                    '?'}
                </div>

                <div className="conversation-info">
                  <div className="conversation-header">
                    <span className="conversation-name">
                      {otherParticipant?.full_name ||
                        otherParticipant?.username ||
                        'Unknown User'}
                    </span>
                    {conversation.last_message && (
                      <span className="conversation-time">
                        {formatTime(conversation.last_message.created_at)}
                      </span>
                    )}
                  </div>

                  <div className="conversation-preview">
                    {conversation.last_message ? (
                      <span className="last-message">
                        {conversation.last_message.content}
                      </span>
                    ) : (
                      <span className="no-messages">
                        No messages yet
                      </span>
                    )}
                    {conversation.unread_count > 0 && (
                      <span className="unread-badge">
                        {conversation.unread_count}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default ConversationList;
