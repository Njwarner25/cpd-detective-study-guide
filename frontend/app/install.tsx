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

  const appUrl = 'https://cpd-study.emergent.app';

  const androidSteps = [
    {
      icon: 'logo-chrome' as const,
      title: 'Open Chrome Browser',
      description: 'Launch Google Chrome on your Android device',
    },
    {
      icon: 'globe-outline' as const,
      title: 'Visit the App URL',
      description: `Go to ${appUrl}`,
    },
    {
      icon: 'ellipsis-vertical' as const,
      title: 'Tap the Menu (⋮)',
      description: 'Tap the three dots in the top-right corner of Chrome',
    },
    {
      icon: 'add-circle-outline' as const,
      title: 'Select "Add to Home screen"',
      description: 'Find and tap "Add to Home screen" in the menu',
    },
    {
      icon: 'checkmark-circle' as const,
      title: 'Confirm Installation',
      description: 'Tap "Add" to place the app on your home screen',
    },
    {
      icon: 'apps-outline' as const,
      title: 'Launch the App',
      description: 'Find the CPD Study Guide icon on your home screen and tap to open!',
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
      title: 'Visit the App URL',
      description: `Go to ${appUrl}`,
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

  const steps = selectedDevice === 'android' ? androidSteps : iosSteps;

  const handleOpenInBrowser = () => {
    Linking.openURL(appUrl);
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
            Add the CPD Detective Study Guide to your home screen for quick access - works just like a native app!
          </Text>
        </View>

        {/* Benefits */}
        <View style={styles.benefitsContainer}>
          <View style={styles.benefitItem}>
            <Ionicons name="flash" size={20} color="#10b981" />
            <Text style={styles.benefitText}>Instant access from home screen</Text>
          </View>
          <View style={styles.benefitItem}>
            <Ionicons name="cellular" size={20} color="#10b981" />
            <Text style={styles.benefitText}>Works offline after first load</Text>
          </View>
          <View style={styles.benefitItem}>
            <Ionicons name="resize" size={20} color="#10b981" />
            <Text style={styles.benefitText}>Full-screen experience</Text>
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

        {/* Browser Note */}
        <View style={styles.browserNote}>
          <Ionicons 
            name={selectedDevice === 'android' ? 'logo-chrome' : 'compass-outline'} 
            size={18} 
            color="#f59e0b" 
          />
          <Text style={styles.browserNoteText}>
            {selectedDevice === 'android' 
              ? 'Use Chrome browser for best results' 
              : 'Important: This only works in Safari browser'}
          </Text>
        </View>

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

        {/* Copy URL Section */}
        <View style={styles.urlSection}>
          <Text style={styles.urlLabel}>App URL:</Text>
          <View style={styles.urlContainer}>
            <Text style={styles.urlText}>{appUrl}</Text>
          </View>
          <TouchableOpacity style={styles.openButton} onPress={handleOpenInBrowser}>
            <Ionicons name="open-outline" size={20} color="#fff" />
            <Text style={styles.openButtonText}>Open in Browser</Text>
          </TouchableOpacity>
        </View>

        {/* Help Note */}
        <View style={styles.helpNote}>
          <Ionicons name="information-circle" size={24} color="#64748b" />
          <Text style={styles.helpNoteText}>
            The installed app works exactly like a native app - it opens in full screen and can be accessed from your home screen anytime!
          </Text>
        </View>

        {/* App Store Coming Soon */}
        <View style={styles.comingSoonSection}>
          <View style={styles.comingSoonBadge}>
            <Ionicons name="storefront-outline" size={20} color="#94a3b8" />
            <Text style={styles.comingSoonText}>App Store & Play Store versions coming soon!</Text>
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
  browserNote: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    backgroundColor: '#78350f',
    marginHorizontal: 24,
    padding: 12,
    borderRadius: 10,
    marginBottom: 24,
  },
  browserNoteText: {
    flex: 1,
    color: '#fcd34d',
    fontSize: 14,
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
  urlSection: {
    backgroundColor: '#1e293b',
    marginHorizontal: 24,
    padding: 16,
    borderRadius: 12,
    marginBottom: 16,
  },
  urlLabel: {
    fontSize: 12,
    color: '#64748b',
    textTransform: 'uppercase',
    marginBottom: 8,
  },
  urlContainer: {
    backgroundColor: '#0f172a',
    padding: 12,
    borderRadius: 8,
    marginBottom: 12,
  },
  urlText: {
    color: '#3b82f6',
    fontSize: 14,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
  },
  openButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    backgroundColor: '#3b82f6',
    paddingVertical: 12,
    borderRadius: 10,
  },
  openButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  helpNote: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 12,
    backgroundColor: '#1e293b',
    marginHorizontal: 24,
    padding: 16,
    borderRadius: 12,
    marginBottom: 16,
  },
  helpNoteText: {
    flex: 1,
    color: '#94a3b8',
    fontSize: 14,
    lineHeight: 20,
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
