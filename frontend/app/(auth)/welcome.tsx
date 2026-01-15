import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Image } from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';

// Chicago Police Star Badge SVG as a component
const ChicagoPoliceStar = () => (
  <View style={starStyles.container}>
    <View style={starStyles.star}>
      <View style={starStyles.centerCircle}>
        <Text style={starStyles.cityText}>CITY OF</Text>
        <Text style={starStyles.chicagoText}>CHICAGO</Text>
        <View style={starStyles.divider} />
        <Text style={starStyles.policeText}>POLICE</Text>
      </View>
      {/* Star points */}
      <View style={[starStyles.point, starStyles.pointTop]} />
      <View style={[starStyles.point, starStyles.pointTopRight]} />
      <View style={[starStyles.point, starStyles.pointBottomRight]} />
      <View style={[starStyles.point, starStyles.pointBottom]} />
      <View style={[starStyles.point, starStyles.pointBottomLeft]} />
      <View style={[starStyles.point, starStyles.pointTopLeft]} />
    </View>
  </View>
);

const starStyles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 20,
  },
  star: {
    width: 120,
    height: 120,
    alignItems: 'center',
    justifyContent: 'center',
    position: 'relative',
  },
  centerCircle: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#1e3a5f',
    borderWidth: 3,
    borderColor: '#c9a227',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 10,
  },
  cityText: {
    color: '#c9a227',
    fontSize: 8,
    fontWeight: 'bold',
    letterSpacing: 1,
  },
  chicagoText: {
    color: '#c9a227',
    fontSize: 12,
    fontWeight: 'bold',
    letterSpacing: 1,
  },
  divider: {
    width: 40,
    height: 1,
    backgroundColor: '#c9a227',
    marginVertical: 4,
  },
  policeText: {
    color: '#c9a227',
    fontSize: 10,
    fontWeight: 'bold',
    letterSpacing: 2,
  },
  point: {
    position: 'absolute',
    width: 0,
    height: 0,
    borderLeftWidth: 12,
    borderRightWidth: 12,
    borderBottomWidth: 30,
    borderLeftColor: 'transparent',
    borderRightColor: 'transparent',
    borderBottomColor: '#c9a227',
  },
  pointTop: {
    top: -5,
    transform: [{ rotate: '0deg' }],
  },
  pointTopRight: {
    top: 15,
    right: 5,
    transform: [{ rotate: '60deg' }],
  },
  pointBottomRight: {
    bottom: 15,
    right: 5,
    transform: [{ rotate: '120deg' }],
  },
  pointBottom: {
    bottom: -5,
    transform: [{ rotate: '180deg' }],
  },
  pointBottomLeft: {
    bottom: 15,
    left: 5,
    transform: [{ rotate: '240deg' }],
  },
  pointTopLeft: {
    top: 15,
    left: 5,
    transform: [{ rotate: '300deg' }],
  },
});

export default function Welcome() {
  const router = useRouter();

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <View style={styles.header}>
          <ChicagoPoliceStar />
          <Text style={styles.title}>CPD Detective Exam</Text>
          <Text style={styles.subtitle}>Study Guide</Text>
          <Text style={styles.description}>
            Prepare for the Chicago Police Department Detective Exam with flashcards, scenarios, multiple choice tests, and AI-powered grading
          </Text>
        </View>

        <View style={styles.features}>
          <View style={styles.featureRow}>
            <View style={styles.feature}>
              <Ionicons name="layers" size={24} color="#10b981" />
              <Text style={styles.featureText}>99+ Flashcards</Text>
            </View>
            <View style={styles.feature}>
              <Ionicons name="document-text" size={24} color="#f59e0b" />
              <Text style={styles.featureText}>12 Scenarios</Text>
            </View>
          </View>
          <View style={styles.featureRow}>
            <View style={styles.feature}>
              <Ionicons name="clipboard" size={24} color="#ef4444" />
              <Text style={styles.featureText}>60+ MCQs</Text>
            </View>
            <View style={styles.feature}>
              <Ionicons name="sparkles" size={24} color="#8b5cf6" />
              <Text style={styles.featureText}>AI Grading</Text>
            </View>
          </View>
        </View>

        <View style={styles.buttonContainer}>
          <TouchableOpacity 
            style={styles.loginButton}
            onPress={() => router.push('/(auth)/login')}
          >
            <Ionicons name="log-in" size={20} color="#fff" />
            <Text style={styles.loginButtonText}>Get Started</Text>
          </TouchableOpacity>

          <Text style={styles.createdBy}>Created by Nathaniel Warner</Text>
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0c0c0c',
  },
  content: {
    flex: 1,
    padding: 24,
    justifyContent: 'space-between',
  },
  header: {
    alignItems: 'center',
    marginTop: 40,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    marginTop: 8,
  },
  subtitle: {
    fontSize: 20,
    color: '#94a3b8',
    marginTop: 4,
  },
  description: {
    fontSize: 15,
    color: '#64748b',
    textAlign: 'center',
    marginTop: 16,
    paddingHorizontal: 10,
    lineHeight: 22,
  },
  features: {
    gap: 12,
  },
  featureRow: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 16,
  },
  feature: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    backgroundColor: '#1e293b',
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderRadius: 8,
    minWidth: 140,
  },
  featureText: {
    color: '#cbd5e1',
    fontSize: 14,
    fontWeight: '500',
  },
  buttonContainer: {
    gap: 16,
    alignItems: 'center',
  },
  loginButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#2563eb',
    padding: 16,
    borderRadius: 12,
    gap: 8,
    width: '100%',
  },
  loginButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
  createdBy: {
    fontSize: 13,
    color: '#64748b',
    textAlign: 'center',
    fontStyle: 'italic',
  },
});
