import React, { createContext, useState, useContext, useEffect } from 'react';
import type { ReactNode } from 'react';
import { authService, paymentService } from '../services/api';
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
  hasPaid: boolean;
  checkingPayment: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name: string) => Promise<void>;
  guestLogin: () => Promise<void>;
  loginWithGoogle: () => Promise<void>;
  logout: () => Promise<void>;
  checkAuth: () => Promise<void>;
  checkPaymentStatus: () => Promise<void>;
  refreshPaymentStatus: () => Promise<boolean>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [sessionToken, setSessionToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [isGuest, setIsGuest] = useState(false);
  const [hasPaid, setHasPaid] = useState(false);
  const [checkingPayment, setCheckingPayment] = useState(false);

  useEffect(() => {
    checkAuth();

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

    Linking.getInitialURL().then((url) => {
      if (url) {
        handleUrl({ url });
      }
    });

    const subscription = Linking.addEventListener('url', handleUrl);

    if (Platform.OS === 'web') {
      const hash = window.location.hash;
      const sessionId = authService.extractSessionId(hash);
      if (sessionId) {
        authService.exchangeSessionId(sessionId)
          .then(async (data) => {
            await handleAuthSuccess(data.session_token);
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

  const checkPaymentStatus = async () => {
    try {
      setCheckingPayment(true);
      const token = await AsyncStorage.getItem('session_token');
      if (token) {
        const status = await paymentService.getPaymentStatus(token);
        setHasPaid(status.has_paid || false);
        await AsyncStorage.setItem('has_paid', status.has_paid ? 'true' : 'false');
      }
    } catch (error) {
      console.error('Payment status check failed:', error);
      const cached = await AsyncStorage.getItem('has_paid');
      if (cached === 'true') {
        setHasPaid(true);
      }
    } finally {
      setCheckingPayment(false);
    }
  };

  const refreshPaymentStatus = async (): Promise<boolean> => {
    try {
      const token = await AsyncStorage.getItem('session_token');
      if (token) {
        const verifyResult = await paymentService.verifyPayment(token);
        if (verifyResult.has_paid) {
          setHasPaid(true);
          await AsyncStorage.setItem('has_paid', 'true');
          return true;
        }
        const status = await paymentService.getPaymentStatus(token);
        setHasPaid(status.has_paid || false);
        await AsyncStorage.setItem('has_paid', status.has_paid ? 'true' : 'false');
        return status.has_paid || false;
      }
      return false;
    } catch (error) {
      console.error('Payment refresh failed:', error);
      return false;
    }
  };

  const checkAuth = async () => {
    try {
      const token = await AsyncStorage.getItem('session_token');
      if (token) {
        const userData = await authService.getMe(token);
        setUser(userData);
        setSessionToken(token);
        setIsGuest(userData.role === 'guest');
        if (userData.role !== 'guest') {
          const cachedPaid = await AsyncStorage.getItem('has_paid');
          if (cachedPaid === 'true') {
            setHasPaid(true);
          }
          checkPaymentStatus();
        }
      }
    } catch (error) {
      console.error('Auth check failed:', error);
      await AsyncStorage.removeItem('session_token');
      setUser(null);
      setSessionToken(null);
      setIsGuest(false);
      setHasPaid(false);
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
      if (userData.session_token) {
        await AsyncStorage.setItem('session_token', userData.session_token);
        setSessionToken(userData.session_token);
      }
      setUser(userData);
      setIsGuest(userData.is_guest || false);
      if (!userData.is_guest) {
        setTimeout(() => checkPaymentStatus(), 500);
      }
    } catch (error: any) {
      console.error('Login error details:', error);
      if (error.code === 'ECONNABORTED' || error.message?.includes('timeout')) {
        throw new Error('Connection timed out. Please check your internet and try again.');
      }
      if (error.code === 'ERR_NETWORK' || error.message?.includes('Network Error')) {
        throw new Error('Network error. Please check your internet connection.');
      }
      throw new Error(error.response?.data?.detail || 'Login failed. Please try again.');
    }
  };

  const guestLogin = async () => {
    try {
      const userData = await authService.guestLogin();
      if (userData.session_token) {
        await AsyncStorage.setItem('session_token', userData.session_token);
        await AsyncStorage.setItem('was_guest', 'true');
        setSessionToken(userData.session_token);
      }
      setUser(userData);
      setIsGuest(true);
      setHasPaid(false);
    } catch (error: any) {
      console.error('Guest login error details:', error);
      if (error.code === 'ECONNABORTED' || error.message?.includes('timeout')) {
        throw new Error('Connection timed out. Please check your internet and try again.');
      }
      if (error.code === 'ERR_NETWORK' || error.message?.includes('Network Error')) {
        throw new Error('Network error. Please check your internet connection.');
      }
      throw new Error(error.response?.data?.detail || 'Guest login failed. Please try again.');
    }
  };

  const register = async (email: string, password: string, name: string) => {
    try {
      const userData = await authService.register(email, password, name);
      if (userData.session_token) {
        await AsyncStorage.setItem('session_token', userData.session_token);
        setSessionToken(userData.session_token);
      }
      setUser(userData);
      setIsGuest(false);
      setHasPaid(false);
    } catch (error: any) {
      console.error('Register error details:', error);
      if (error.code === 'ECONNABORTED' || error.message?.includes('timeout')) {
        throw new Error('Connection timed out. Please check your internet and try again.');
      }
      if (error.code === 'ERR_NETWORK' || error.message?.includes('Network Error')) {
        throw new Error('Network error. Please check your internet connection.');
      }
      throw new Error(error.response?.data?.detail || 'Registration failed. Please try again.');
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
      await AsyncStorage.removeItem('was_guest');
      await AsyncStorage.removeItem('has_paid');
      setUser(null);
      setSessionToken(null);
      setIsGuest(false);
      setHasPaid(false);
    }
  };

  return (
    <AuthContext.Provider value={{
      user,
      sessionToken,
      loading,
      isGuest,
      hasPaid,
      checkingPayment,
      login,
      register,
      guestLogin,
      loginWithGoogle,
      logout,
      checkAuth,
      checkPaymentStatus,
      refreshPaymentStatus,
    }}>
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
