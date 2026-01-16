import React, { useEffect, useState, useRef } from 'react';
import { 
  View, 
  Text, 
  TouchableOpacity, 
  StyleSheet, 
  TextInput, 
  ScrollView, 
  ActivityIndicator,
  Alert,
  KeyboardAvoidingView,
  Platform
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useAuth } from '../contexts/AuthContext';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { questionService, scenarioService } from '../services/api';

const TOTAL_TIME = 7 * 60; // Default 7 minutes in seconds

export default function PracticeScenario() {
  const { sessionToken } = useAuth();
  const router = useRouter();
  const params = useLocalSearchParams();
  const [scenario, setScenario] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [response, setResponse] = useState('');
  const [timeRemaining, setTimeRemaining] = useState(TOTAL_TIME);
  const [totalTime, setTotalTime] = useState(TOTAL_TIME);
  const [isStarted, setIsStarted] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<any>(null);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const startTimeRef = useRef<number>(0);

  useEffect(() => {
    loadScenario();
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, []);

  useEffect(() => {
    if (isStarted && !isSubmitted && timeRemaining > 0) {
      timerRef.current = setInterval(() => {
        setTimeRemaining(prev => {
          if (prev <= 1) {
            handleTimeUp();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, [isStarted, isSubmitted]);

  const loadScenario = async () => {
    try {
      const scenarioId = params.scenarioId as string;
      const data = await questionService.getQuestion(scenarioId, sessionToken || undefined);
      setScenario(data);
      // Set time limit from scenario data, default to 7 minutes
      const scenarioTime = data.time_limit || TOTAL_TIME;
      setTimeRemaining(scenarioTime);
      setTotalTime(scenarioTime);
    } catch (error) {
      console.error('Failed to load scenario:', error);
      Alert.alert('Error', 'Failed to load scenario');
    } finally {
      setLoading(false);
    }
  };

  const handleStart = () => {
    setIsStarted(true);
    startTimeRef.current = Date.now();
  };

  const handleTimeUp = () => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
    }
    if (!isSubmitted) {
      handleSubmit(true);
    }
  };

  const handleSubmit = async (timeUp: boolean = false) => {
    if (submitting) return;
    
    if (!timeUp && response.trim().length < 50) {
      Alert.alert('Response Too Short', 'Please provide a more detailed response (at least 50 characters).');
      return;
    }

    setSubmitting(true);
    if (timerRef.current) {
      clearInterval(timerRef.current);
    }

    const timeTaken = Math.round((Date.now() - startTimeRef.current) / 1000);

    try {
      const resultData = await scenarioService.submitResponse(
        scenario.question_id,
        response || 'No response provided - time expired',
        timeTaken,
        sessionToken || undefined
      );
      setResult(resultData);
      setIsSubmitted(true);
    } catch (error) {
      console.error('Failed to submit response:', error);
      Alert.alert('Error', 'Failed to submit response. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getTimerColor = () => {
    if (timeRemaining <= 60) return '#ef4444'; // Red for last minute
    if (timeRemaining <= 180) return '#f59e0b'; // Yellow for last 3 minutes
    return '#10b981'; // Green
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
        <View style={styles.header}>
          <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
            <Ionicons name="arrow-back" size={24} color="#fff" />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Scenario</Text>
          <View style={styles.backButton} />
        </View>
        <View style={styles.emptyContainer}>
          <Ionicons name="alert-circle-outline" size={64} color="#64748b" />
          <Text style={styles.emptyText}>Scenario not found</Text>
        </View>
      </SafeAreaView>
    );
  }

  // Result screen
  if (isSubmitted && result) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.header}>
          <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
            <Ionicons name="arrow-back" size={24} color="#fff" />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Results</Text>
          <View style={styles.backButton} />
        </View>
        <ScrollView style={styles.scrollView} contentContainerStyle={styles.scrollContent}>
          <View style={styles.resultCard}>
            <View style={styles.scoreContainer}>
              <Text style={styles.scoreLabel}>Your Score</Text>
              <Text style={[
                styles.scoreValue,
                { color: result.grade >= 70 ? '#10b981' : result.grade >= 50 ? '#f59e0b' : '#ef4444' }
              ]}>
                {result.grade !== null ? `${Math.round(result.grade)}%` : 'Pending'}
              </Text>
            </View>
            
            <View style={styles.divider} />
            
            <Text style={styles.feedbackLabel}>AI Feedback:</Text>
            <Text style={styles.feedbackText}>{result.feedback}</Text>
            
            <View style={styles.divider} />
            
            <Text style={styles.feedbackLabel}>Model Answer:</Text>
            <Text style={styles.modelAnswer}>{scenario.model_answer || scenario.answer}</Text>
          </View>

          <TouchableOpacity 
            style={styles.doneButton}
            onPress={() => router.back()}
          >
            <Text style={styles.doneButtonText}>Back to Scenarios</Text>
          </TouchableOpacity>
        </ScrollView>
      </SafeAreaView>
    );
  }

  // Start screen
  if (!isStarted) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.header}>
          <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
            <Ionicons name="arrow-back" size={24} color="#fff" />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Scenario Practice</Text>
          <View style={styles.backButton} />
        </View>
        <ScrollView style={styles.scrollView} contentContainerStyle={styles.scrollContent}>
          <View style={styles.startCard}>
            <View style={styles.scenarioHeader}>
              <View style={[styles.badge, styles[`badge${scenario.difficulty}` as keyof typeof styles] || styles.badgehard]}>
                <Text style={styles.badgeText}>{scenario.difficulty}</Text>
              </View>
              <Text style={styles.categoryBadge}>{scenario.category_name}</Text>
            </View>
            
            <Text style={styles.scenarioTitle}>{scenario.title}</Text>
            
            <View style={styles.infoBox}>
              <Ionicons name="information-circle" size={24} color="#60a5fa" />
              <View style={styles.infoContent}>
                <Text style={styles.infoTitle}>Instructions</Text>
                <Text style={styles.infoText}>
                  • You will have {Math.floor(totalTime / 60)} minutes to respond{'\n'}
                  • Read the scenario carefully{'\n'}
                  • Provide a detailed, professional response{'\n'}
                  • Your response will be graded by AI
                  {scenario.is_complex && '\n• This is a complex multi-part scenario'}
                </Text>
              </View>
            </View>

            <View style={styles.timerPreview}>
              <Ionicons name="time" size={32} color="#f59e0b" />
              <Text style={styles.timerPreviewText}>{formatTime(totalTime)}</Text>
            </View>

            <TouchableOpacity style={styles.startButton} onPress={handleStart}>
              <Ionicons name="play" size={24} color="#fff" />
              <Text style={styles.startButtonText}>Start Scenario</Text>
            </TouchableOpacity>
          </View>
        </ScrollView>
      </SafeAreaView>
    );
  }

  // Practice screen
  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView 
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.keyboardView}
      >
        <View style={styles.header}>
          <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
            <Ionicons name="close" size={24} color="#fff" />
          </TouchableOpacity>
          <View style={[styles.timerBadge, { backgroundColor: getTimerColor() }]}>
            <Ionicons name="time" size={18} color="#fff" />
            <Text style={styles.timerText}>{formatTime(timeRemaining)}</Text>
          </View>
          <View style={styles.backButton} />
        </View>

        <ScrollView style={styles.scrollView} contentContainerStyle={styles.practiceContent}>
          <View style={styles.scenarioBox}>
            <Text style={styles.scenarioLabel}>SCENARIO</Text>
            <Text style={styles.scenarioContent}>{scenario.content}</Text>
            {scenario.reference && (
              <Text style={styles.reference}>{scenario.reference}</Text>
            )}
          </View>

          <View style={styles.responseSection}>
            <Text style={styles.responseLabel}>YOUR RESPONSE</Text>
            <TextInput
              style={styles.responseInput}
              multiline
              placeholder="Type your response here. Be thorough and professional in your approach..."
              placeholderTextColor="#64748b"
              value={response}
              onChangeText={setResponse}
              textAlignVertical="top"
            />
            <Text style={styles.charCount}>{response.length} characters</Text>
          </View>
        </ScrollView>

        <View style={styles.submitContainer}>
          <TouchableOpacity 
            style={[styles.submitButton, submitting && styles.submitButtonDisabled]}
            onPress={() => handleSubmit(false)}
            disabled={submitting}
          >
            {submitting ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <>
                <Ionicons name="send" size={20} color="#fff" />
                <Text style={styles.submitButtonText}>Submit Response</Text>
              </>
            )}
          </TouchableOpacity>
        </View>
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
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    gap: 12,
  },
  emptyText: {
    fontSize: 18,
    color: '#94a3b8',
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
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
  },
  timerBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
  },
  timerText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    padding: 16,
  },
  practiceContent: {
    padding: 16,
    paddingBottom: 100,
  },
  startCard: {
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 20,
    gap: 16,
  },
  scenarioHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  badge: {
    paddingHorizontal: 10,
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
    fontSize: 22,
    fontWeight: 'bold',
    color: '#fff',
  },
  infoBox: {
    flexDirection: 'row',
    backgroundColor: '#1e3a5f',
    borderRadius: 12,
    padding: 16,
    gap: 12,
  },
  infoContent: {
    flex: 1,
  },
  infoTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#60a5fa',
    marginBottom: 8,
  },
  infoText: {
    fontSize: 14,
    color: '#94a3b8',
    lineHeight: 22,
  },
  timerPreview: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 12,
    paddingVertical: 16,
  },
  timerPreviewText: {
    fontSize: 48,
    fontWeight: 'bold',
    color: '#f59e0b',
  },
  startButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    backgroundColor: '#2563eb',
    padding: 16,
    borderRadius: 12,
  },
  startButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
  scenarioBox: {
    backgroundColor: '#1e293b',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
  },
  scenarioLabel: {
    fontSize: 12,
    fontWeight: '600',
    color: '#60a5fa',
    marginBottom: 12,
    letterSpacing: 1,
  },
  scenarioContent: {
    fontSize: 15,
    color: '#e2e8f0',
    lineHeight: 24,
  },
  reference: {
    fontSize: 12,
    color: '#94a3b8',
    fontStyle: 'italic',
    marginTop: 12,
  },
  responseSection: {
    flex: 1,
  },
  responseLabel: {
    fontSize: 12,
    fontWeight: '600',
    color: '#10b981',
    marginBottom: 12,
    letterSpacing: 1,
  },
  responseInput: {
    backgroundColor: '#1e293b',
    borderRadius: 12,
    padding: 16,
    fontSize: 15,
    color: '#fff',
    minHeight: 200,
    borderWidth: 1,
    borderColor: '#334155',
  },
  charCount: {
    fontSize: 12,
    color: '#64748b',
    textAlign: 'right',
    marginTop: 8,
  },
  submitContainer: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    padding: 16,
    backgroundColor: '#0c0c0c',
    borderTopWidth: 1,
    borderTopColor: '#1e293b',
  },
  submitButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    backgroundColor: '#10b981',
    padding: 16,
    borderRadius: 12,
  },
  submitButtonDisabled: {
    opacity: 0.7,
  },
  submitButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  resultCard: {
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 20,
    gap: 16,
  },
  scoreContainer: {
    alignItems: 'center',
    paddingVertical: 16,
  },
  scoreLabel: {
    fontSize: 14,
    color: '#94a3b8',
    marginBottom: 8,
  },
  scoreValue: {
    fontSize: 64,
    fontWeight: 'bold',
  },
  divider: {
    height: 1,
    backgroundColor: '#334155',
  },
  feedbackLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#60a5fa',
    marginBottom: 8,
  },
  feedbackText: {
    fontSize: 15,
    color: '#e2e8f0',
    lineHeight: 24,
  },
  modelAnswer: {
    fontSize: 14,
    color: '#94a3b8',
    lineHeight: 22,
  },
  doneButton: {
    backgroundColor: '#2563eb',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    marginTop: 16,
  },
  doneButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});
