import axios from 'axios';

// Use environment variable for API URL, fallback to localhost for development
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add token to headers
api.interceptors.request.use(
  (config) => {
    const accessToken = localStorage.getItem('access_token');
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // If error is 401 and we haven't tried to refresh yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');

        if (!refreshToken) {
          // No refresh token, redirect to login
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          localStorage.removeItem('user');
          window.location.href = '/login';
          return Promise.reject(error);
        }

        // Try to refresh the token
        const response = await axios.post(`${API_URL}/auth/refresh`, {
          refresh_token: refreshToken,
        });

        const { access_token } = response.data;

        // Save new access token
        localStorage.setItem('access_token', access_token);

        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed, clear tokens and redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (userData) => api.post('/auth/register', userData),
  login: (credentials) => api.post('/auth/login', credentials),
  getCurrentUser: () => api.get('/auth/me'),
  refreshToken: (refreshToken) =>
    api.post('/auth/refresh', { refresh_token: refreshToken }),
};

// Messaging API
export const messagingAPI = {
  getConversations: () => api.get('/messages/conversations'),
  getMessages: (conversationId, page = 1, perPage = 50) =>
    api.get(`/messages/conversations/${conversationId}/messages`, {
      params: { page, per_page: perPage },
    }),
  sendMessage: (conversationId, content, file = null) => {
    const formData = new FormData();
    if (content) formData.append('content', content);
    if (file) formData.append('file', file);

    return api.post(`/messages/conversations/${conversationId}/send`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  downloadFile: (filename) =>
    api.get(`/messages/files/${filename}`, {
      responseType: 'blob',
    }),
  markAsRead: (conversationId) =>
    api.post(`/messages/conversations/${conversationId}/mark-read`),
  startConversation: (recipientId) =>
    api.post('/messages/conversations/start', { recipient_id: recipientId }),
};

// Jobs API
export const jobsAPI = {
  applyForJob: (employerId, jobTitle) =>
    api.post('/jobs/applications', {
      employer_id: employerId,
      job_title: jobTitle,
    }),
  acceptApplication: (applicationId) =>
    api.post(`/jobs/applications/${applicationId}/accept`),
  rejectApplication: (applicationId) =>
    api.post(`/jobs/applications/${applicationId}/reject`),
  getApplications: () => api.get('/jobs/applications'),
};

// Users API
export const usersAPI = {
  getStudents: () => api.get('/users/students'), // Employer-only
};

export default api;
