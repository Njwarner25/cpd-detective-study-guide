import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Modal,
  Platform,
  Linking,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import * as WebBrowser from 'expo-web-browser';
import api from '../services/api';

// This must match the version in the backend
export const APP_VERSION = '1.4.0';

// APK Download URL - Update this when building new APK
const APK_DOWNLOAD_URL = 'https://expo.dev/artifacts/eas/nbESgJdthDNMN4CNV6ggd3.apk';

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
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    checkVersion();
  }, []);

  const checkVersion = async () => {
    setError(null);
    setChecking(true);
    try {
      const response = await api.get(`/version?client_version=${APP_VERSION}`);
      const data: VersionInfo = response.data;
      setVersionInfo(data);
      
      if (data.update_required) {
        setUpdateRequired(true);
      }
    } catch (err: any) {
      // If version check fails due to network, show error but allow retry
      console.error('Version check failed:', err);
      if (err.code === 'ERR_NETWORK' || err.message?.includes('Network Error')) {
        setError('Unable to connect to server. Please check your internet connection.');
      } else if (err.code === 'ECONNABORTED') {
        setError('Connection timed out. The server may be starting up, please try again.');
      } else {
        // For other errors, allow app to continue
        setChecking(false);
        return;
      }
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
      checkVersion();
    }
  };

  const handleDownloadAPK = async () => {
    try {
      // First try to open in browser which will trigger download
      const canOpen = await Linking.canOpenURL(APK_DOWNLOAD_URL);
      
      if (canOpen) {
        await Linking.openURL(APK_DOWNLOAD_URL);
      } else {
        // Fallback to WebBrowser
        await WebBrowser.openBrowserAsync(APK_DOWNLOAD_URL);
      }
    } catch (error) {
      console.error('Failed to open download URL:', error);
      // Show alert with manual URL
      Alert.alert(
        'Download Link',
        `Please copy this URL and open in your browser:\n\n${APK_DOWNLOAD_URL}`,
        [
          { text: 'OK' }
        ]
      );
    }
  };

  // Show error state with retry
  if (error) {
    return (
      <View style={styles.container}>
        <View style={styles.content}>
          <View style={[styles.iconContainer, styles.errorIconContainer]}>
            <Ionicons name="cloud-offline" size={80} color="#f59e0b" />
          </View>
          
          <Text style={styles.title}>Connection Error</Text>
          
          <Text style={styles.message}>{error}</Text>
          
          <TouchableOpacity style={styles.refreshButton} onPress={handleRefresh}>
            <Ionicons name="refresh" size={24} color="#fff" />
            <Text style={styles.refreshButtonText}>Try Again</Text>
          </TouchableOpacity>
          
          <Text style={styles.helpText}>
            If this is your first time opening the app, the server may need a moment to start up. Please wait 10-15 seconds and try again.
          </Text>
        </View>
      </View>
    );
  }

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
            
            {Platform.OS === 'web' ? (
              <>
                <TouchableOpacity style={styles.refreshButton} onPress={handleRefresh}>
                  <Ionicons name="refresh" size={24} color="#fff" />
                  <Text style={styles.refreshButtonText}>Refresh Page</Text>
                </TouchableOpacity>
                
                <Text style={styles.helpText}>
                  Click the button above or press Ctrl+Shift+R (Cmd+Shift+R on Mac) to force refresh.
                </Text>
              </>
            ) : (
              <>
                <TouchableOpacity style={styles.downloadButton} onPress={handleDownloadAPK}>
                  <Ionicons name="download" size={24} color="#fff" />
                  <Text style={styles.downloadButtonText}>Download New Version</Text>
                </TouchableOpacity>
                
                <TouchableOpacity style={styles.secondaryButton} onPress={handleRefresh}>
                  <Ionicons name="refresh" size={20} color="#3b82f6" />
                  <Text style={styles.secondaryButtonText}>Check Again</Text>
                </TouchableOpacity>
                
                <Text style={styles.helpText}>
                  Download and install the new APK to continue using the app. You may need to uninstall the current version first.
                </Text>
              </>
            )}
          </View>
        </View>
      </Modal>
    );
  }

  // Don't render children while checking version
  if (checking) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#2563eb" />
        <Ionicons name="shield-checkmark" size={48} color="#2563eb" style={styles.loadingIcon} />
        <Text style={styles.loadingText}>Checking for updates...</Text>
        <Text style={styles.loadingSubText}>Please wait</Text>
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
  errorIconContainer: {
    backgroundColor: '#78350f',
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
  downloadButton: {
    backgroundColor: '#22c55e',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 12,
    paddingVertical: 16,
    paddingHorizontal: 32,
    borderRadius: 12,
    width: '100%',
    marginBottom: 12,
  },
  downloadButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
  secondaryButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#3b82f6',
    marginBottom: 16,
  },
  secondaryButtonText: {
    color: '#3b82f6',
    fontSize: 14,
    fontWeight: '500',
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
  },
  loadingIcon: {
    marginTop: 20,
  },
  loadingText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
    marginTop: 16,
  },
  loadingSubText: {
    color: '#64748b',
    fontSize: 14,
    marginTop: 8,
  },
});
