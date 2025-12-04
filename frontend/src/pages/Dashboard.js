import React from 'react';
import { useNavigate } from 'react-router-dom';
import { getUser, clearAuthData } from '../utils/auth';
import Messaging from '../components/messaging/Messaging';
import './Dashboard.css';

function Dashboard() {
  const navigate = useNavigate();
  const user = getUser();

  const handleLogout = () => {
    clearAuthData();
    navigate('/login');
  };

  return (
    <div className="dashboard">
      <nav className="dashboard-nav">
        <div className="nav-content">
          <h1>CN Project</h1>

          <div className="nav-right">
            <div className="user-info">
              <span className="username">{user?.username}</span>
              <span className="user-type-badge-nav">
                {user?.user_type}
              </span>
            </div>
            <button onClick={handleLogout} className="logout-btn">
              Logout
            </button>
          </div>
        </div>
      </nav>

      <div className="dashboard-content">
        <Messaging />
      </div>
    </div>
  );
}

export default Dashboard;
