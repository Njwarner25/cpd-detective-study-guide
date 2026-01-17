import React, { createContext, useState, useContext, useEffect } from 'react';
import type { ReactNode } from 'react';
import { authService } from '../services/api';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as Linking from 'expo-linking';
import { Platform } from 'react-native';

interface User {
  user_id: string;
  email: string;
  name: string;
  picture?: string;
  role: string;
  is_guest?: boolean;
}

interface AuthContextType {
  user: User | null;
  sessionToken: string | null;
  loading: boolean;
  isGuest: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name: string) => Promise<void>;
  guestLogin: () => Promise<void>;
  loginWithGoogle: () => Promise<void>;
  logout: () => Promise<void>;
  checkAuth: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [sessionToken, setSessionToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [isGuest, setIsGuest] = useState(false);

  useEffect(() => {
    // Check for existing session on mount
    checkAuth();

    // Handle deep links (for OAuth redirect on mobile)
    const handleUrl = async (event: { url: string }) => {
      const sessionId = authService.extractSessionId(event.url);
      if (sessionId) {
        try {
          const data = await authService.exchangeSessionId(sessionId);
          await handleAuthSuccess(data.session_token);
        } catch (error) {
          console.error('Failed to exchange session ID:', error);
        }
      }
    };

    // Check initial URL (cold start)
    Linking.getInitialURL().then((url) => {
      if (url) {
        handleUrl({ url });
      }
    });

    // Listen for URL events (hot link)
    const subscription = Linking.addEventListener('url', handleUrl);

    // Web platform: check for session_id in URL hash
    if (Platform.OS === 'web') {
      const hash = window.location.hash;
      const sessionId = authService.extractSessionId(hash);
      if (sessionId) {
        authService.exchangeSessionId(sessionId)
          .then(async (data) => {
            await handleAuthSuccess(data.session_token);
            // Clean URL
            window.history.replaceState(null, '', window.location.pathname);
          })
          .catch(console.error);
      }
    }

    return () => {
      subscription.remove();
    };
  }, []);

  const handleAuthSuccess = async (token: string) => {
    await AsyncStorage.setItem('session_token', token);
    setSessionToken(token);
    await checkAuth();
  };

  const checkAuth = async () => {
    try {
      const token = await AsyncStorage.getItem('session_token');
      if (token) {
        const userData = await authService.getMe(token);
        setUser(userData);
        setSessionToken(token);
        setIsGuest(userData.role === 'guest');
      }
    } catch (error) {
      console.error('Auth check failed:', error);
      // Clear invalid token
      await AsyncStorage.removeItem('session_token');
      setUser(null);
      setSessionToken(null);
      setIsGuest(false);
      
      // Check if this was a guest session and auto-re-login
      const wasGuest = await AsyncStorage.getItem('was_guest');
      if (wasGuest === 'true') {
        console.log('Re-authenticating as guest...');
        try {
          const userData = await authService.guestLogin();
          if (userData.session_token) {
            await AsyncStorage.setItem('session_token', userData.session_token);
            setSessionToken(userData.session_token);
          }
          setUser(userData);
          setIsGuest(true);
        } catch (guestError) {
          console.error('Guest re-auth failed:', guestError);
        }
      }
    } finally {
      setLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    try {
      const userData = await authService.login(email, password);
      // Store session token from response
      if (userData.session_token) {
        await AsyncStorage.setItem('session_token', userData.session_token);
        setSessionToken(userData.session_token);
      }
      setUser(userData);
      setIsGuest(userData.is_guest || false);
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Login failed');
    }
  };

  const guestLogin = async () => {
    try {
      const userData = await authService.guestLogin();
      // Store session token from response
      if (userData.session_token) {
        await AsyncStorage.setItem('session_token', userData.session_token);
        await AsyncStorage.setItem('was_guest', 'true');
        setSessionToken(userData.session_token);
      }
      setUser(userData);
      setIsGuest(true);
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Guest login failed');
    }
  };

  const register = async (email: string, password: string, name: string) => {
    try {
      const userData = await authService.register(email, password, name);
      // Store session token from response
      if (userData.session_token) {
        await AsyncStorage.setItem('session_token', userData.session_token);
        setSessionToken(userData.session_token);
      }
      setUser(userData);
      setIsGuest(false);
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Registration failed');
    }
  };

  const loginWithGoogle = async () => {
    try {
      const result = await authService.loginWithGoogle();
      if (result && result.session_token) {
        await handleAuthSuccess(result.session_token);
      }
    } catch (error: any) {
      throw new Error(error.message || 'Google login failed');
    }
  };

  const logout = async () => {
    try {
      await authService.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      await AsyncStorage.removeItem('session_token');
      setUser(null);
      setSessionToken(null);
    }
  };

  return (
    <AuthContext.Provider value={{ user, sessionToken, loading, isGuest, login, register, guestLogin, loginWithGoogle, logout, checkAuth }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};