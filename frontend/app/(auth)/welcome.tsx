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
    gap: 12,
  },
  googleButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#dc2626',
    padding: 16,
    borderRadius: 12,
    gap: 8,
  },
  googleButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  divider: {
    flexDirection: 'row',
    alignItems: 'center',
    marginVertical: 8,
  },
  dividerLine: {
    flex: 1,
    height: 1,
    backgroundColor: '#334155',
  },
  dividerText: {
    color: '#64748b',
    marginHorizontal: 16,
    fontSize: 14,
  },
  loginButton: {
    backgroundColor: '#2563eb',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  loginButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  registerButton: {
    backgroundColor: 'transparent',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#334155',
  },
  registerButtonText: {
    color: '#e2e8f0',
    fontSize: 16,
    fontWeight: '600',
  },
});