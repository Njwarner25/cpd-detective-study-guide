import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { feedbackService } from '../services/api';

const updates = [
  {
    version: '1.7.0',
    date: 'February 2026',
    title: 'Feedback Loop & Grading Improvements',
    features: [
      { icon: 'chatbox-ellipses', color: '#f59e0b', text: 'Feedback Feature - Report incorrect grades, suggest corrections, and flag missing info after any scenario' },
      { icon: 'checkmark-done', color: '#10b981', text: 'Admin Review - All feedback is reviewed by our team to continuously improve AI grading accuracy' },
      { icon: 'construct', color: '#8b5cf6', text: 'Your input matters - Help us make the grading better for everyone preparing for the detective exam' },
    ],
  },
  {
    version: '1.6.0',
    date: 'February 2026',
    title: 'Full Practice Exam & MCQ Tests',
    features: [
      { icon: 'trophy', color: '#8b5cf6', text: '105-Question Full Practice Exam - 90-minute timed test simulating actual CPD Detective exam' },
      { icon: 'flash', color: '#10b981', text: '25/50/75 Question MCQ Tests - Instant feedback showing correct/wrong answers' },
      { icon: 'checkmark-circle', color: '#22c55e', text: 'Real-time Answer Feedback - See if you got it right immediately with explanations' },
      { icon: 'book', color: '#60a5fa', text: '105 New Flashcards - Based on CPD General Orders and Special Orders' },
      { icon: 'shield', color: '#fbbf24', text: '23 Complex Detective Scenarios - Real-world case dilemmas with detailed responses' },
    ],
  },
  {
    version: '1.3.0',
    date: 'January 2025',
    title: 'Practice Test Content & Gold Scenarios',
    features: [
      { icon: 'star', color: '#fbbf24', text: '100 Practice MCQs - Based on previous questions that test administrators have used' },
      { icon: 'diamond', color: '#fbbf24', text: '5 Gold Scenarios - Premium practice scenarios including lineups, domestic violence, and more' },
      { icon: 'search', color: '#60a5fa', text: 'Lineup Questions - 10+ questions covering live lineups, photo lineups, and showups' },
      { icon: 'documents', color: '#10b981', text: 'Total content now: 163 MCQs, 20 Scenarios, 138 Flashcards' },
    ],
  },
  {
    version: '1.2.0',
    date: 'January 2025',
    title: 'Leaderboard & Score Reset',
    features: [
      { icon: 'trophy', color: '#fbbf24', text: 'Leaderboard - See how you rank against other test takers' },
      { icon: 'refresh', color: '#ef4444', text: 'Reset Scores - Start fresh with a clean slate' },
      { icon: 'shield-checkmark', color: '#10b981', text: 'Improved session handling - No more lost progress' },
    ],
  },
  {
    version: '1.1.0',
    date: 'January 2025',
    title: 'Complex Scenarios & Study Aids',
    features: [
      { icon: 'document-text', color: '#8b5cf6', text: '3 Complex Multi-Part Scenarios with 15-minute timers' },
      { icon: 'bulb', color: '#f59e0b', text: 'R.E.A.C.T.I.O.N. Framework - Organize your scenario responses' },
      { icon: 'time', color: '#60a5fa', text: 'Extended time limits for complex scenarios' },
    ],
  },
  {
    version: '1.0.0',
    date: 'January 2025',
    title: 'Initial Release',
    features: [
      { icon: 'layers', color: '#10b981', text: '138 Flashcards across 8 categories' },
      { icon: 'clipboard', color: '#f59e0b', text: '15 Practice Scenarios with AI grading' },
      { icon: 'checkbox', color: '#2563eb', text: '63 Multiple Choice Questions (some multi-answer)' },
      { icon: 'bookmark', color: '#ec4899', text: 'Bookmark system to save difficult questions' },
      { icon: 'person-add', color: '#8b5cf6', text: 'User registration with progress tracking' },
      { icon: 'sparkles', color: '#fbbf24', text: 'AI-powered scenario grading with feedback' },
    ],
  },
];

const upcomingFeatures = [
  { icon: 'analytics', text: 'Detailed performance analytics' },
  { icon: 'notifications', text: 'Study reminders and notifications' },
  { icon: 'people', text: 'Study groups and shared progress' },
  { icon: 'cloud-download', text: 'Offline mode for studying without internet' },
];

const feedbackTypeLabels: Record<string, string> = {
  incorrect_grade: 'Incorrect Grade',
  missing_info: 'Missing Info',
  wrong_procedure: 'Wrong Procedure',
  general: 'General',
};

