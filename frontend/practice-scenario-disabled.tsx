import React, { useEffect, useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ScrollView, KeyboardAvoidingView, Platform, ActivityIndicator, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useAuth } from '../contexts/AuthContext';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { questionService, scenarioService, bookmarkService } from '../services/api';

const TIMER_DURATION = 7 * 60; // 7 minutes in seconds

export default function PracticeScenario() {
  const { sessionToken } = useAuth();
  const router = useRouter();
  const params = useLocalSearchParams();
  const [scenario, setScenario] = useState<any>(null);
  const [response, setResponse] = useState('');
  const [timeRemaining, setTimeRemaining] = useState(TIMER_DURATION);
  const [timerStarted, setTimerStarted] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [grading, setGrading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [bookmarked, setBookmarked] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadScenario();
  }, []);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (timerStarted && timeRemaining > 0 && !submitted) {
      interval = setInterval(() => {
        setTimeRemaining((prev) => {
          if (prev <= 1) {
            handleSubmit();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [timerStarted, timeRemaining, submitted]);

  const loadScenario = async () => {
    try {
      const scenarioId = params.scenarioId as string;
      const data = await questionService.getQuestion(scenarioId, sessionToken || undefined);
      setScenario(data);
      
      const progress = await bookmarkService.getProgress(scenarioId, sessionToken || undefined);
      setBookmarked(progress?.bookmarked || false);
    } catch (error) {
      console.error('Failed to load scenario:', error);
      Alert.alert('Error', 'Failed to load scenario');
      router.back();
    } finally {
      setLoading(false);
    }
  };

  const startTimer = () => {
    if (!timerStarted && response.length > 0) {
      setTimerStarted(true);
    }
  };

  const handleSubmit = async () => {
    if (submitted || grading) return;
    
    if (!response.trim()) {
      Alert.alert('Empty Response', 'Please provide a response before submitting.');
      return;
    }

    setGrading(true);
    setSubmitted(true);
    const timeTaken = TIMER_DURATION - timeRemaining;

    try {
      const gradingResult = await scenarioService.submitResponse(
        scenario.question_id,
        response,
        timeTaken,
        sessionToken || undefined
      );
      setResult(gradingResult);
    } catch (error) {
      console.error('Failed to submit scenario:', error);
      Alert.alert('Error', 'Failed to submit response. Please try again.');
      setSubmitted(false);
    } finally {
      setGrading(false);
    }
  };

  const toggleBookmark = async () => {
    try {
      const result = await bookmarkService.toggleBookmark(scenario.question_id, sessionToken || undefined);
      setBookmarked(result.bookmarked);
    } catch (error) {
      console.error('Failed to toggle bookmark:', error);
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getTimerColor = () => {
    if (timeRemaining > 120) return '#10b981';
    if (timeRemaining > 60) return '#f59e0b';
    return '#ef4444';
  };

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#2563eb" />
        </View>
      </SafeAreaView>
    );
  }

  if (!scenario) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.errorContainer}>
          <Ionicons name="alert-circle" size={64} color="#ef4444" />
          <Text style={styles.errorText}>Scenario not found</Text>
          <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
            <Text style={styles.backButtonText}>Go Back</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView 
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.keyboardView}
      >
        <View style={styles.header}>
          <TouchableOpacity onPress={() => router.back()} style={styles.headerButton}>
            <Ionicons name="arrow-back" size={24} color="#fff" />
          </TouchableOpacity>
          
          <View style={[styles.timerContainer, { backgroundColor: submitted ? '#1e293b' : getTimerColor() }]}>
            <Ionicons name="time" size={20} color="#fff" />
            <Text style={styles.timerText}>{formatTime(timeRemaining)}</Text>
          </View>
          
          <TouchableOpacity onPress={toggleBookmark} style={styles.headerButton}>
            <Ionicons 
              name={bookmarked ? "bookmark" : "bookmark-outline"} 
              size={24} 
              color={bookmarked ? "#f59e0b" : "#fff"} 
            />
          </TouchableOpacity>
        </View>

        <ScrollView style={styles.scrollView} contentContainerStyle={styles.scrollContent}>
          {/* Scenario Details */}
          <View style={styles.scenarioHeader}>
            <View style={styles.badgeRow}>
              <View style={[styles.badge, styles[`badge${scenario.difficulty}`]]}>
                <Text style={styles.badgeText}>{scenario.difficulty}</Text>
              </View>
              <Text style={styles.categoryBadge}>{scenario.category_name}</Text>
            </View>
            <Text style={styles.scenarioTitle}>{scenario.title}</Text>
            {scenario.reference && (
              <Text style={styles.reference}>{scenario.reference}</Text>
            )}
          </View>

          {/* Scenario Content */}
          <View style={styles.contentCard}>
            <Text style={styles.sectionLabel}>Scenario:</Text>
            <Text style={styles.scenarioContent}>{scenario.content}</Text>
          </View>

          {/* Response Input */}
          {!submitted ? (
            <View style={styles.responseCard}>
              <Text style={styles.sectionLabel}>Your Response:</Text>
              <TextInput
                style={styles.responseInput}
                placeholder="Type your detailed response here..."
                placeholderTextColor="#64748b"
                value={response}
                onChangeText={(text) => {
                  setResponse(text);
                  if (!timerStarted && text.length > 0) {
                    startTimer();
                  }
                }}
                multiline
                numberOfLines={12}
                textAlignVertical="top"
                editable={!submitted}
              />
              <Text style={styles.wordCount}>{response.split(/\s+/).filter(w => w).length} words</Text>
            </View>
          ) : (
            <>
              {/* User's Response */}
              <View style={styles.responseCard}>
                <Text style={styles.sectionLabel}>Your Response:</Text>
                <Text style={styles.submittedResponse}>{response}</Text>
              </View>

              {/* AI Grading Result */}
              {grading ? (
                <View style={styles.gradingCard}>
                  <ActivityIndicator size="large" color="#2563eb" />
                  <Text style={styles.gradingText}>AI is grading your response...</Text>
                  <Text style={styles.gradingSubtext}>This may take a moment</Text>
                </View>
              ) : result ? (
                <>
                  <View style={styles.gradeCard}>
                    <View style={styles.gradeHeader}>
                      <Ionicons name="ribbon" size={32} color="#f59e0b" />
                      <View>
                        <Text style={styles.gradeLabel}>Your Grade</Text>
                        {result.grade !== null && result.grade !== undefined ? (
                          <Text style={styles.gradeValue}>{Math.round(result.grade)}%</Text>
                        ) : (
                          <Text style={styles.gradeValue}>Pending</Text>
                        )}
                      </View>
                    </View>
                  </View>

                  <View style={styles.feedbackCard}>
                    <Text style={styles.sectionLabel}>AI Feedback:</Text>
                    <Text style={styles.feedbackText}>{result.feedback}</Text>
                  </View>

                  {scenario.answer && (
                    <View style={styles.answerCard}>
                      <Text style={styles.sectionLabel}>Model Answer:</Text>
                      <Text style={styles.answerText}>{scenario.answer}</Text>
                    </View>
                  )}
                </>
              ) : null}
            </>
          )}
        </ScrollView>

        {/* Submit Button */}
        {!submitted && (
          <View style={styles.footer}>
            <TouchableOpacity 
              style={[styles.submitButton, (!response.trim() || grading) && styles.submitButtonDisabled]}
              onPress={handleSubmit}
              disabled={!response.trim() || grading}
            >
              <Ionicons name="checkmark-circle" size={24} color="#fff" />
              <Text style={styles.submitButtonText}>Submit Response</Text>
            </TouchableOpacity>
          </View>
        )}

        {submitted && result && (
          <View style={styles.footer}>
            <TouchableOpacity 
              style={styles.doneButton}
              onPress={() => router.back()}
            >
              <Text style={styles.doneButtonText}>Done</Text>
            </TouchableOpacity>
          </View>
        )}
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0c0c0c',
  },
  keyboardView: {
    flex: 1,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    gap: 16,
  },
  errorText: {
    fontSize: 18,
    color: '#ef4444',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#1e293b',
  },
  headerButton: {
    padding: 8,
  },
  timerContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
  },
  timerText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    padding: 16,
    gap: 16,
  },
  scenarioHeader: {
    gap: 8,
  },
  badgeRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  badge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
  },
  badgeeasy: {
    backgroundColor: '#10b981',
  },
  badgemedium: {
    backgroundColor: '#f59e0b',
  },
  badgehard: {
    backgroundColor: '#ef4444',
  },
  badgeText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
    textTransform: 'capitalize',
  },
  categoryBadge: {
    fontSize: 12,
    color: '#64748b',
  },
  scenarioTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  reference: {
    fontSize: 12,
    color: '#94a3b8',
    fontStyle: 'italic',
  },
  contentCard: {
    backgroundColor: '#1e293b',
    padding: 16,
    borderRadius: 12,
    gap: 12,
  },
  responseCard: {
    backgroundColor: '#1e293b',
    padding: 16,
    borderRadius: 12,
    gap: 12,
  },
  sectionLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#3b82f6',
  },
  scenarioContent: {
    fontSize: 16,
    color: '#cbd5e1',
    lineHeight: 24,
  },
  responseInput: {
    backgroundColor: '#0f172a',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    color: '#fff',
    minHeight: 200,
    borderWidth: 1,
    borderColor: '#334155',
  },
  wordCount: {
    fontSize: 12,
    color: '#64748b',
    textAlign: 'right',
  },
  submittedResponse: {
    fontSize: 16,
    color: '#cbd5e1',
    lineHeight: 24,
  },
  gradingCard: {
    backgroundColor: '#1e293b',
    padding: 32,
    borderRadius: 12,
    alignItems: 'center',
    gap: 12,
  },
  gradingText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#fff',
  },
  gradingSubtext: {
    fontSize: 14,
    color: '#94a3b8',
  },
  gradeCard: {
    backgroundColor: '#1e293b',
    padding: 20,
    borderRadius: 12,
  },
  gradeHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 16,
  },
  gradeLabel: {
    fontSize: 14,
    color: '#94a3b8',
  },
  gradeValue: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#fff',
  },
  feedbackCard: {
    backgroundColor: '#1e293b',
    padding: 16,
    borderRadius: 12,
    gap: 12,
  },
  feedbackText: {
    fontSize: 16,
    color: '#cbd5e1',
    lineHeight: 24,
  },
  answerCard: {
    backgroundColor: '#1e293b',
    padding: 16,
    borderRadius: 12,
    gap: 12,
    borderLeftWidth: 4,
    borderLeftColor: '#10b981',
  },
  answerText: {
    fontSize: 16,
    color: '#cbd5e1',
    lineHeight: 24,
  },
  footer: {
    padding: 16,
    borderTopWidth: 1,
    borderTopColor: '#1e293b',
  },
  submitButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    backgroundColor: '#2563eb',
    padding: 16,
    borderRadius: 12,
  },
  submitButtonDisabled: {
    opacity: 0.5,
  },
  submitButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  doneButton: {
    backgroundColor: '#10b981',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  doneButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  backButton: {
    backgroundColor: '#2563eb',
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 8,
  },
  backButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});
