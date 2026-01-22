import React, { useState } from 'react';
import { View, Text, ScrollView, StyleSheet, TouchableOpacity, Platform, Linking } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';

type DeviceType = 'android' | 'ios';

export default function InstallApp() {
  const router = useRouter();
  const [selectedDevice, setSelectedDevice] = useState<DeviceType>(
    Platform.OS === 'ios' ? 'ios' : 'android'
  );

  // Direct APK download URL from EAS Build
  const apkDownloadUrl = 'https://expo.dev/artifacts/eas/QjyBscnWucWMiptU35iFb.apk';

  const androidApkSteps = [
    {
      icon: 'download-outline' as const,
      title: 'Download the APK',
      description: 'Tap the download button below to get the APK file',
    },
    {
      icon: 'folder-outline' as const,
      title: 'Open Downloads',
      description: 'Go to your Downloads folder or notification panel',
    },
    {
      icon: 'shield-checkmark-outline' as const,
      title: 'Allow Installation',
      description: 'If prompted, allow installation from unknown sources in Settings',
    },
    {
      icon: 'checkmark-circle' as const,
      title: 'Install the App',
      description: 'Tap the APK file and select "Install"',
    },
    {
      icon: 'apps-outline' as const,
      title: 'Launch the App',
      description: 'Find the CPD Study Guide icon in your app drawer and tap to open!',
    },
  ];

  const iosSteps = [
    {
      icon: 'compass-outline' as const,
      title: 'Open Safari Browser',
      description: 'Launch Safari on your iPhone or iPad (this only works in Safari)',
    },
    {
      icon: 'globe-outline' as const,
      title: 'Visit the Web App',
      description: 'Open this app in Safari on your device',
    },
    {
      icon: 'share-outline' as const,
      title: 'Tap the Share Button',
      description: 'Tap the share icon (square with arrow) at the bottom of Safari',
    },
    {
      icon: 'add-circle-outline' as const,
      title: 'Select "Add to Home Screen"',
      description: 'Scroll down in the share menu and tap "Add to Home Screen"',
    },
    {
      icon: 'create-outline' as const,
      title: 'Name the App',
      description: 'Keep the default name or customize it, then tap "Add"',
    },
    {
      icon: 'apps-outline' as const,
      title: 'Launch the App',
      description: 'Find the CPD Study Guide icon on your home screen and tap to open!',
    },
  ];

  const steps = selectedDevice === 'android' ? androidApkSteps : iosSteps;

  const handleDownloadAPK = () => {
    Linking.openURL(apkDownloadUrl);
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
          <Ionicons name="arrow-back" size={24} color="#fff" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Install App</Text>
        <View style={styles.placeholder} />
      </View>

      <ScrollView style={styles.scrollView} showsVerticalScrollIndicator={false}>
        {/* Hero Section */}
        <View style={styles.heroSection}>
          <View style={styles.iconContainer}>
            <Ionicons name="download-outline" size={48} color="#3b82f6" />
          </View>
          <Text style={styles.heroTitle}>Install on Your Device</Text>
          <Text style={styles.heroSubtitle}>
            Get the CPD Detective Study Guide app on your phone for the best experience!
          </Text>
        </View>

        {/* Benefits */}
        <View style={styles.benefitsContainer}>
          <View style={styles.benefitItem}>
            <Ionicons name="flash" size={20} color="#10b981" />
            <Text style={styles.benefitText}>Instant access</Text>
          </View>
          <View style={styles.benefitItem}>
            <Ionicons name="notifications" size={20} color="#10b981" />
            <Text style={styles.benefitText}>Native experience</Text>
          </View>
          <View style={styles.benefitItem}>
            <Ionicons name="resize" size={20} color="#10b981" />
            <Text style={styles.benefitText}>Full-screen</Text>
          </View>
        </View>

        {/* Device Selector */}
        <View style={styles.deviceSelector}>
          <TouchableOpacity
            style={[
              styles.deviceButton,
              selectedDevice === 'android' && styles.deviceButtonActive,
            ]}
            onPress={() => setSelectedDevice('android')}
          >
            <Ionicons 
              name="logo-android" 
              size={24} 
              color={selectedDevice === 'android' ? '#fff' : '#64748b'} 
            />
            <Text style={[
              styles.deviceButtonText,
              selectedDevice === 'android' && styles.deviceButtonTextActive
            ]}>
              Android
            </Text>
          </TouchableOpacity>
          
          <TouchableOpacity
            style={[
              styles.deviceButton,
              selectedDevice === 'ios' && styles.deviceButtonActive,
            ]}
            onPress={() => setSelectedDevice('ios')}
          >
            <Ionicons 
              name="logo-apple" 
              size={24} 
              color={selectedDevice === 'ios' ? '#fff' : '#64748b'} 
            />
            <Text style={[
              styles.deviceButtonText,
              selectedDevice === 'ios' && styles.deviceButtonTextActive
            ]}>
              iPhone/iPad
            </Text>
          </TouchableOpacity>
        </View>

        {/* Android APK Download Section */}
        {selectedDevice === 'android' && (
          <View style={styles.apkSection}>
            <View style={styles.apkCard}>
              <View style={styles.apkIconRow}>
                <View style={styles.apkIconContainer}>
                  <Ionicons name="logo-android" size={32} color="#3ddc84" />
                </View>
                <View style={styles.apkInfo}>
                  <Text style={styles.apkTitle}>Android APK</Text>
                  <Text style={styles.apkVersion}>Version 1.3.0 • ~50MB</Text>
                </View>
              </View>
              <TouchableOpacity style={styles.downloadButton} onPress={handleDownloadAPK}>
                <Ionicons name="download" size={24} color="#fff" />
                <Text style={styles.downloadButtonText}>Download APK</Text>
              </TouchableOpacity>
            </View>
          </View>
        )}

        {/* iOS Note */}
        {selectedDevice === 'ios' && (
          <View style={styles.browserNote}>
            <Ionicons name="information-circle" size={18} color="#f59e0b" />
            <Text style={styles.browserNoteText}>
              iOS apps require App Store distribution. For now, add to home screen from Safari for the best experience.
            </Text>
          </View>
        )}

        {/* Steps */}
        <View style={styles.stepsContainer}>
          <Text style={styles.stepsTitle}>Installation Steps</Text>
          
          {steps.map((step, index) => (
            <View key={index} style={styles.stepItem}>
              <View style={styles.stepNumber}>
                <Text style={styles.stepNumberText}>{index + 1}</Text>
              </View>
              <View style={styles.stepContent}>
                <View style={styles.stepHeader}>
                  <Ionicons name={step.icon} size={20} color="#3b82f6" />
                  <Text style={styles.stepTitle}>{step.title}</Text>
                </View>
                <Text style={styles.stepDescription}>{step.description}</Text>
              </View>
            </View>
          ))}
        </View>

        {/* Android Security Note */}
        {selectedDevice === 'android' && (
          <View style={styles.securityNote}>
            <Ionicons name="shield-checkmark" size={24} color="#10b981" />
            <View style={styles.securityNoteContent}>
              <Text style={styles.securityNoteTitle}>Safe & Secure</Text>
              <Text style={styles.securityNoteText}>
                This APK is built directly from our source code using Expo Application Services (EAS). It's the same app that will be on Google Play Store.
              </Text>
            </View>
          </View>
        )}

        {/* App Store Coming Soon */}
        <View style={styles.comingSoonSection}>
          <View style={styles.comingSoonBadge}>
            <Ionicons name="storefront-outline" size={20} color="#94a3b8" />
            <Text style={styles.comingSoonText}>Google Play & App Store versions coming soon!</Text>
          </View>
        </View>

        <View style={styles.bottomPadding} />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0c0c0c',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#1e293b',
  },
  backButton: {
    padding: 8,
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#fff',
  },
  placeholder: {
    width: 40,
  },
  scrollView: {
    flex: 1,
  },
  heroSection: {
    alignItems: 'center',
    paddingHorizontal: 24,
    paddingTop: 32,
    paddingBottom: 24,
  },
  iconContainer: {
    width: 96,
    height: 96,
    borderRadius: 24,
    backgroundColor: '#1e3a8a',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 20,
  },
  heroTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 12,
    textAlign: 'center',
  },
  heroSubtitle: {
    fontSize: 16,
    color: '#94a3b8',
    textAlign: 'center',
    lineHeight: 24,
  },
  benefitsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'center',
    paddingHorizontal: 16,
    gap: 12,
    marginBottom: 24,
  },
  benefitItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    backgroundColor: '#064e3b',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 20,
  },
  benefitText: {
    color: '#10b981',
    fontSize: 12,
    fontWeight: '500',
  },
  deviceSelector: {
    flexDirection: 'row',
    marginHorizontal: 24,
    gap: 12,
    marginBottom: 16,
  },
  deviceButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    paddingVertical: 16,
    borderRadius: 12,
    backgroundColor: '#1e293b',
    borderWidth: 2,
    borderColor: '#334155',
  },
  deviceButtonActive: {
    backgroundColor: '#1e3a8a',
    borderColor: '#3b82f6',
  },
  deviceButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#64748b',
  },
  deviceButtonTextActive: {
    color: '#fff',
  },
  apkSection: {
    paddingHorizontal: 24,
    marginBottom: 20,
  },
  apkCard: {
    backgroundColor: '#14532d',
    borderRadius: 16,
    padding: 20,
    borderWidth: 2,
    borderColor: '#22c55e',
  },
  apkIconRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  apkIconContainer: {
    width: 56,
    height: 56,
    borderRadius: 12,
    backgroundColor: '#1e293b',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  apkInfo: {
    flex: 1,
  },
  apkTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
  },
  apkVersion: {
    fontSize: 14,
    color: '#86efac',
    marginTop: 2,
  },
  downloadButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 10,
    backgroundColor: '#22c55e',
    paddingVertical: 14,
    borderRadius: 12,
  },
  downloadButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  browserNote: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 8,
    backgroundColor: '#78350f',
    marginHorizontal: 24,
    padding: 12,
    borderRadius: 10,
    marginBottom: 20,
  },
  browserNoteText: {
    flex: 1,
    color: '#fcd34d',
    fontSize: 14,
    lineHeight: 20,
  },
  stepsContainer: {
    paddingHorizontal: 24,
    marginBottom: 24,
  },
  stepsTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 16,
  },
  stepItem: {
    flexDirection: 'row',
    marginBottom: 16,
  },
  stepNumber: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: '#3b82f6',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  stepNumberText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
  },
  stepContent: {
    flex: 1,
  },
  stepHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 4,
  },
  stepTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#fff',
  },
  stepDescription: {
    fontSize: 14,
    color: '#94a3b8',
    lineHeight: 20,
    marginLeft: 28,
  },
  securityNote: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 12,
    backgroundColor: '#064e3b',
    marginHorizontal: 24,
    padding: 16,
    borderRadius: 12,
    marginBottom: 16,
  },
  securityNoteContent: {
    flex: 1,
  },
  securityNoteTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#10b981',
    marginBottom: 4,
  },
  securityNoteText: {
    color: '#86efac',
    fontSize: 13,
    lineHeight: 18,
  },
  comingSoonSection: {
    alignItems: 'center',
    paddingHorizontal: 24,
    marginBottom: 24,
  },
  comingSoonBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    backgroundColor: '#334155',
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderRadius: 20,
  },
  comingSoonText: {
    color: '#94a3b8',
    fontSize: 13,
    fontStyle: 'italic',
  },
  bottomPadding: {
    height: 40,
  },
});
