import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import { useAuth } from '../../contexts/AuthContext';

export default function Tests() {
  const router = useRouter();
  const { isGuest } = useAuth();

  const testOptions = [
    {
      id: '25',
      title: '25 Question Quiz',
      description: 'Quick practice test',
      duration: '~15 min',
      icon: 'flash',
      color: '#10b981',
    },
    {
      id: '50',
      title: '50 Question Test',
      description: 'Standard practice exam',
      duration: '~30 min',
      icon: 'document-text',
      color: '#f59e0b',
    },
    {
      id: '75',
      title: '75 Question Exam',
      description: 'Full-length practice',
      duration: '~45 min',
      icon: 'school',
      color: '#ef4444',
    },
  ];

  const startTest = (count: string) => {
    router.push(`/quiz?count=${count}`);
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Practice Tests</Text>
        <Text style={styles.headerSubtitle}>Multiple Choice Exams</Text>
      </View>

      <ScrollView style={styles.scrollView} contentContainerStyle={styles.scrollContent}>
        {isGuest && (
          <View style={styles.guestBanner}>
            <Ionicons name="information-circle" size={20} color="#f59e0b" />
            <Text style={styles.guestText}>Guest progress is not saved. Register to track your scores!</Text>
          </View>
        )}

        <View style={styles.infoCard}>
          <Ionicons name="bulb" size={24} color="#60a5fa" />
          <View style={styles.infoContent}>
            <Text style={styles.infoTitle}>About These Tests</Text>
            <Text style={styles.infoText}>
              Each test pulls random questions from our database of 160+ multiple choice questions covering Illinois criminal law, constitutional law, and CPD procedures. Includes 100 questions based on previous practice from the testing company. Some questions may have multiple correct answers.
            </Text>
          </View>
        </View>

        {/* Practice Test Badge */}
        <View style={styles.practiceTestBadge}>
          <Ionicons name="star" size={18} color="#fbbf24" />
          <Text style={styles.practiceTestText}>
            100 Practice Test Questions from the testing company included!
          </Text>
        </View>

        <Text style={styles.sectionTitle}>Select Test Length</Text>

        {testOptions.map((test) => (
          <TouchableOpacity
            key={test.id}
            style={styles.testCard}
            onPress={() => startTest(test.id)}
          >
            <View style={[styles.testIcon, { backgroundColor: test.color + '20' }]}>
              <Ionicons name={test.icon as any} size={28} color={test.color} />
            </View>
            <View style={styles.testContent}>
              <Text style={styles.testTitle}>{test.title}</Text>
              <Text style={styles.testDescription}>{test.description}</Text>
              <View style={styles.testMeta}>
                <Ionicons name="time-outline" size={14} color="#64748b" />
                <Text style={styles.testDuration}>{test.duration}</Text>
              </View>
            </View>
            <Ionicons name="chevron-forward" size={24} color="#64748b" />
          </TouchableOpacity>
        ))}

        <View style={styles.tipsCard}>
          <Text style={styles.tipsTitle}>Test Taking Tips</Text>
          <View style={styles.tip}>
            <Ionicons name="checkmark-circle" size={16} color="#10b981" />
            <Text style={styles.tipText}>Read each question carefully before answering</Text>
          </View>
          <View style={styles.tip}>
            <Ionicons name="checkmark-circle" size={16} color="#10b981" />
            <Text style={styles.tipText}>Look for keywords like "always," "never," and "except"</Text>
          </View>
          <View style={styles.tip}>
            <Ionicons name="checkmark-circle" size={16} color="#10b981" />
            <Text style={styles.tipText}>Eliminate obviously wrong answers first</Text>
          </View>
          <View style={styles.tip}>
            <Ionicons name="checkmark-circle" size={16} color="#10b981" />
            <Text style={styles.tipText}>70% is the passing score on the actual exam</Text>
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
    padding: 20,
    paddingBottom: 12,
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
  },
  headerSubtitle: {
    fontSize: 16,
    color: '#64748b',
    marginTop: 4,
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    padding: 16,
    paddingTop: 8,
  },
  guestBanner: {
    backgroundColor: '#78350f',
    borderRadius: 8,
    padding: 12,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 16,
  },
  guestText: {
    color: '#fcd34d',
    fontSize: 13,
    flex: 1,
  },
  infoCard: {
    backgroundColor: '#1e293b',
    borderRadius: 12,
    padding: 16,
    flexDirection: 'row',
    gap: 12,
    marginBottom: 24,
  },
  infoContent: {
    flex: 1,
  },
  infoTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#fff',
    marginBottom: 4,
  },
  infoText: {
    fontSize: 14,
    color: '#94a3b8',
    lineHeight: 20,
  },
  practiceTestBadge: {
    backgroundColor: '#422006',
    borderRadius: 8,
    padding: 12,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 24,
    borderWidth: 1,
    borderColor: '#fbbf24',
  },
  practiceTestText: {
    color: '#fcd34d',
    fontSize: 14,
    fontWeight: '600',
    flex: 1,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#fff',
    marginBottom: 12,
  },
  testCard: {
    backgroundColor: '#1e293b',
    borderRadius: 12,
    padding: 16,
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  testIcon: {
    width: 56,
    height: 56,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  testContent: {
    flex: 1,
  },
  testTitle: {
    fontSize: 17,
    fontWeight: '600',
    color: '#fff',
  },
  testDescription: {
    fontSize: 14,
    color: '#94a3b8',
    marginTop: 2,
  },
  testMeta: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    marginTop: 6,
  },
  testDuration: {
    fontSize: 13,
    color: '#64748b',
  },
  tipsCard: {
    backgroundColor: '#1e293b',
    borderRadius: 12,
    padding: 16,
    marginTop: 12,
  },
  tipsTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#fff',
    marginBottom: 12,
  },
  tip: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 8,
    marginBottom: 8,
  },
  tipText: {
    fontSize: 14,
    color: '#94a3b8',
    flex: 1,
  },
});