import React from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  Linking,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';

export default function Troubleshoot() {
  const router = useRouter();

  const openEmail = () => {
    Linking.openURL('mailto:njwarner25@gmail.com?subject=CPD Study Guide - Login Issue');
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
          <Ionicons name="arrow-back" size={24} color="#fff" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Troubleshooting</Text>
        <View style={styles.placeholder} />
      </View>

      <ScrollView style={styles.scrollView} contentContainerStyle={styles.content}>
        <View style={styles.iconContainer}>
          <Ionicons name="help-circle" size={64} color="#2563eb" />
        </View>

        <Text style={styles.title}>Can't Login or Create Account?</Text>
        <Text style={styles.subtitle}>Try these solutions</Text>

        {/* Solution 1 */}
        <View style={styles.solutionCard}>
          <View style={styles.solutionHeader}>
            <View style={styles.numberBadge}>
              <Text style={styles.numberText}>1</Text>
            </View>
            <Text style={styles.solutionTitle}>Check Your Internet Connection</Text>
          </View>
          <Text style={styles.solutionText}>
            • Make sure you have a stable internet connection (WiFi or mobile data){'\n'}
            • Try opening other websites to verify your connection{'\n'}
            • If on mobile data, ensure you have good signal strength
          </Text>
        </View>

        {/* Solution 2 */}
        <View style={styles.solutionCard}>
          <View style={styles.solutionHeader}>
            <View style={styles.numberBadge}>
              <Text style={styles.numberText}>2</Text>
            </View>
            <Text style={styles.solutionTitle}>Clear Browser Cache (Web Users)</Text>
          </View>
          <Text style={styles.solutionText}>
            <Text style={styles.bold}>For Chrome/Android:</Text>{'\n'}
            • Tap the three dots menu{'\n'}
            • Go to Settings → Privacy → Clear browsing data{'\n'}
            • Select "Cached images and files"{'\n'}
            • Tap "Clear data"{'\n\n'}
            
            <Text style={styles.bold}>For Safari/iPhone:</Text>{'\n'}
            • Settings → Safari → Clear History and Website Data
          </Text>
        </View>

        {/* Solution 3 */}
        <View style={styles.solutionCard}>
          <View style={styles.solutionHeader}>
            <View style={styles.numberBadge}>
              <Text style={styles.numberText}>3</Text>
            </View>
            <Text style={styles.solutionTitle}>Use Guest Mode (Temporary Access)</Text>
          </View>
          <Text style={styles.solutionText}>
            If you can't create an account right now:{'\n\n'}
            • Tap "Continue as Guest" on the login screen{'\n'}
            • This gives you immediate access to all study materials{'\n'}
            • You can create an account later to save your progress
          </Text>
        </View>

        {/* Solution 4 */}
        <View style={styles.solutionCard}>
          <View style={styles.solutionHeader}>
            <View style={styles.numberBadge}>
              <Text style={styles.numberText}>4</Text>
            </View>
            <Text style={styles.solutionTitle}>Wait and Retry (Server Starting)</Text>
          </View>
          <Text style={styles.solutionText}>
            If you see "Connection timed out":{'\n\n'}
            • The server may be waking up (first-time access){'\n'}
            • Wait 10-15 seconds{'\n'}
            • Tap "Try Again" or refresh the page{'\n'}
            • The app should load on the second attempt
          </Text>
        </View>

        {/* Solution 5 */}
        <View style={styles.solutionCard}>
          <View style={styles.solutionHeader}>
            <View style={styles.numberBadge}>
              <Text style={styles.numberText}>5</Text>
            </View>
            <Text style={styles.solutionTitle}>Try a Different Browser/Device</Text>
          </View>
          <Text style={styles.solutionText}>
            • Try Chrome, Firefox, or Safari{'\n'}
            • Use incognito/private browsing mode{'\n'}
            • Test on a different device if available
          </Text>
        </View>

        {/* Solution 6 - APK Users */}
        <View style={styles.solutionCard}>
          <View style={styles.solutionHeader}>
            <View style={styles.numberBadge}>
              <Text style={styles.numberText}>6</Text>
            </View>
            <Text style={styles.solutionTitle}>APK Users: Download Latest Version</Text>
          </View>
          <Text style={styles.solutionText}>
            If using the Android app:{'\n\n'}
            • Make sure you have the latest APK version{'\n'}
            • Uninstall the old version first{'\n'}
            • Download and install the newest version{'\n'}
            • Latest version should be 1.5.0 or higher
          </Text>
        </View>

        {/* Still Having Issues */}
        <View style={styles.contactCard}>
          <Ionicons name="mail" size={32} color="#2563eb" />
          <Text style={styles.contactTitle}>Still Having Issues?</Text>
          <Text style={styles.contactText}>
            If none of these solutions work, please contact support:
          </Text>
          <TouchableOpacity style={styles.emailButton} onPress={openEmail}>
            <Ionicons name="mail-outline" size={20} color="#fff" />
            <Text style={styles.emailButtonText}>Email Support</Text>
          </TouchableOpacity>
          <Text style={styles.emailText}>njwarner25@gmail.com</Text>
        </View>

        {/* Common Error Messages */}
        <View style={styles.errorsCard}>
          <Text style={styles.errorsTitle}>Common Error Messages:</Text>
          
          <View style={styles.errorItem}>
            <Text style={styles.errorMessage}>"Network error. Please check your internet connection."</Text>
            <Text style={styles.errorSolution}>→ Follow steps 1, 2, and 4 above</Text>
          </View>

          <View style={styles.errorItem}>
            <Text style={styles.errorMessage}>"Email already registered"</Text>
            <Text style={styles.errorSolution}>→ Use the login page instead, or use "Forgot Password"</Text>
          </View>

          <View style={styles.errorItem}>
            <Text style={styles.errorMessage}>"Connection timed out"</Text>
            <Text style={styles.errorSolution}>→ Wait 15 seconds and try again (server starting up)</Text>
          </View>

          <View style={styles.errorItem}>
            <Text style={styles.errorMessage}>"Password must be at least 6 characters"</Text>
            <Text style={styles.errorSolution}>→ Create a longer password (minimum 6 characters)</Text>
          </View>
        </View>
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
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#1e293b',
  },
  backButton: {
    padding: 8,
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
  },
  placeholder: {
    width: 40,
  },
  scrollView: {
    flex: 1,
  },
  content: {
    padding: 20,
    paddingBottom: 40,
  },
  iconContainer: {
    alignItems: 'center',
    marginBottom: 20,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    textAlign: 'center',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#94a3b8',
    textAlign: 'center',
    marginBottom: 32,
  },
  solutionCard: {
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 20,
    marginBottom: 16,
    borderLeftWidth: 4,
    borderLeftColor: '#2563eb',
  },
  solutionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    marginBottom: 12,
  },
  numberBadge: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: '#2563eb',
    justifyContent: 'center',
    alignItems: 'center',
  },
  numberText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  solutionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#fff',
    flex: 1,
  },
  solutionText: {
    fontSize: 14,
    color: '#cbd5e1',
    lineHeight: 22,
  },
  bold: {
    fontWeight: '600',
    color: '#fff',
  },
  contactCard: {
    backgroundColor: '#1e3a8a',
    borderRadius: 16,
    padding: 24,
    alignItems: 'center',
    marginTop: 16,
    marginBottom: 24,
  },
  contactTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
    marginTop: 12,
    marginBottom: 8,
  },
  contactText: {
    fontSize: 14,
    color: '#cbd5e1',
    textAlign: 'center',
    marginBottom: 16,
  },
  emailButton: {
    backgroundColor: '#2563eb',
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 12,
    marginBottom: 8,
  },
  emailButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  emailText: {
    fontSize: 12,
    color: '#94a3b8',
  },
  errorsCard: {
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 20,
  },
  errorsTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 16,
  },
  errorItem: {
    marginBottom: 16,
    paddingBottom: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#334155',
  },
  errorMessage: {
    fontSize: 14,
    color: '#fca5a5',
    fontStyle: 'italic',
    marginBottom: 6,
  },
  errorSolution: {
    fontSize: 13,
    color: '#94a3b8',
  },
});
