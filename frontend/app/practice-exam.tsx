import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import { useAuth } from '../contexts/AuthContext';
import { questionService } from '../services/api';

const EXAM_DURATION = 90 * 60; // 90 minutes in seconds

export default function PracticeExam() {
  const router = useRouter();
  const { sessionToken } = useAuth();
  const [questions, setQuestions] = useState<any[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<{[key: number]: string}>({});
  const [timeRemaining, setTimeRemaining] = useState(EXAM_DURATION);
  const [examStarted, setExamStarted] = useState(false);
  const [examCompleted, setExamCompleted] = useState(false);
  const [loading, setLoading] = useState(true);
  const [score, setScore] = useState<number | null>(null);

  useEffect(() => {
    loadQuestions();
  }, []);

  useEffect(() => {
    if (examStarted && !examCompleted && timeRemaining > 0) {
      const timer = setInterval(() => {
        setTimeRemaining(prev => {
          if (prev <= 1) {
            handleSubmit();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
      return () => clearInterval(timer);
    }
  }, [examStarted, examCompleted, timeRemaining]);

  const loadQuestions = async () => {
    try {
      const data = await questionService.getQuestions('practice_exam', undefined, sessionToken || undefined);
      setQuestions(data);
    } catch (error) {
      console.error('Failed to load practice exam:', error);
      Alert.alert('Error', 'Failed to load practice exam questions');
    } finally {
      setLoading(false);
    }
  };

  const handleStart = () => {
    // Skip confirmation and start immediately for web compatibility
    setExamStarted(true);
  };

  const handleAnswer = (answer: string) => {
    setAnswers({ ...answers, [currentIndex]: answer });
  };

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(currentIndex + 1);
    }
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  const handleSubmit = () => {
    setExamCompleted(true);
    calculateScore();
  };

  const calculateScore = () => {
    let correct = 0;
    questions.forEach((q, idx) => {
      if (answers[idx] === q.answer) {
        correct++;
      }
    });
    setScore(Math.round((correct / questions.length) * 100));
  };

  const formatTime = (seconds: number) => {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hrs}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <ActivityIndicator size="large" color="#2563eb" />
      </SafeAreaView>
    );
  }

  // Pre-exam instructions
  if (!examStarted) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.header}>
          <TouchableOpacity onPress={() => router.back()}>
            <Ionicons name="arrow-back" size={24} color="#fff" />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Full Practice Exam</Text>
          <View style={{ width: 24 }} />
        </View>

        <ScrollView style={styles.instructionsContainer}>
          <View style={styles.instructionsCard}>
            <Ionicons name="document-text" size={64} color="#2563eb" />
            <Text style={styles.instructionsTitle}>CPD Detective Practice Exam</Text>
            
            <View style={styles.examStats}>
              <View style={styles.statItem}>
                <Text style={styles.statNumber}>{questions.length}</Text>
                <Text style={styles.statLabel}>Questions</Text>
              </View>
              <View style={styles.statItem}>
                <Text style={styles.statNumber}>90</Text>
                <Text style={styles.statLabel}>Minutes</Text>
              </View>
            </View>

            <View style={styles.instructionsList}>
              <Text style={styles.instructionsHeader}>Instructions:</Text>
              
              <View style={styles.instructionItem}>
                <Ionicons name="checkmark-circle" size={20} color="#10b981" />
                <Text style={styles.instructionText}>
                  This exam simulates the actual CPD Detective promotional test
                </Text>
              </View>

              <View style={styles.instructionItem}>
                <Ionicons name="time" size={20} color="#f59e0b" />
                <Text style={styles.instructionText}>
                  You have 90 minutes (1.5 hours) to complete all {questions.length} questions
                </Text>
              </View>

              <View style={styles.instructionItem}>
                <Ionicons name="alert-circle" size={20} color="#ef4444" />
                <Text style={styles.instructionText}>
                  Once started, the timer CANNOT be paused
                </Text>
              </View>

              <View style={styles.instructionItem}>
                <Ionicons name="book" size={20} color="#3b82f6" />
                <Text style={styles.instructionText}>
                  Questions cover CPD General Orders, Special Orders, and procedures
                </Text>
              </View>

              <View style={styles.instructionItem}>
                <Ionicons name="ribbon" size={20} color="#8b5cf6" />
                <Text style={styles.instructionText}>
                  Your score will be calculated at the end
                </Text>
              </View>
            </View>

            <TouchableOpacity style={styles.startButton} onPress={handleStart}>
              <Ionicons name="play-circle" size={24} color="#fff" />
              <Text style={styles.startButtonText}>Start Practice Exam</Text>
            </TouchableOpacity>

            <Text style={styles.disclaimer}>
              Take this exam seriously to best prepare for the actual test. Good luck!
            </Text>
          </View>
        </ScrollView>
      </SafeAreaView>
    );
  }

  // Exam completed - show results
  if (examCompleted) {
    const answeredCount = Object.keys(answers).length;
    const passingScore = 70;
    const passed = score! >= passingScore;

    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.resultsContainer}>
          <View style={[styles.scoreCard, passed ? styles.passCard : styles.failCard]}>
            <Ionicons 
              name={passed ? "checkmark-circle" : "close-circle"} 
              size={80} 
              color={passed ? "#10b981" : "#ef4444"} 
            />
            <Text style={styles.scoreTitle}>
              {passed ? "Congratulations!" : "Keep Studying"}
            </Text>
            <Text style={styles.scoreValue}>{score}%</Text>
            <Text style={styles.scoreSubtitle}>
              {answeredCount} of {questions.length} questions answered
            </Text>
          </View>

          <View style={styles.statsContainer}>
            <View style={styles.statRow}>
              <Text style={styles.statLabel}>Correct Answers:</Text>
              <Text style={styles.statValue}>
                {Math.round((score! / 100) * questions.length)} / {questions.length}
              </Text>
            </View>
            <View style={styles.statRow}>
              <Text style={styles.statLabel}>Passing Score:</Text>
              <Text style={styles.statValue}>70%</Text>
            </View>
            <View style={styles.statRow}>
              <Text style={styles.statLabel}>Time Used:</Text>
              <Text style={styles.statValue}>{formatTime(EXAM_DURATION - timeRemaining)}</Text>
            </View>
          </View>

          <TouchableOpacity 
            style={styles.reviewButton}
            onPress={() => {
              setExamStarted(false);
              setExamCompleted(false);
              setAnswers({});
              setCurrentIndex(0);
              setTimeRemaining(EXAM_DURATION);
              setScore(null);
            }}
          >
            <Ionicons name="refresh" size={24} color="#fff" />
            <Text style={styles.reviewButtonText}>Retake Exam</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.homeButton} onPress={() => router.back()}>
            <Text style={styles.homeButtonText}>Back to Home</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  // Active exam
  const currentQuestion = questions[currentIndex];
  const timeColor = timeRemaining < 600 ? '#ef4444' : timeRemaining < 1800 ? '#f59e0b' : '#10b981';

  return (
    <SafeAreaView style={styles.container}>
      {/* Timer Header */}
      <View style={styles.timerHeader}>
        <View style={styles.timerContainer}>
          <Ionicons name="time" size={20} color={timeColor} />
          <Text style={[styles.timerText, { color: timeColor }]}>
            {formatTime(timeRemaining)}
          </Text>
        </View>
        <Text style={styles.progressText}>
          {currentIndex + 1} / {questions.length}
        </Text>
      </View>

      {/* Question */}
      <ScrollView style={styles.questionContainer}>
        <View style={styles.questionCard}>
          <Text style={styles.questionNumber}>Question {currentIndex + 1}</Text>
          <Text style={styles.questionText}>{currentQuestion?.content}</Text>

          <View style={styles.optionsContainer}>
            {currentQuestion?.options?.map((option: string, idx: number) => (
              <TouchableOpacity
                key={idx}
                style={[
                  styles.optionButton,
                  answers[currentIndex] === option && styles.optionSelected,
                ]}
                onPress={() => handleAnswer(option)}
              >
                <View style={[
                  styles.optionCircle,
                  answers[currentIndex] === option && styles.optionCircleSelected
                ]}>
                  {answers[currentIndex] === option && (
                    <Ionicons name="checkmark" size={16} color="#fff" />
                  )}
                </View>
                <Text style={[
                  styles.optionText,
                  answers[currentIndex] === option && styles.optionTextSelected
                ]}>
                  {option}
                </Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>
      </ScrollView>

      {/* Navigation */}
      <View style={styles.navigationContainer}>
        <TouchableOpacity
          style={[styles.navButton, currentIndex === 0 && styles.navButtonDisabled]}
          onPress={handlePrevious}
          disabled={currentIndex === 0}
        >
          <Ionicons name="chevron-back" size={24} color={currentIndex === 0 ? "#64748b" : "#fff"} />
          <Text style={[styles.navButtonText, currentIndex === 0 && styles.navButtonTextDisabled]}>
            Previous
          </Text>
        </TouchableOpacity>

        {currentIndex === questions.length - 1 ? (
          <TouchableOpacity style={styles.submitButton} onPress={handleSubmit}>
            <Ionicons name="checkmark-done" size={24} color="#fff" />
            <Text style={styles.submitButtonText}>Submit Exam</Text>
          </TouchableOpacity>
        ) : (
          <TouchableOpacity style={styles.navButton} onPress={handleNext}>
            <Text style={styles.navButtonText}>Next</Text>
            <Ionicons name="chevron-forward" size={24} color="#fff" />
          </TouchableOpacity>
        )}
      </View>
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
  headerTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
  },
  instructionsContainer: {
    flex: 1,
    padding: 20,
  },
  instructionsCard: {
    backgroundColor: '#1e293b',
    borderRadius: 24,
    padding: 32,
    alignItems: 'center',
  },
  instructionsTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    marginTop: 20,
    marginBottom: 24,
    textAlign: 'center',
  },
  examStats: {
    flexDirection: 'row',
    gap: 48,
    marginBottom: 32,
  },
  statItem: {
    alignItems: 'center',
  },
  statNumber: {
    fontSize: 48,
    fontWeight: 'bold',
    color: '#2563eb',
  },
  statLabel: {
    fontSize: 14,
    color: '#94a3b8',
    marginTop: 8,
  },
  instructionsList: {
    width: '100%',
    gap: 16,
    marginBottom: 32,
  },
  instructionsHeader: {
    fontSize: 18,
    fontWeight: '600',
    color: '#fff',
    marginBottom: 8,
  },
  instructionItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  instructionText: {
    flex: 1,
    fontSize: 15,
    color: '#cbd5e1',
    lineHeight: 22,
  },
  startButton: {
    backgroundColor: '#10b981',
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    paddingVertical: 16,
    paddingHorizontal: 32,
    borderRadius: 16,
    width: '100%',
    justifyContent: 'center',
    marginBottom: 16,
  },
  startButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
  disclaimer: {
    fontSize: 13,
    color: '#64748b',
    textAlign: 'center',
    fontStyle: 'italic',
  },
  timerHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    backgroundColor: '#1e293b',
    borderBottomWidth: 1,
    borderBottomColor: '#334155',
  },
  timerContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  timerText: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  progressText: {
    fontSize: 16,
    color: '#94a3b8',
    fontWeight: '600',
  },
  questionContainer: {
    flex: 1,
  },
  questionCard: {
    padding: 20,
  },
  questionNumber: {
    fontSize: 14,
    color: '#64748b',
    marginBottom: 12,
  },
  questionText: {
    fontSize: 18,
    color: '#fff',
    lineHeight: 28,
    marginBottom: 24,
  },
  optionsContainer: {
    gap: 12,
  },
  optionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1e293b',
    padding: 16,
    borderRadius: 12,
    gap: 12,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  optionSelected: {
    backgroundColor: '#1e3a8a',
    borderColor: '#2563eb',
  },
  optionCircle: {
    width: 24,
    height: 24,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#64748b',
    alignItems: 'center',
    justifyContent: 'center',
  },
  optionCircleSelected: {
    backgroundColor: '#2563eb',
    borderColor: '#2563eb',
  },
  optionText: {
    flex: 1,
    fontSize: 16,
    color: '#cbd5e1',
  },
  optionTextSelected: {
    color: '#fff',
    fontWeight: '500',
  },
  navigationContainer: {
    flexDirection: 'row',
    padding: 16,
    gap: 12,
    backgroundColor: '#1e293b',
    borderTopWidth: 1,
    borderTopColor: '#334155',
  },
  navButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    backgroundColor: '#334155',
    paddingVertical: 14,
    borderRadius: 12,
  },
  navButtonDisabled: {
    opacity: 0.4,
  },
  navButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  navButtonTextDisabled: {
    color: '#64748b',
  },
  submitButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    backgroundColor: '#10b981',
    paddingVertical: 14,
    borderRadius: 12,
  },
  submitButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  resultsContainer: {
    flex: 1,
    padding: 24,
    justifyContent: 'center',
  },
  scoreCard: {
    backgroundColor: '#1e293b',
    borderRadius: 24,
    padding: 32,
    alignItems: 'center',
    marginBottom: 24,
    borderWidth: 3,
  },
  passCard: {
    borderColor: '#10b981',
  },
  failCard: {
    borderColor: '#ef4444',
  },
  scoreTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    marginTop: 16,
    marginBottom: 8,
  },
  scoreValue: {
    fontSize: 72,
    fontWeight: 'bold',
    color: '#2563eb',
    marginBottom: 8,
  },
  scoreSubtitle: {
    fontSize: 16,
    color: '#94a3b8',
  },
  statsContainer: {
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 20,
    marginBottom: 24,
  },
  statRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#334155',
  },
  statValue: {
    fontSize: 16,
    fontWeight: '600',
    color: '#fff',
  },
  reviewButton: {
    backgroundColor: '#2563eb',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 12,
    paddingVertical: 16,
    borderRadius: 12,
    marginBottom: 12,
  },
  reviewButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  homeButton: {
    paddingVertical: 14,
    alignItems: 'center',
  },
  homeButtonText: {
    color: '#64748b',
    fontSize: 16,
  },
});
// Practice exam
