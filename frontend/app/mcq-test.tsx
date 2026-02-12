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
import { useRouter, useLocalSearchParams } from 'expo-router';
import { useAuth } from '../contexts/AuthContext';
import { questionService } from '../services/api';

export default function MultipleChoiceTest() {
  const router = useRouter();
  const { sessionToken } = useAuth();
  const params = useLocalSearchParams();
  const questionCount = parseInt(params.count as string) || 25;
  
  const [questions, setQuestions] = useState<any[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<{[key: number]: {selected: string, correct: boolean}}>({});
  const [showFeedback, setShowFeedback] = useState(false);
  const [loading, setLoading] = useState(true);
  const [testCompleted, setTestCompleted] = useState(false);

  useEffect(() => {
    loadQuestions();
  }, []);

  const loadQuestions = async () => {
    try {
      const data = await questionService.getQuestions('practice_exam', undefined, sessionToken || undefined);
      // Randomly select the specified number of questions
      const shuffled = data.sort(() => 0.5 - Math.random());
      setQuestions(shuffled.slice(0, questionCount));
    } catch (error) {
      console.error('Failed to load test:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAnswer = (answer: string) => {
    const currentQ = questions[currentIndex];
    const isCorrect = answer === currentQ.answer;
    
    setAnswers({
      ...answers,
      [currentIndex]: { selected: answer, correct: isCorrect }
    });
    setShowFeedback(true);
  };

  const handleNext = () => {
    setShowFeedback(false);
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(currentIndex + 1);
    } else {
      setTestCompleted(true);
    }
  };

  const calculateScore = () => {
    const correct = Object.values(answers).filter(a => a.correct).length;
    return Math.round((correct / questions.length) * 100);
  };

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <ActivityIndicator size="large" color="#2563eb" />
      </SafeAreaView>
    );
  }

  if (testCompleted) {
    const score = calculateScore();
    const passed = score >= 70;
    
    return (
      <SafeAreaView style={styles.container}>
        <ScrollView style={styles.scrollView}>
          <View style={styles.resultsContainer}>
            <View style={[styles.scoreCard, passed ? styles.passCard : styles.failCard]}>
              <Ionicons 
                name={passed ? "checkmark-circle" : "close-circle"} 
                size={80} 
                color={passed ? "#10b981" : "#ef4444"} 
              />
              <Text style={styles.scoreTitle}>{passed ? "Great Job!" : "Keep Practicing"}</Text>
              <Text style={styles.scoreValue}>{score}%</Text>
              <Text style={styles.scoreSubtitle}>
                {Object.values(answers).filter(a => a.correct).length} / {questions.length} correct
              </Text>
            </View>

            <TouchableOpacity style={styles.retryButton} onPress={() => router.back()}>
              <Text style={styles.retryButtonText}>Back to Tests</Text>
            </TouchableOpacity>
          </View>
        </ScrollView>
      </SafeAreaView>
    );
  }

  const currentQ = questions[currentIndex];
  const hasAnswered = answers[currentIndex] !== undefined;
  const userAnswer = answers[currentIndex];

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()}>
          <Ionicons name="arrow-back" size={24} color="#fff" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>{questionCount}-Question Test</Text>
        <Text style={styles.progressText}>{currentIndex + 1}/{questions.length}</Text>
      </View>

      <ScrollView style={styles.questionContainer}>
        <View style={styles.questionCard}>
          <Text style={styles.questionNumber}>Question {currentIndex + 1}</Text>
          <Text style={styles.questionText}>{currentQ?.content}</Text>

          <View style={styles.optionsContainer}>
            {currentQ?.options?.map((option: string, idx: number) => {
              const isSelected = hasAnswered && userAnswer.selected === option;
              const isCorrect = option === currentQ.answer;
              const showCorrect = showFeedback && isCorrect;
              const showWrong = showFeedback && isSelected && !isCorrect;

              return (
                <TouchableOpacity
                  key={idx}
                  style={[
                    styles.optionButton,
                    isSelected && styles.optionSelected,
                    showCorrect && styles.optionCorrect,
                    showWrong && styles.optionWrong,
                  ]}
                  onPress={() => !hasAnswered && handleAnswer(option)}
                  disabled={hasAnswered}
                >
                  <View style={styles.optionContent}>
                    <Text style={[
                      styles.optionText,
                      (showCorrect || showWrong) && styles.optionTextBold
                    ]}>
                      {option}
                    </Text>
                    {showCorrect && <Ionicons name="checkmark-circle" size={24} color="#10b981" />}
                    {showWrong && <Ionicons name="close-circle" size={24} color="#ef4444" />}
                  </View>
                </TouchableOpacity>
              );
            })}
          </View>

          {showFeedback && (
            <View style={[styles.feedbackCard, userAnswer.correct ? styles.correctFeedback : styles.wrongFeedback]}>
              <View style={styles.feedbackHeader}>
                <Ionicons 
                  name={userAnswer.correct ? "checkmark-circle" : "close-circle"} 
                  size={24} 
                  color={userAnswer.correct ? "#10b981" : "#ef4444"} 
                />
                <Text style={styles.feedbackTitle}>
                  {userAnswer.correct ? "Correct!" : "Incorrect"}
                </Text>
              </View>
              {!userAnswer.correct && (
                <Text style={styles.correctAnswerText}>
                  Correct answer: {currentQ.answer}
                </Text>
              )}
              {currentQ.explanation && (
                <Text style={styles.explanationText}>{currentQ.explanation}</Text>
              )}
            </View>
          )}
        </View>
      </ScrollView>

      {showFeedback && (
        <View style={styles.navigationContainer}>
          <TouchableOpacity style={styles.nextButton} onPress={handleNext}>
            <Text style={styles.nextButtonText}>
              {currentIndex === questions.length - 1 ? 'Finish' : 'Next Question'}
            </Text>
            <Ionicons name="chevron-forward" size={24} color="#fff" />
          </TouchableOpacity>
        </View>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0c0c0c' },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', padding: 16, backgroundColor: '#1e293b' },
  headerTitle: { fontSize: 18, fontWeight: 'bold', color: '#fff' },
  progressText: { fontSize: 16, color: '#94a3b8' },
  questionContainer: { flex: 1 },
  questionCard: { padding: 20 },
  questionNumber: { fontSize: 14, color: '#64748b', marginBottom: 12 },
  questionText: { fontSize: 18, color: '#fff', lineHeight: 28, marginBottom: 24 },
  optionsContainer: { gap: 12, marginBottom: 20 },
  optionButton: { backgroundColor: '#1e293b', padding: 16, borderRadius: 12, borderWidth: 2, borderColor: 'transparent' },
  optionSelected: { borderColor: '#2563eb' },
  optionCorrect: { backgroundColor: '#064e3b', borderColor: '#10b981' },
  optionWrong: { backgroundColor: '#7f1d1d', borderColor: '#ef4444' },
  optionContent: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  optionText: { flex: 1, fontSize: 16, color: '#cbd5e1' },
  optionTextBold: { fontWeight: '600', color: '#fff' },
  feedbackCard: { padding: 16, borderRadius: 12, borderLeftWidth: 4 },
  correctFeedback: { backgroundColor: '#064e3b', borderLeftColor: '#10b981' },
  wrongFeedback: { backgroundColor: '#7f1d1d', borderLeftColor: '#ef4444' },
  feedbackHeader: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 8 },
  feedbackTitle: { fontSize: 16, fontWeight: 'bold', color: '#fff' },
  correctAnswerText: { fontSize: 15, color: '#86efac', marginBottom: 8 },
  explanationText: { fontSize: 14, color: '#cbd5e1', lineHeight: 20 },
  navigationContainer: { padding: 16, backgroundColor: '#1e293b' },
  nextButton: { backgroundColor: '#2563eb', flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8, paddingVertical: 14, borderRadius: 12 },
  nextButtonText: { color: '#fff', fontSize: 16, fontWeight: '600' },
  scrollView: { flex: 1 },
  resultsContainer: { padding: 24 },
  scoreCard: { backgroundColor: '#1e293b', borderRadius: 24, padding: 32, alignItems: 'center', marginBottom: 24, borderWidth: 3 },
  passCard: { borderColor: '#10b981' },
  failCard: { borderColor: '#ef4444' },
  scoreTitle: { fontSize: 24, fontWeight: 'bold', color: '#fff', marginTop: 16, marginBottom: 8 },
  scoreValue: { fontSize: 64, fontWeight: 'bold', color: '#2563eb', marginBottom: 8 },
  scoreSubtitle: { fontSize: 16, color: '#94a3b8' },
  retryButton: { backgroundColor: '#2563eb', paddingVertical: 16, borderRadius: 12, alignItems: 'center' },
  retryButtonText: { color: '#fff', fontSize: 16, fontWeight: '600' },
});
// MCQ