export default function Updates() {
  const router = useRouter();
  const [corrections, setCorrections] = useState<any[]>([]);
  const [loadingCorrections, setLoadingCorrections] = useState(true);

  useEffect(() => {
    loadCorrections();
  }, []);

  const loadCorrections = async () => {
    try {
      const token = await AsyncStorage.getItem('session_token');
      if (token) {
        const data = await feedbackService.getCorrections(token);
        setCorrections(data.corrections || []);
      }
    } catch (err) {
      // Silently fail — corrections are not critical
    } finally {
      setLoadingCorrections(false);
    }
  };

  const formatDate = (dateStr: string) => {
    const d = new Date(dateStr);
    const now = new Date();
    const diffMs = now.getTime() - d.getTime();
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return 'Yesterday';
    if (diffDays < 7) return `${diffDays} days ago`;
    return d.toLocaleDateString();
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
          <Ionicons name="arrow-back" size={24} color="#fff" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>What's New</Text>
        <View style={styles.backButton} />
      </View>

      <ScrollView style={styles.scrollView} contentContainerStyle={styles.scrollContent}>
        {/* Approved Corrections from API */}
        {loadingCorrections ? (
          <View style={styles.correctionsLoading}>
            <ActivityIndicator size="small" color="#f59e0b" />
            <Text style={styles.correctionsLoadingText}>Loading corrections...</Text>
          </View>
        ) : corrections.length > 0 ? (
          <View style={styles.correctionsCard}>
            <View style={styles.correctionsHeader}>
              <Ionicons name="build" size={22} color="#f59e0b" />
              <Text style={styles.correctionsTitle}>Recent Fixes & Corrections</Text>
            </View>

            <Text style={styles.correctionsSubtitle}>
              These corrections were submitted by users and verified by our team. Shown for 7 days.
            </Text>

            {corrections.map((item: any, index: number) => (
              <View key={item.feedback_id} style={styles.correctionItem}>
                <Text style={styles.correctionNumber}>{index + 1}.</Text>
                <View style={styles.correctionContent}>
                  <Text style={styles.correctionQuestion}>
                    {item.question_title}
                  </Text>
                  <View style={styles.correctionTypeBadge}>
                    <Text style={styles.correctionTypeText}>
                      {feedbackTypeLabels[item.feedback_type] || item.feedback_type}
                    </Text>
                  </View>
                  <View style={styles.correctionAnswer}>
                    <Text style={styles.correctionUserMsg}>{item.user_message}</Text>
                    {item.admin_notes ? (
                      <View style={styles.adminNotesBox}>
                        <Text style={styles.adminNotesLabel}>Admin Note:</Text>
                        <Text style={styles.adminNotesText}>{item.admin_notes}</Text>
                      </View>
                    ) : null}
                  </View>
                  <Text style={styles.correctionDate}>
                    Verified {formatDate(item.reviewed_at)}
                  </Text>
                </View>
              </View>
            ))}
          </View>
        ) : null}

        {/* Current Version Banner */}
        <View style={styles.currentVersionBanner}>
          <View style={styles.versionBadge}>
            <Text style={styles.versionBadgeText}>v1.7.0</Text>
          </View>
          <Text style={styles.currentVersionText}>CPD Detective Exam Study Guide</Text>
          <Text style={styles.currentVersionSubtext}>Latest Version</Text>
        </View>

        {/* Update History */}
        {updates.map((update, index) => (
          <View key={index} style={styles.updateCard}>
            <View style={styles.updateHeader}>
              <View style={styles.updateTitleRow}>
                <Text style={styles.updateVersion}>Version {update.version}</Text>
                <Text style={styles.updateDate}>{update.date}</Text>
              </View>
              <Text style={styles.updateTitle}>{update.title}</Text>
            </View>
            <View style={styles.updateFeatures}>
              {update.features.map((feature, fIndex) => (
                <View key={fIndex} style={styles.featureItem}>
                  <View style={[styles.featureIcon, { backgroundColor: feature.color + '20' }]}>
                    <Ionicons name={feature.icon as any} size={18} color={feature.color} />
                  </View>
                  <Text style={styles.featureText}>{feature.text}</Text>
                </View>
              ))}
            </View>
          </View>
        ))}

        {/* Coming Soon */}
        <View style={styles.comingSoonCard}>
          <View style={styles.comingSoonHeader}>
            <Ionicons name="rocket" size={24} color="#8b5cf6" />
            <Text style={styles.comingSoonTitle}>Coming Soon</Text>
          </View>
          <View style={styles.comingSoonFeatures}>
            {upcomingFeatures.map((feature, index) => (
              <View key={index} style={styles.comingSoonItem}>
                <Ionicons name={feature.icon as any} size={18} color="#64748b" />
                <Text style={styles.comingSoonText}>{feature.text}</Text>
              </View>
            ))}
          </View>
        </View>

        {/* Feedback Section */}
        <View style={styles.feedbackCard}>
          <Ionicons name="chatbubble-ellipses" size={32} color="#2563eb" />
          <Text style={styles.feedbackTitle}>Have Feedback?</Text>
          <Text style={styles.feedbackText}>
            After completing any scenario, use the feedback button to report incorrect grades or suggest corrections. Your input helps improve the app for everyone.
          </Text>
        </View>

        {/* Credits */}
        <View style={styles.creditsSection}>
          <Text style={styles.creditsText}>Created by Nathaniel Warner</Text>
          <Text style={styles.creditsSubtext}>For CPD Detective Exam Preparation</Text>
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
  },
  backButton: {
    padding: 8,
    width: 40,
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    padding: 16,
    paddingBottom: 32,
  },
  correctionsLoading: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 10,
    padding: 20,
    marginBottom: 16,
  },
  correctionsLoadingText: {
    color: '#f59e0b',
    fontSize: 14,
  },
  correctionsCard: {
    backgroundColor: '#78350f',
    borderRadius: 16,
    padding: 20,
    marginBottom: 20,
    borderWidth: 2,
    borderColor: '#f59e0b',
  },
  correctionsHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    marginBottom: 12,
  },
  correctionsTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
  },
  correctionsSubtitle: {
    fontSize: 13,
    color: '#fcd34d',
    marginBottom: 16,
    lineHeight: 19,
  },
  correctionItem: {
    flexDirection: 'row',
    marginBottom: 20,
    gap: 12,
  },
  correctionNumber: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#f59e0b',
  },
  correctionContent: {
    flex: 1,
  },
  correctionQuestion: {
    fontSize: 15,
    color: '#fff',
    marginBottom: 8,
    lineHeight: 21,
    fontWeight: '600',
  },
  correctionTypeBadge: {
    backgroundColor: '#f59e0b22',
    paddingHorizontal: 10,
    paddingVertical: 3,
    borderRadius: 12,
    alignSelf: 'flex-start',
    marginBottom: 8,
  },
  correctionTypeText: {
    fontSize: 11,
    color: '#f59e0b',
    fontWeight: '700',
    textTransform: 'uppercase',
  },
  correctionAnswer: {
    backgroundColor: '#0c0c0c',
    padding: 14,
    borderRadius: 10,
    gap: 8,
  },
  correctionUserMsg: {
    fontSize: 14,
    color: '#e2e8f0',
    lineHeight: 20,
  },
  adminNotesBox: {
    borderTopWidth: 1,
    borderTopColor: '#334155',
    paddingTop: 8,
    marginTop: 4,
  },
  adminNotesLabel: {
    fontSize: 11,
    color: '#10b981',
    fontWeight: '700',
    textTransform: 'uppercase',
    marginBottom: 4,
  },
  adminNotesText: {
    fontSize: 13,
    color: '#86efac',
    lineHeight: 19,
  },
  correctionDate: {
    fontSize: 11,
    color: '#94a3b8',
    marginTop: 6,
    fontStyle: 'italic',
  },
  currentVersionBanner: {
    backgroundColor: '#1e3a8a',
    borderRadius: 16,
    padding: 24,
    alignItems: 'center',
    marginBottom: 20,
  },
  versionBadge: {
    backgroundColor: '#2563eb',
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
    marginBottom: 12,
  },
  versionBadgeText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  currentVersionText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  currentVersionSubtext: {
    color: '#93c5fd',
    fontSize: 14,
    marginTop: 4,
  },
  updateCard: {
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 16,
    marginBottom: 16,
  },
  updateHeader: {
    borderBottomWidth: 1,
    borderBottomColor: '#334155',
    paddingBottom: 12,
    marginBottom: 12,
  },
  updateTitleRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 4,
  },
  updateVersion: {
    color: '#2563eb',
    fontSize: 14,
    fontWeight: '600',
  },
  updateDate: {
    color: '#64748b',
    fontSize: 12,
  },
  updateTitle: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  updateFeatures: {
    gap: 12,
  },
  featureItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  featureIcon: {
    width: 36,
    height: 36,
    borderRadius: 10,
    justifyContent: 'center',
    alignItems: 'center',
  },
  featureText: {
    flex: 1,
    color: '#e2e8f0',
    fontSize: 14,
    lineHeight: 20,
  },
  comingSoonCard: {
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#8b5cf6',
    borderStyle: 'dashed',
  },
  comingSoonHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    marginBottom: 16,
  },
  comingSoonTitle: {
    color: '#8b5cf6',
    fontSize: 18,
    fontWeight: 'bold',
  },
  comingSoonFeatures: {
    gap: 12,
  },
  comingSoonItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  comingSoonText: {
    color: '#94a3b8',
    fontSize: 14,
  },
  feedbackCard: {
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 20,
    alignItems: 'center',
    marginBottom: 16,
  },
  feedbackTitle: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
    marginTop: 12,
    marginBottom: 8,
  },
  feedbackText: {
    color: '#94a3b8',
    fontSize: 14,
    textAlign: 'center',
    lineHeight: 20,
  },
  creditsSection: {
    alignItems: 'center',
    paddingVertical: 16,
  },
  creditsText: {
    color: '#64748b',
    fontSize: 14,
  },
  creditsSubtext: {
    color: '#475569',
    fontSize: 12,
    marginTop: 4,
  },
});
