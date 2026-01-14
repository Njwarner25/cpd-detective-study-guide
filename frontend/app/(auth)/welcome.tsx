import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';

export default function Welcome() {
  const router = useRouter();

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <View style={styles.header}>
          <Ionicons name="shield-checkmark" size={80} color="#2563eb" />
          <Text style={styles.title}>CPD Detective Exam</Text>
          <Text style={styles.subtitle}>Study Guide</Text>
          <Text style={styles.description}>
            Prepare for the Chicago Police Department Detective Exam with flashcards, scenarios, and AI-powered grading
          </Text>
          <Text style={styles.createdBy}>Created by Nathaniel Warner</Text>
        </View>

        <View style={styles.buttonContainer}>
          <TouchableOpacity 
            style={styles.loginButton}
            onPress={() => router.push('/(auth)/login')}
          >
            <Ionicons name="log-in" size={20} color="#fff" />
            <Text style={styles.loginButtonText}>Login to Study</Text>
          </TouchableOpacity>
          
          <View style={styles.credentialsBox}>
            <Ionicons name="information-circle" size={20} color="#64748b" />
            <View style={styles.credentialsText}>
              <Text style={styles.credentialsLabel}>Universal Login</Text>
              <Text style={styles.credentialsDetail}>Username: Detective2026</Text>
              <Text style={styles.credentialsDetail}>Password: Exam2026</Text>
            </View>
          </View>
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
    marginTop: 60,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#fff',
    marginTop: 16,
  },
  subtitle: {
    fontSize: 24,
    color: '#94a3b8',
    marginTop: 4,
  },
  description: {
    fontSize: 16,
    color: '#64748b',
    textAlign: 'center',
    marginTop: 16,
    paddingHorizontal: 20,
    lineHeight: 24,
  },
  createdBy: {
    fontSize: 14,
    color: '#94a3b8',
    textAlign: 'center',
    marginTop: 16,
    fontStyle: 'italic',
  },
  buttonContainer: {
    gap: 16,
  },
  loginButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#2563eb',
    padding: 16,
    borderRadius: 12,
    gap: 8,
  },
  loginButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
  credentialsBox: {
    flexDirection: 'row',
    backgroundColor: '#1e293b',
    padding: 16,
    borderRadius: 12,
    gap: 12,
    borderWidth: 1,
    borderColor: '#334155',
  },
  credentialsText: {
    flex: 1,
    gap: 4,
  },
  credentialsLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#cbd5e1',
    marginBottom: 4,
  },
  credentialsDetail: {
    fontSize: 13,
    color: '#94a3b8',
    fontFamily: 'monospace',
  },
});