import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Modal,
  Platform,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import api from '../services/api';

// This must match the version in the backend
export const APP_VERSION = '1.3.0';

interface VersionCheckProps {
  children: React.ReactNode;
}

interface VersionInfo {
  current_version: string;
  minimum_version: string;
  update_required: boolean;
  update_message: string | null;
}

export default function VersionCheck({ children }: VersionCheckProps) {
  const [updateRequired, setUpdateRequired] = useState(false);
  const [versionInfo, setVersionInfo] = useState<VersionInfo | null>(null);
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    checkVersion();
  }, []);

  const checkVersion = async () => {
    try {
      const response = await api.get(`/version?client_version=${APP_VERSION}`);
      const data: VersionInfo = response.data;
      setVersionInfo(data);
      
      if (data.update_required) {
        setUpdateRequired(true);
      }
    } catch (error) {
      // If version check fails, allow app to continue
      console.error('Version check failed:', error);
    } finally {
      setChecking(false);
    }
  };

  const handleRefresh = () => {
    if (Platform.OS === 'web') {
      // Force hard refresh on web
      window.location.reload();
    } else {
      // On mobile, re-check version
      setChecking(true);
      checkVersion();
    }
  };

  // Show blocking modal if update is required
  if (updateRequired && versionInfo) {
    return (
      <Modal visible={true} animationType="fade" transparent={false}>
        <View style={styles.container}>
          <View style={styles.content}>
            <View style={styles.iconContainer}>
              <Ionicons name="cloud-download" size={80} color="#2563eb" />
            </View>
            
            <Text style={styles.title}>Update Required</Text>
            
            <Text style={styles.message}>
              {versionInfo.update_message || 
                `A new version (${versionInfo.current_version}) is available. Please update to continue using the app.`}
            </Text>
            
            <View style={styles.versionInfo}>
              <Text style={styles.versionText}>
                Your version: <Text style={styles.versionNumber}>{APP_VERSION}</Text>
              </Text>
              <Text style={styles.versionText}>
                Required version: <Text style={styles.versionNumber}>{versionInfo.minimum_version}</Text>
              </Text>
            </View>
            
            <TouchableOpacity style={styles.refreshButton} onPress={handleRefresh}>
              <Ionicons name="refresh" size={24} color="#fff" />
              <Text style={styles.refreshButtonText}>
                {Platform.OS === 'web' ? 'Refresh Page' : 'Check Again'}
              </Text>
            </TouchableOpacity>
            
            <Text style={styles.helpText}>
              {Platform.OS === 'web' 
                ? 'Click the button above or press Ctrl+Shift+R (Cmd+Shift+R on Mac) to force refresh.'
                : 'If this issue persists, please close and reopen the app.'}
            </Text>
          </View>
        </View>
      </Modal>
    );
  }

  // Don't render children while checking version
  if (checking) {
    return (
      <View style={styles.loadingContainer}>
        <Ionicons name="shield-checkmark" size={48} color="#2563eb" />
        <Text style={styles.loadingText}>Checking for updates...</Text>
      </View>
    );
  }

  // Version is OK, render children
  return <>{children}</>;
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0c0c0c',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  content: {
    backgroundColor: '#1e293b',
    borderRadius: 24,
    padding: 32,
    alignItems: 'center',
    maxWidth: 400,
    width: '100%',
  },
  iconContainer: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: '#1e3a8a',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 24,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 16,
    textAlign: 'center',
  },
  message: {
    fontSize: 16,
    color: '#94a3b8',
    textAlign: 'center',
    lineHeight: 24,
    marginBottom: 24,
  },
  versionInfo: {
    backgroundColor: '#0f172a',
    borderRadius: 12,
    padding: 16,
    width: '100%',
    marginBottom: 24,
  },
  versionText: {
    fontSize: 14,
    color: '#64748b',
    marginBottom: 8,
  },
  versionNumber: {
    color: '#fff',
    fontWeight: '600',
  },
  refreshButton: {
    backgroundColor: '#2563eb',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 12,
    paddingVertical: 16,
    paddingHorizontal: 32,
    borderRadius: 12,
    width: '100%',
    marginBottom: 16,
  },
  refreshButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
  helpText: {
    fontSize: 12,
    color: '#64748b',
    textAlign: 'center',
    lineHeight: 18,
  },
  loadingContainer: {
    flex: 1,
    backgroundColor: '#0c0c0c',
    justifyContent: 'center',
    alignItems: 'center',
    gap: 16,
  },
  loadingText: {
    color: '#94a3b8',
    fontSize: 16,
  },
});
