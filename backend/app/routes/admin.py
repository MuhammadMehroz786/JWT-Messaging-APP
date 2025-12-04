from flask import Blueprint, jsonify, render_template_string
from app import db
from app.models.user import User
from app.models.conversation import Conversation, ConversationParticipant, Message
from app.models.job_application import JobApplication

bp = Blueprint('admin', __name__, url_prefix='/admin')

# HTML template for displaying database
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Database Viewer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background: #f5f5f5;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .section {
            margin-bottom: 40px;
        }
        h2 {
            color: #667eea;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }
        th {
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }
        td {
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }
        tr:hover {
            background: #f8f9fa;
        }
        .no-data {
            text-align: center;
            padding: 20px;
            color: #999;
            font-style: italic;
        }
        .stats {
            display: flex;
            gap: 20px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        .stat-card {
            flex: 1;
            min-width: 200px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-number {
            font-size: 36px;
            font-weight: bold;
        }
        .stat-label {
            margin-top: 5px;
            opacity: 0.9;
        }
        .refresh-btn {
            display: block;
            margin: 20px auto;
            padding: 12px 30px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 16px;
            cursor: pointer;
            transition: opacity 0.3s;
        }
        .refresh-btn:hover {
            opacity: 0.9;
        }
        .timestamp {
            text-align: center;
            color: #666;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Database Viewer</h1>
        <p class="timestamp">Last Updated: {{ timestamp }}</p>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{{ stats.users }}</div>
                <div class="stat-label">Total Users</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ stats.conversations }}</div>
                <div class="stat-label">Conversations</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ stats.messages }}</div>
                <div class="stat-label">Messages</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ stats.applications }}</div>
                <div class="stat-label">Job Applications</div>
            </div>
        </div>

        <button class="refresh-btn" onclick="location.reload()">🔄 Refresh Data</button>

        <!-- Users Table -->
        <div class="section">
            <h2>👥 Users</h2>
            {% if users %}
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Username</th>
                        <th>Email</th>
                        <th>Full Name</th>
                        <th>User Type</th>
                        <th>Created At</th>
                    </tr>
                </thead>
                <tbody>
                    {% for user in users %}
                    <tr>
                        <td>{{ user.id }}</td>
                        <td>{{ user.username }}</td>
                        <td>{{ user.email }}</td>
                        <td>{{ user.full_name or '-' }}</td>
                        <td>{{ user.user_type }}</td>
                        <td>{{ user.created_at.strftime('%Y-%m-%d %H:%M:%S') }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <p class="no-data">No users found</p>
            {% endif %}
        </div>

        <!-- Conversations Table -->
        <div class="section">
            <h2>💬 Conversations</h2>
            {% if conversations %}
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Participants</th>
                        <th>Messages Count</th>
                        <th>Created At</th>
                        <th>Updated At</th>
                    </tr>
                </thead>
                <tbody>
                    {% for conv in conversations %}
                    <tr>
                        <td>{{ conv.id }}</td>
                        <td>
                            {% for p in conv.participants %}
                            {{ p.user.username }}{% if not loop.last %}, {% endif %}
                            {% endfor %}
                        </td>
                        <td>{{ conv.messages|length }}</td>
                        <td>{{ conv.created_at.strftime('%Y-%m-%d %H:%M:%S') }}</td>
                        <td>{{ conv.updated_at.strftime('%Y-%m-%d %H:%M:%S') }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <p class="no-data">No conversations found</p>
            {% endif %}
        </div>

        <!-- Messages Table -->
        <div class="section">
            <h2>✉️ Messages</h2>
            {% if messages %}
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Conversation ID</th>
                        <th>Sender</th>
                        <th>Content</th>
                        <th>Has Attachment</th>
                        <th>File Name</th>
                        <th>Created At</th>
                    </tr>
                </thead>
                <tbody>
                    {% for msg in messages %}
                    <tr>
                        <td>{{ msg.id }}</td>
                        <td>{{ msg.conversation_id }}</td>
                        <td>{{ msg.sender.username }}</td>
                        <td>{{ msg.content[:50] if msg.content else '-' }}{% if msg.content and msg.content|length > 50 %}...{% endif %}</td>
                        <td>{{ '✓' if msg.has_attachment else '-' }}</td>
                        <td>{{ msg.file_name or '-' }}</td>
                        <td>{{ msg.created_at.strftime('%Y-%m-%d %H:%M:%S') }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <p class="no-data">No messages found</p>
            {% endif %}
        </div>

        <!-- Job Applications Table -->
        <div class="section">
            <h2>💼 Job Applications</h2>
            {% if applications %}
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Student</th>
                        <th>Employer</th>
                        <th>Job Title</th>
                        <th>Status</th>
                        <th>Created At</th>
                    </tr>
                </thead>
                <tbody>
                    {% for app in applications %}
                    <tr>
                        <td>{{ app.id }}</td>
                        <td>{{ app.student.username }}</td>
                        <td>{{ app.employer.username }}</td>
                        <td>{{ app.job_title }}</td>
                        <td>{{ app.status }}</td>
                        <td>{{ app.created_at.strftime('%Y-%m-%d %H:%M:%S') }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <p class="no-data">No job applications found</p>
            {% endif %}
        </div>
    </div>
</body>
</html>
'''

@bp.route('/database')
def view_database():
    """View all database tables in a nice HTML format"""
    from datetime import datetime

    # Get all data
    users = User.query.all()
    conversations = Conversation.query.all()
    messages = Message.query.order_by(Message.created_at.desc()).all()
    applications = JobApplication.query.all()

    # Calculate stats
    stats = {
        'users': len(users),
        'conversations': len(conversations),
        'messages': len(messages),
        'applications': len(applications)
    }

    return render_template_string(
        HTML_TEMPLATE,
        users=users,
        conversations=conversations,
        messages=messages,
        applications=applications,
        stats=stats,
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )


@bp.route('/database/json')
def view_database_json():
    """View all database data as JSON"""
    users = User.query.all()
    conversations = Conversation.query.all()
    messages = Message.query.all()
    applications = JobApplication.query.all()

    return jsonify({
        'users': [u.to_dict() for u in users],
        'conversations': [c.to_dict() for c in conversations],
        'messages': [m.to_dict() for m in messages],
        'applications': [a.to_dict() for a in applications]
    })
