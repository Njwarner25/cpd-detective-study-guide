import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useAuth } from '../contexts/AuthContext';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { questionService } from '../services/api';

export default function Quiz() {
  const { sessionToken } = useAuth();
  const router = useRouter();
  const params = useLocalSearchParams();
  const questionCount = parseInt(params.count as string) || 25;
  
  const [questions, setQuestions] = useState<any[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState<string[]>([]);
  const [showResult, setShowResult] = useState(false);
  const [score, setScore] = useState(0);
  const [answers, setAnswers] = useState<{questionId: string, selected: string[], correct: boolean}[]>([]);
  const [loading, setLoading] = useState(true);
  const [quizComplete, setQuizComplete] = useState(false);

  useEffect(() => {
    loadQuestions();
  }, []);

  const loadQuestions = async () => {
    try {
      const data = await questionService.getQuestions('multiple_choice', undefined, sessionToken || undefined);
      // Shuffle and take required number
      const shuffled = data.sort(() => Math.random() - 0.5);
      setQuestions(shuffled.slice(0, questionCount));
    } catch (error) {
      console.error('Failed to load questions:', error);
      Alert.alert('Error', 'Failed to load quiz questions');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectAnswer = (answer: string) => {
    if (showResult) return;
    
    const currentQuestion = questions[currentIndex];
    const hasMultipleCorrect = currentQuestion.correct_answers.length > 1;
    
    if (hasMultipleCorrect) {
      // Toggle selection for multi-answer questions
      setSelectedAnswers(prev => {
        if (prev.includes(answer)) {
          return prev.filter(a => a !== answer);
        } else {
          return [...prev, answer];
        }
      });
    } else {
      // Single selection for single-answer questions
      setSelectedAnswers([answer]);
    }
  };

  const handleSubmitAnswer = () => {
    if (selectedAnswers.length === 0) {
      Alert.alert('Select an Answer', 'Please select an answer before continuing.');
      return;
    }

    const currentQuestion = questions[currentIndex];
    const correctAnswers = currentQuestion.correct_answers;
    
    // Check if all selected answers are correct and all correct answers are selected
    const isCorrect = 
      selectedAnswers.length === correctAnswers.length &&
      selectedAnswers.every(ans => correctAnswers.includes(ans));
    
    if (isCorrect) {
      setScore(prev => prev + 1);
    }

    setAnswers(prev => [...prev, {
      questionId: currentQuestion.question_id,
      selected: selectedAnswers,
      correct: isCorrect
    }]);

    setShowResult(true);
  };

  const handleNextQuestion = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(prev => prev + 1);
      setSelectedAnswers([]);
      setShowResult(false);
    } else {
      setQuizComplete(true);
    }
  };

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#2563eb" />
          <Text style={styles.loadingText}>Loading Quiz...</Text>
        </View>
      </SafeAreaView>
    );
  }

  if (questions.length === 0) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.header}>
          <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
            <Ionicons name="arrow-back" size={24} color="#fff" />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Quiz</Text>
          <View style={styles.backButton} />
        </View>
        <View style={styles.emptyContainer}>
          <Ionicons name="help-circle-outline" size={64} color="#64748b" />
          <Text style={styles.emptyText}>No questions available</Text>
        </View>
      </SafeAreaView>
    );
  }

  // Quiz Complete Screen
  if (quizComplete) {
    const percentage = Math.round((score / questions.length) * 100);
    const passed = percentage >= 70;

    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.header}>
          <View style={styles.backButton} />
          <Text style={styles.headerTitle}>Quiz Complete</Text>
          <View style={styles.backButton} />
        </View>
        <ScrollView contentContainerStyle={styles.resultContainer}>
          <View style={[styles.scoreCircle, { borderColor: passed ? '#10b981' : '#ef4444' }]}>
            <Text style={[styles.scorePercentage, { color: passed ? '#10b981' : '#ef4444' }]}>
              {percentage}%
            </Text>
            <Text style={styles.scoreLabel}>{score} / {questions.length}</Text>
          </View>

          <Text style={[styles.resultText, { color: passed ? '#10b981' : '#ef4444' }]}>
            {passed ? 'PASSED!' : 'Keep Studying'}
          </Text>
          <Text style={styles.resultSubtext}>
            {passed ? 'Great job! You\'re making progress.' : 'You need 70% to pass. Review the material and try again.'}
          </Text>

          <View style={styles.statsRow}>
            <View style={styles.statBox}>
              <Ionicons name="checkmark-circle" size={24} color="#10b981" />
              <Text style={styles.statNumber}>{score}</Text>
              <Text style={styles.statLabel}>Correct</Text>
            </View>
            <View style={styles.statBox}>
              <Ionicons name="close-circle" size={24} color="#ef4444" />
              <Text style={styles.statNumber}>{questions.length - score}</Text>
              <Text style={styles.statLabel}>Incorrect</Text>
            </View>
          </View>

          <TouchableOpacity style={styles.retryButton} onPress={() => router.back()}>
            <Text style={styles.retryButtonText}>Back to Tests</Text>
          </TouchableOpacity>
        </ScrollView>
      </SafeAreaView>
    );
  }

  const currentQuestion = questions[currentIndex];
  const hasMultipleCorrect = currentQuestion.correct_answers.length > 1;

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
          <Ionicons name="close" size={24} color="#fff" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Question {currentIndex + 1}/{questions.length}</Text>
        <Text style={styles.scoreText}>{score} pts</Text>
      </View>

      <View style={styles.progressBar}>
        <View style={[styles.progressFill, { width: `${((currentIndex + 1) / questions.length) * 100}%` }]} />
      </View>

      <ScrollView style={styles.scrollView} contentContainerStyle={styles.scrollContent}>
        <View style={styles.questionCard}>
          <View style={styles.categoryBadge}>
            <Text style={styles.categoryText}>{currentQuestion.category_name}</Text>
          </View>
          
          <Text style={styles.questionText}>{currentQuestion.question}</Text>
          
          {hasMultipleCorrect && (
            <Text style={styles.multipleNote}>Note: This question may have multiple correct answers</Text>
          )}
        </View>

        <View style={styles.optionsContainer}>
          {currentQuestion.options.map((option: string, index: number) => {
            const isSelected = selectedAnswers.includes(option);
            const isCorrect = currentQuestion.correct_answers.includes(option);
            
            let optionStyle = styles.option;
            let textStyle = styles.optionText;
            
            if (showResult) {
              if (isCorrect) {
                optionStyle = {...styles.option, ...styles.optionCorrect};
                textStyle = {...styles.optionText, color: '#10b981'};
              } else if (isSelected && !isCorrect) {
                optionStyle = {...styles.option, ...styles.optionIncorrect};
                textStyle = {...styles.optionText, color: '#ef4444'};
              }
            } else if (isSelected) {
              optionStyle = {...styles.option, ...styles.optionSelected};
            }

            return (
              <TouchableOpacity
                key={index}
                style={optionStyle}
                onPress={() => handleSelectAnswer(option)}
                disabled={showResult}
              >
                {hasMultipleCorrect ? (
                  <View style={[styles.checkbox, isSelected && styles.checkboxSelected]}>
                    {isSelected && <Ionicons name="checkmark" size={16} color="#fff" />}
                  </View>
                ) : (
                  <View style={[styles.radioButton, isSelected && styles.radioButtonSelected]}>
                    {isSelected && <View style={styles.radioButtonInner} />}
                  </View>
                )}
                <Text style={textStyle}>{option}</Text>
                {showResult && isCorrect && (
                  <Ionicons name="checkmark-circle" size={24} color="#10b981" style={styles.optionIcon} />
                )}
                {showResult && isSelected && !isCorrect && (
                  <Ionicons name="close-circle" size={24} color="#ef4444" style={styles.optionIcon} />
                )}
              </TouchableOpacity>
            );
          })}
        </View>

        {showResult && currentQuestion.explanation && (
          <View style={styles.explanationBox}>
            <Text style={styles.explanationTitle}>Explanation:</Text>
            <Text style={styles.explanationText}>{currentQuestion.explanation}</Text>
            {currentQuestion.reference && (
              <Text style={styles.referenceText}>{currentQuestion.reference}</Text>
            )}
          </View>
        )}
      </ScrollView>

      <View style={styles.footer}>
        {!showResult ? (
          <TouchableOpacity 
            style={[styles.submitButton, selectedAnswers.length === 0 && styles.submitButtonDisabled]}
            onPress={handleSubmitAnswer}
            disabled={selectedAnswers.length === 0}
          >
            <Text style={styles.submitButtonText}>Submit Answer</Text>
          </TouchableOpacity>
        ) : (
          <TouchableOpacity style={styles.nextButton} onPress={handleNextQuestion}>
            <Text style={styles.nextButtonText}>
              {currentIndex < questions.length - 1 ? 'Next Question' : 'See Results'}
            </Text>
            <Ionicons name="arrow-forward" size={20} color="#fff" />
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
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    gap: 12,
  },
  loadingText: {
    color: '#94a3b8',
    fontSize: 16,
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
    width: 50,
  },
  headerTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#fff',
  },
  scoreText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#10b981',
    width: 50,
    textAlign: 'right',
  },
  progressBar: {
    height: 4,
    backgroundColor: '#1e293b',
    marginHorizontal: 16,
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#2563eb',
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    padding: 16,
    paddingBottom: 100,
  },
  questionCard: {
    backgroundColor: '#1e293b',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
  },
  categoryBadge: {
    backgroundColor: '#334155',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 6,
    alignSelf: 'flex-start',
    marginBottom: 12,
  },
  categoryText: {
    color: '#94a3b8',
    fontSize: 12,
  },
  questionText: {
    fontSize: 17,
    color: '#fff',
    lineHeight: 26,
  },
  multipleNote: {
    fontSize: 12,
    color: '#f59e0b',
    fontStyle: 'italic',
    marginTop: 12,
  },
  optionsContainer: {
    gap: 12,
  },
  option: {
    backgroundColor: '#1e293b',
    borderRadius: 12,
    padding: 16,
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: 'transparent',
  },
  optionSelected: {
    borderColor: '#2563eb',
    backgroundColor: '#1e3a5f',
  },
  optionCorrect: {
    borderColor: '#10b981',
    backgroundColor: '#064e3b',
  },
  optionIncorrect: {
    borderColor: '#ef4444',
    backgroundColor: '#7f1d1d',
  },
  optionLetter: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: '#334155',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  optionLetterText: {
    color: '#fff',
    fontWeight: '600',
  },
  checkbox: {
    width: 24,
    height: 24,
    borderRadius: 6,
    borderWidth: 2,
    borderColor: '#64748b',
    marginRight: 12,
    justifyContent: 'center',
    alignItems: 'center',
  },
  checkboxSelected: {
    backgroundColor: '#2563eb',
    borderColor: '#2563eb',
  },
  radioButton: {
    width: 24,
    height: 24,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#64748b',
    marginRight: 12,
    justifyContent: 'center',
    alignItems: 'center',
  },
  radioButtonSelected: {
    borderColor: '#2563eb',
  },
  radioButtonInner: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: '#2563eb',
  },
  optionText: {
    flex: 1,
    color: '#e2e8f0',
    fontSize: 15,
    lineHeight: 22,
  },
  optionIcon: {
    marginLeft: 8,
  },
  explanationBox: {
    backgroundColor: '#1e3a5f',
    borderRadius: 12,
    padding: 16,
    marginTop: 16,
  },
  explanationTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#60a5fa',
    marginBottom: 8,
  },
  explanationText: {
    fontSize: 14,
    color: '#cbd5e1',
    lineHeight: 22,
  },
  referenceText: {
    fontSize: 12,
    color: '#94a3b8',
    fontStyle: 'italic',
    marginTop: 8,
  },
  footer: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    padding: 16,
    paddingBottom: 32,
    backgroundColor: '#0c0c0c',
    borderTopWidth: 1,
    borderTopColor: '#1e293b',
  },
  submitButton: {
    backgroundColor: '#2563eb',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  submitButtonDisabled: {
    opacity: 0.5,
  },
  submitButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  nextButton: {
    backgroundColor: '#10b981',
    padding: 16,
    borderRadius: 12,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
  },
  nextButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  resultContainer: {
    padding: 24,
    alignItems: 'center',
  },
  scoreCircle: {
    width: 180,
    height: 180,
    borderRadius: 90,
    borderWidth: 8,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 24,
  },
  scorePercentage: {
    fontSize: 48,
    fontWeight: 'bold',
  },
  scoreLabel: {
    fontSize: 16,
    color: '#94a3b8',
  },
  resultText: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  resultSubtext: {
    fontSize: 16,
    color: '#94a3b8',
    textAlign: 'center',
    marginBottom: 32,
  },
  statsRow: {
    flexDirection: 'row',
    gap: 24,
    marginBottom: 32,
  },
  statBox: {
    backgroundColor: '#1e293b',
    borderRadius: 12,
    padding: 20,
    alignItems: 'center',
    minWidth: 100,
  },
  statNumber: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#fff',
    marginTop: 8,
  },
  statLabel: {
    fontSize: 14,
    color: '#94a3b8',
  },
  retryButton: {
    backgroundColor: '#2563eb',
    padding: 16,
    paddingHorizontal: 32,
    borderRadius: 12,
  },
  retryButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});