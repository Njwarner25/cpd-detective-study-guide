import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Image } from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';

// Chicago Police Star Badge - 5-pointed gold star design (authentic style)
const ChicagoPoliceStar = () => (
  <View style={starStyles.container}>
    <View style={starStyles.starWrapper}>
      {/* 5-pointed star using SVG-like approach */}
      <View style={starStyles.starOuter}>
        {/* Star points */}
        <View style={[starStyles.point, starStyles.pointTop]} />
        <View style={[starStyles.point, starStyles.pointTopRight]} />
        <View style={[starStyles.point, starStyles.pointBottomRight]} />
        <View style={[starStyles.point, starStyles.pointBottomLeft]} />
        <View style={[starStyles.point, starStyles.pointTopLeft]} />
        
        {/* Center circle with Chicago seal */}
        <View style={starStyles.centerCircle}>
          <View style={starStyles.innerRing}>
            <Text style={starStyles.topText}>CHICAGO</Text>
            <View style={starStyles.sealCenter}>
              <Text style={starStyles.sealText}>★</Text>
            </View>
            <Text style={starStyles.bottomText}>POLICE</Text>
          </View>
        </View>
      </View>
    </View>
  </View>
);

const starStyles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 24,
  },
  starWrapper: {
    width: 150,
    height: 150,
    alignItems: 'center',
    justifyContent: 'center',
  },
  starOuter: {
    width: 140,
    height: 140,
    alignItems: 'center',
    justifyContent: 'center',
    position: 'relative',
  },
  point: {
    position: 'absolute',
    width: 0,
    height: 0,
    borderLeftWidth: 20,
    borderRightWidth: 20,
    borderBottomWidth: 55,
    borderLeftColor: 'transparent',
    borderRightColor: 'transparent',
    borderBottomColor: '#CFB53B', // Classic gold
  },
  pointTop: {
    top: -8,
  },
  pointTopRight: {
    top: 28,
    right: -2,
    transform: [{ rotate: '72deg' }],
  },
  pointBottomRight: {
    bottom: 5,
    right: 12,
    transform: [{ rotate: '144deg' }],
  },
  pointBottomLeft: {
    bottom: 5,
    left: 12,
    transform: [{ rotate: '-144deg' }],
  },
  pointTopLeft: {
    top: 28,
    left: -2,
    transform: [{ rotate: '-72deg' }],
  },
  centerCircle: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#CFB53B',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 10,
    borderWidth: 2,
    borderColor: '#8B7500',
  },
  innerRing: {
    width: 68,
    height: 68,
    borderRadius: 34,
    backgroundColor: '#1B3D6D', // Navy blue
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 2,
    borderColor: '#CFB53B',
  },
  topText: {
    color: '#CFB53B',
    fontSize: 10,
    fontWeight: 'bold',
    letterSpacing: 1,
    marginTop: 2,
  },
  sealCenter: {
    width: 28,
    height: 28,
    borderRadius: 14,
    backgroundColor: '#CFB53B',
    alignItems: 'center',
    justifyContent: 'center',
    marginVertical: 2,
  },
  sealText: {
    color: '#1B3D6D',
    fontSize: 16,
    fontWeight: 'bold',
  },
  bottomText: {
    color: '#CFB53B',
    fontSize: 9,
    fontWeight: 'bold',
    letterSpacing: 1.5,
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
