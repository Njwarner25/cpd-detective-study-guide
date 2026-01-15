import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Image } from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';

// Chicago Police Star Badge - 6-pointed gold star design
const ChicagoPoliceStar = () => (
  <View style={starStyles.container}>
    {/* Outer star shape using positioned triangles */}
    <View style={starStyles.starContainer}>
      {/* Six points of the star */}
      <View style={[starStyles.point, starStyles.point0]} />
      <View style={[starStyles.point, starStyles.point1]} />
      <View style={[starStyles.point, starStyles.point2]} />
      <View style={[starStyles.point, starStyles.point3]} />
      <View style={[starStyles.point, starStyles.point4]} />
      <View style={[starStyles.point, starStyles.point5]} />
      
      {/* Center hexagon */}
      <View style={starStyles.centerHex}>
        {/* Inner circle with text */}
        <View style={starStyles.innerCircle}>
          <Text style={starStyles.chicagoText}>CHICAGO</Text>
          <View style={starStyles.shield}>
            <View style={starStyles.shieldStripe1} />
            <View style={starStyles.shieldStripe2} />
            <View style={starStyles.shieldStripe3} />
          </View>
          <Text style={starStyles.policeText}>POLICE</Text>
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
  starContainer: {
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
    borderLeftWidth: 18,
    borderRightWidth: 18,
    borderBottomWidth: 45,
    borderLeftColor: 'transparent',
    borderRightColor: 'transparent',
    borderBottomColor: '#D4AF37', // Gold color
  },
  point0: { // Top point
    top: 0,
    transform: [{ rotate: '0deg' }],
  },
  point1: { // Top-right
    top: 22,
    right: 8,
    transform: [{ rotate: '60deg' }],
  },
  point2: { // Bottom-right
    bottom: 22,
    right: 8,
    transform: [{ rotate: '120deg' }],
  },
  point3: { // Bottom
    bottom: 0,
    transform: [{ rotate: '180deg' }],
  },
  point4: { // Bottom-left
    bottom: 22,
    left: 8,
    transform: [{ rotate: '240deg' }],
  },
  point5: { // Top-left
    top: 22,
    left: 8,
    transform: [{ rotate: '300deg' }],
  },
  centerHex: {
    width: 90,
    height: 90,
    borderRadius: 45,
    backgroundColor: '#D4AF37',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 10,
  },
  innerCircle: {
    width: 76,
    height: 76,
    borderRadius: 38,
    backgroundColor: '#1a237e', // Deep blue
    borderWidth: 2,
    borderColor: '#D4AF37',
    alignItems: 'center',
    justifyContent: 'center',
  },
  chicagoText: {
    color: '#D4AF37',
    fontSize: 11,
    fontWeight: 'bold',
    letterSpacing: 1.5,
    marginTop: 4,
  },
  shield: {
    width: 24,
    height: 18,
    backgroundColor: '#fff',
    borderRadius: 2,
    marginVertical: 4,
    overflow: 'hidden',
    flexDirection: 'row',
  },
  shieldStripe1: {
    flex: 1,
    backgroundColor: '#bf0a30', // Red
  },
  shieldStripe2: {
    flex: 1,
    backgroundColor: '#fff', // White
  },
  shieldStripe3: {
    flex: 1,
    backgroundColor: '#002868', // Blue
  },
  policeText: {
    color: '#D4AF37',
    fontSize: 10,
    fontWeight: 'bold',
    letterSpacing: 2,
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
