import axios from 'axios';
import * as WebBrowser from 'expo-web-browser';
import * as Linking from 'expo-linking';
import { Platform } from 'react-native';

// Get the backend URL - always use the full URL for API calls
const BACKEND_URL = process.env.EXPO_PUBLIC_BACKEND_URL || '';

const api = axios.create({
  baseURL: `${BACKEND_URL}/api`,
  withCredentials: false, // Use token-based auth instead of cookies for mobile
  headers: {
    'Content-Type': 'application/json',
  },
});

// Auth Service
export const authService = {
  async register(email: string, password: string, name: string) {
    const response = await api.post('/auth/register', { email, password, name });
    return response.data;
  },

  async login(email: string, password: string) {
    const response = await api.post('/auth/login', { email, password });
    return response.data;
  },

  async loginWithGoogle() {
    const redirectUrl = Platform.OS === 'web'
      ? `${typeof window !== 'undefined' ? window.location.origin : ''}/`
      : Linking.createURL('/');

    const authUrl = `https://auth.emergentagent.com/?redirect=${encodeURIComponent(redirectUrl)}`;

    if (Platform.OS === 'web') {
      window.location.href = authUrl;
      return null;
    } else {
      const result = await WebBrowser.openAuthSessionAsync(authUrl, redirectUrl);
      
      if (result.type === 'success' && result.url) {
        const url = result.url;
        const sessionId = this.extractSessionId(url);
        
        if (sessionId) {
          return await this.exchangeSessionId(sessionId);
        }
      }
      throw new Error('Google login was cancelled or failed');
    }
  },

  extractSessionId(url: string): string | null {
    // Check hash first
    const hashMatch = url.match(/[#&]session_id=([^&]+)/);
    if (hashMatch) return hashMatch[1];
    
    // Check query params
    const queryMatch = url.match(/[?&]session_id=([^&]+)/);
    if (queryMatch) return queryMatch[1];
    
    return null;
  },

  async exchangeSessionId(sessionId: string) {
    const response = await api.get('/auth/session-data', {
      headers: { 'X-Session-ID': sessionId }
    });
    return response.data;
  },

  async getMe(token?: string) {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const response = await api.get('/auth/me', { headers });
    return response.data;
  },

  async logout() {
    const response = await api.post('/auth/logout');
    return response.data;
  },
};

// Question Service
export const questionService = {
  async getQuestions(type?: string, categoryId?: string, token?: string) {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const params: any = {};
    if (type) params.type = type;
    if (categoryId) params.category_id = categoryId;
    
    const response = await api.get('/questions', { headers, params });
    return response.data;
  },

  async getQuestion(questionId: string, token?: string) {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const response = await api.get(`/questions/${questionId}`, { headers });
    return response.data;
  },

  async createQuestion(data: any, token?: string) {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const response = await api.post('/questions', data, { headers });
    return response.data;
  },

  async updateQuestion(questionId: string, data: any, token?: string) {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const response = await api.put(`/questions/${questionId}`, data, { headers });
    return response.data;
  },

  async deleteQuestion(questionId: string, token?: string) {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const response = await api.delete(`/questions/${questionId}`, { headers });
    return response.data;
  },
};

// Category Service
export const categoryService = {
  async getCategories() {
    const response = await api.get('/categories');
    return response.data;
  },
};

// Bookmark Service
export const bookmarkService = {
  async toggleBookmark(questionId: string, token?: string) {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const response = await api.post('/bookmarks/toggle', { question_id: questionId }, { headers });
    return response.data;
  },

  async getBookmarks(token?: string) {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const response = await api.get('/bookmarks', { headers });
    return response.data;
  },

  async getProgress(questionId: string, token?: string) {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const response = await api.get(`/progress/${questionId}`, { headers });
    return response.data;
  },
};

// Scenario Service
export const scenarioService = {
  async submitResponse(questionId: string, userResponse: string, timeTaken: number, token?: string) {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const response = await api.post('/scenarios/submit', {
      question_id: questionId,
      user_response: userResponse,
      time_taken: timeTaken
    }, { headers });
    return response.data;
  },

  async getHistory(token?: string) {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const response = await api.get('/scenarios/history', { headers });
    return response.data;
  },
};

// Stats Service
export const statsService = {
  async getStats(token?: string) {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const response = await api.get('/stats', { headers });
    return response.data;
  },
};

export default api;