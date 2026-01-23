import axios from 'axios';
import * as WebBrowser from 'expo-web-browser';
import * as Linking from 'expo-linking';
import { Platform } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import Constants from 'expo-constants';

// Backend URL - hardcoded for reliability in native builds
// This is the preview URL that the APK will use
const NATIVE_BACKEND_URL = 'https://police-study.preview.emergentagent.com';

// Get the backend URL
const getBackendUrl = () => {
  // For native builds (Android/iOS APK), always use the hardcoded URL
  if (Platform.OS !== 'web') {
    console.log('Native build - using hardcoded URL:', NATIVE_BACKEND_URL);
    return NATIVE_BACKEND_URL;
  }
  // For web/development, use environment variable
  const envUrl = process.env.EXPO_PUBLIC_BACKEND_URL || '';
  console.log('Web build - using env URL:', envUrl);
  return envUrl;
};

const BACKEND_URL = getBackendUrl();
console.log('Final backend URL:', BACKEND_URL);

const api = axios.create({
  baseURL: `${BACKEND_URL}/api`,
  withCredentials: false, // Use token-based auth instead of cookies for mobile
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  timeout: 45000, // 45 second timeout for slow connections/cold starts
});

// Flag to prevent infinite retry loops
let isRefreshing = false;

// Request interceptor to add auth token to all requests
api.interceptors.request.use(
  async (config) => {
    try {
      const token = await AsyncStorage.getItem('session_token');
      if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
        console.log('Added auth token to request:', config.url);
      } else {
        console.log('No auth token found for request:', config.url);
      }
    } catch (error) {
      console.error('Error getting token from storage:', error);
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle 401 errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // If 401 and not already retrying
    if (error.response?.status === 401 && !originalRequest._retry && !isRefreshing) {
      originalRequest._retry = true;
      isRefreshing = true;
      
      try {
        // Try to get a new guest session
        console.log('Session expired, getting new guest session...');
        const response = await axios.post(`${BACKEND_URL}/api/auth/guest`);
        const newToken = response.data.session_token;
        
        if (newToken) {
          await AsyncStorage.setItem('session_token', newToken);
          await AsyncStorage.setItem('was_guest', 'true');
          
          // Update the failed request with new token
          originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
          
          isRefreshing = false;
          return api(originalRequest);
        }
      } catch (refreshError) {
        console.error('Failed to refresh session:', refreshError);
        isRefreshing = false;
      }
    }
    
    isRefreshing = false;
    return Promise.reject(error);
  }
);

// Auth Service with retry logic for cold starts
const MAX_RETRIES = 3;
const RETRY_DELAY = 5000; // 5 seconds between retries

const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

const withRetry = async <T>(fn: () => Promise<T>, retries = MAX_RETRIES): Promise<T> => {
  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      console.log(`Attempt ${attempt}/${retries}...`);
      return await fn();
    } catch (error: any) {
      const isNetworkError = error.code === 'ERR_NETWORK' || 
                            error.code === 'ECONNABORTED' ||
                            error.message?.includes('Network Error') ||
                            error.message?.includes('timeout');
      
      if (isNetworkError && attempt < retries) {
        console.log(`Network error on attempt ${attempt}, retrying in ${RETRY_DELAY/1000}s...`);
        await sleep(RETRY_DELAY);
        continue;
      }
      throw error;
    }
  }
  throw new Error('Max retries exceeded');
};

export const authService = {
  async register(email: string, password: string, name: string) {
    return withRetry(async () => {
      const response = await api.post('/auth/register', { email, password, name });
      return response.data;
    });
  },

  async login(email: string, password: string) {
    return withRetry(async () => {
      const response = await api.post('/auth/login', { email, password });
      return response.data;
    });
  },

  async guestLogin() {
    return withRetry(async () => {
      const response = await api.post('/auth/guest');
      return response.data;
    });
  },

  async loginWithGoogle() {
    const redirectUrl = Platform.OS === 'web'
      ? window.location.origin + '/'
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
  async getLeaderboard(token?: string) {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const response = await api.get('/leaderboard', { headers });
    return response.data;
  },
  async resetScores(token?: string) {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const response = await api.post('/reset-scores', {}, { headers });
    return response.data;
  },
};

// Admin Service
export const adminService = {
  async getAnalytics(token?: string) {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const response = await api.get('/admin/analytics', { headers });
    return response.data;
  },
};

export default api;