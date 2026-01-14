import React, { useEffect, useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Dimensions, Animated, ActivityIndicator } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useAuth } from '../contexts/AuthContext';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { questionService, bookmarkService } from '../services/api';

const { width: SCREEN_WIDTH } = Dimensions.get('window');

export default function Study() {
  const { sessionToken } = useAuth();
  const router = useRouter();
  const params = useLocalSearchParams();
  const [questions, setQuestions] = useState<any[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [bookmarked, setBookmarked] = useState(false);
  const [loading, setLoading] = useState(true);
  const flipAnim = new Animated.Value(0);
  const translateX = new Animated.Value(0);

  useEffect(() => {
    loadQuestions();
  }, []);

  useEffect(() => {
    if (questions.length > 0) {
      checkBookmark();
      setFlipped(false);
    }
  }, [currentIndex]);

  const loadQuestions = async () => {
    try {
      const categoryId = params.category !== 'all' ? params.category as string : undefined;
      const data = await questionService.getQuestions('flashcard', categoryId, sessionToken || undefined);
      setQuestions(data);
    } catch (error) {
      console.error('Failed to load questions:', error);
    } finally {
      setLoading(false);
    }
  };

  const checkBookmark = async () => {
    if (questions[currentIndex]) {
      try {
        const progress = await bookmarkService.getProgress(questions[currentIndex].question_id, sessionToken || undefined);
        setBookmarked(progress?.bookmarked || false);
      } catch (error) {
        console.error('Failed to check bookmark:', error);
      }
    }
  };

  const handleFlip = () => {
    Animated.timing(flipAnim, {
      toValue: flipped ? 0 : 180,
      duration: 300,
      useNativeDriver: true,
    }).start();
    setFlipped(!flipped);
  };

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      Animated.sequence([
        Animated.timing(translateX, {
          toValue: -SCREEN_WIDTH,
          duration: 200,
          useNativeDriver: true,
        }),
        Animated.timing(translateX, {
          toValue: 0,
          duration: 0,
          useNativeDriver: true,
        }),
      ]).start();
      setCurrentIndex(currentIndex + 1);
    }
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      Animated.sequence([
        Animated.timing(translateX, {
          toValue: SCREEN_WIDTH,
          duration: 200,
          useNativeDriver: true,
        }),
        Animated.timing(translateX, {
          toValue: 0,
          duration: 0,
          useNativeDriver: true,
        }),
      ]).start();
      setCurrentIndex(currentIndex - 1);
    }
  };

  const toggleBookmark = async () => {
    try {
      const result = await bookmarkService.toggleBookmark(questions[currentIndex].question_id, sessionToken || undefined);
      setBookmarked(result.bookmarked);
    } catch (error) {
      console.error('Failed to toggle bookmark:', error);
    }
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

  if (questions.length === 0) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.header}>
          <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
            <Ionicons name="arrow-back" size={24} color="#fff" />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Study</Text>
        </View>
        <View style={styles.emptyContainer}>
          <Ionicons name="layers-outline" size={64} color="#64748b" />
          <Text style={styles.emptyText}>No flashcards available</Text>
        </View>
      </SafeAreaView>
    );
  }

  const currentQuestion = questions[currentIndex];
  const frontInterpolate = flipAnim.interpolate({
    inputRange: [0, 180],
    outputRange: ['0deg', '180deg'],
  });
  const backInterpolate = flipAnim.interpolate({
    inputRange: [0, 180],
    outputRange: ['180deg', '360deg'],
  });

  return (
    <SafeAreaView style={styles.container}>
        <View style={styles.header}>
          <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
            <Ionicons name="arrow-back" size={24} color="#fff" />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Flashcards</Text>
          <TouchableOpacity onPress={toggleBookmark} style={styles.bookmarkButton}>
            <Ionicons 
              name={bookmarked ? "bookmark" : "bookmark-outline"} 
              size={24} 
              color={bookmarked ? "#f59e0b" : "#fff"} 
            />
          </TouchableOpacity>
        </View>

        <View style={styles.progressContainer}>
          <Text style={styles.progressText}>
            {currentIndex + 1} / {questions.length}
          </Text>
          <View style={styles.progressBar}>
            <View style={[styles.progressFill, { width: `${((currentIndex + 1) / questions.length) * 100}%` }]} />
          </View>
        </View>

        <View style={styles.cardContainer}>
          <TouchableOpacity activeOpacity={1} onPress={handleFlip} style={styles.cardTouchable}>
            <Animated.View style={[styles.card, { transform: [{ translateX }, { rotateY: frontInterpolate }] }]}>
              {!flipped && (
                <View style={styles.cardContent}>
                  <View style={styles.cardHeader}>
                    <View style={[styles.badge, styles[`badge${currentQuestion.difficulty}`]]}>
                      <Text style={styles.badgeText}>{currentQuestion.difficulty}</Text>
                    </View>
                    <Text style={styles.categoryBadge}>{currentQuestion.category_name}</Text>
                  </View>
                  <Text style={styles.questionTitle}>{currentQuestion.title}</Text>
                  <Text style={styles.questionContent}>{currentQuestion.content}</Text>
                  {currentQuestion.reference && (
                    <Text style={styles.reference}>{currentQuestion.reference}</Text>
                  )}
                  <View style={styles.flipHint}>
                    <Ionicons name="refresh" size={20} color="#64748b" />
                    <Text style={styles.flipHintText}>Tap to see answer</Text>
                  </View>
                </View>
              )}
            </Animated.View>

            <Animated.View style={[styles.card, styles.cardBack, { transform: [{ translateX }, { rotateY: backInterpolate }] }]}>
              {flipped && (
                <View style={styles.cardContent}>
                  <Text style={styles.answerLabel}>Answer:</Text>
                  <Text style={styles.answerText}>{currentQuestion.answer}</Text>
                  {currentQuestion.explanation && (
                    <>
                      <Text style={styles.explanationLabel}>Explanation:</Text>
                      <Text style={styles.explanationText}>{currentQuestion.explanation}</Text>
                    </>
                  )}
                  <View style={styles.flipHint}>
                    <Ionicons name="refresh" size={20} color="#64748b" />
                    <Text style={styles.flipHintText}>Tap to see question</Text>
                  </View>
                </View>
              )}
            </Animated.View>
          </TouchableOpacity>
        </View>

        <View style={styles.controls}>
          <TouchableOpacity 
            style={[styles.controlButton, currentIndex === 0 && styles.controlButtonDisabled]}
            onPress={handlePrevious}
            disabled={currentIndex === 0}
          >
            <Ionicons name="chevron-back" size={32} color={currentIndex === 0 ? "#334155" : "#fff"} />
          </TouchableOpacity>

          <TouchableOpacity style={styles.flipButton} onPress={handleFlip}>
            <Ionicons name="refresh" size={24} color="#fff" />
            <Text style={styles.flipButtonText}>Flip</Text>
          </TouchableOpacity>

          <TouchableOpacity 
            style={[styles.controlButton, currentIndex === questions.length - 1 && styles.controlButtonDisabled]}
            onPress={handleNext}
            disabled={currentIndex === questions.length - 1}
          >
            <Ionicons name="chevron-forward" size={32} color={currentIndex === questions.length - 1 ? "#334155" : "#fff"} />
          </TouchableOpacity>
        </View>
      </SafeAreaView>
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
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
  },
  bookmarkButton: {
    padding: 8,
  },
  progressContainer: {
    paddingHorizontal: 24,
    paddingBottom: 16,
  },
  progressText: {
    fontSize: 14,
    color: '#94a3b8',
    marginBottom: 8,
    textAlign: 'center',
  },
  progressBar: {
    height: 4,
    backgroundColor: '#1e293b',
    borderRadius: 2,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#2563eb',
  },
  cardContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  cardTouchable: {
    width: '100%',
    height: '100%',
    maxHeight: 500,
  },
  card: {
    position: 'absolute',
    width: '100%',
    height: '100%',
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 24,
    backfaceVisibility: 'hidden',
  },
  cardBack: {
    position: 'absolute',
  },
  cardContent: {
    flex: 1,
    justifyContent: 'space-between',
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 16,
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
  questionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#fff',
    marginBottom: 12,
  },
  questionContent: {
    fontSize: 16,
    color: '#cbd5e1',
    lineHeight: 24,
    flex: 1,
  },
  reference: {
    fontSize: 12,
    color: '#94a3b8',
    fontStyle: 'italic',
    marginTop: 12,
  },
  answerLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#10b981',
    marginBottom: 8,
  },
  answerText: {
    fontSize: 16,
    color: '#cbd5e1',
    lineHeight: 24,
    marginBottom: 16,
  },
  explanationLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#3b82f6',
    marginBottom: 8,
  },
  explanationText: {
    fontSize: 14,
    color: '#94a3b8',
    lineHeight: 20,
    flex: 1,
  },
  flipHint: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    marginTop: 16,
    paddingTop: 16,
    borderTopWidth: 1,
    borderTopColor: '#334155',
  },
  flipHintText: {
    fontSize: 14,
    color: '#64748b',
  },
  controls: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 24,
    paddingBottom: 32,
  },
  controlButton: {
    width: 64,
    height: 64,
    borderRadius: 32,
    backgroundColor: '#1e293b',
    justifyContent: 'center',
    alignItems: 'center',
  },
  controlButtonDisabled: {
    opacity: 0.3,
  },
  flipButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    backgroundColor: '#2563eb',
    paddingHorizontal: 32,
    paddingVertical: 16,
    borderRadius: 12,
  },
  flipButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});