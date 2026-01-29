import React, { useEffect, useState, useRef } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Dimensions, Animated, ActivityIndicator, ScrollView } from 'react-native';
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
  
  // Use useRef to persist animation value
  const flipAnimation = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    loadQuestions();
  }, []);

  useEffect(() => {
    if (questions.length > 0) {
      checkBookmark();
      // Reset flip state when changing cards
      setFlipped(false);
      flipAnimation.setValue(0);
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
    const toValue = flipped ? 0 : 1;
    Animated.spring(flipAnimation, {
      toValue,
      friction: 8,
      tension: 10,
      useNativeDriver: true,
    }).start();
    setFlipped(!flipped);
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
          <View style={styles.backButton} />
        </View>
        <View style={styles.emptyContainer}>
          <Ionicons name="layers-outline" size={64} color="#64748b" />
          <Text style={styles.emptyText}>No flashcards available</Text>
        </View>
      </SafeAreaView>
    );
  }

  const currentQuestion = questions[currentIndex];
  
  // Interpolate for front card (question)
  const frontOpacity = flipAnimation.interpolate({
    inputRange: [0, 0.5, 1],
    outputRange: [1, 0, 0],
  });
  
  const frontScale = flipAnimation.interpolate({
    inputRange: [0, 0.5, 1],
    outputRange: [1, 0.95, 0.9],
  });

  // Interpolate for back card (answer)
  const backOpacity = flipAnimation.interpolate({
    inputRange: [0, 0.5, 1],
    outputRange: [0, 0, 1],
  });
  
  const backScale = flipAnimation.interpolate({
    inputRange: [0, 0.5, 1],
    outputRange: [0.9, 0.95, 1],
  });

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
          <Ionicons name="arrow-back" size={24} color="#fff" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Flashcards</Text>
        <View style={styles.headerActions}>
          <TouchableOpacity onPress={() => router.push('/support')} style={styles.donateButton}>
            <Ionicons name="heart" size={22} color="#ff6b6b" />
          </TouchableOpacity>
          <TouchableOpacity onPress={toggleBookmark} style={styles.bookmarkButton}>
            <Ionicons 
              name={bookmarked ? "bookmark" : "bookmark-outline"} 
              size={24} 
              color={bookmarked ? "#f59e0b" : "#fff"} 
            />
          </TouchableOpacity>
        </View>
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
        <TouchableOpacity activeOpacity={0.9} onPress={handleFlip} style={styles.cardTouchable}>
          {/* Front Card - Question */}
          <Animated.View 
            style={[
              styles.card, 
              { 
                opacity: frontOpacity,
                transform: [{ scale: frontScale }],
                zIndex: flipped ? 0 : 1,
              }
            ]}
            pointerEvents={flipped ? 'none' : 'auto'}
          >
            <ScrollView style={styles.cardScroll} showsVerticalScrollIndicator={false}>
              <View style={styles.cardContent}>
                <View style={styles.cardHeader}>
                  <View style={[styles.badge, styles[`badge${currentQuestion.difficulty}` as keyof typeof styles] || styles.badgemedium]}>
                    <Text style={styles.badgeText}>{currentQuestion.difficulty}</Text>
                  </View>
                  <Text style={styles.categoryBadge}>{currentQuestion.category_name}</Text>
                </View>
                <Text style={styles.questionTitle}>{currentQuestion.title}</Text>
                <Text style={styles.questionContent}>{currentQuestion.content}</Text>
                {currentQuestion.reference && (
                  <Text style={styles.reference}>{currentQuestion.reference}</Text>
                )}
              </View>
            </ScrollView>
            <View style={styles.flipHint}>
              <Ionicons name="refresh" size={20} color="#64748b" />
              <Text style={styles.flipHintText}>Tap to see answer</Text>
            </View>
          </Animated.View>

          {/* Back Card - Answer */}
          <Animated.View 
            style={[
              styles.card, 
              styles.cardBack,
              { 
                opacity: backOpacity,
                transform: [{ scale: backScale }],
                zIndex: flipped ? 1 : 0,
              }
            ]}
            pointerEvents={flipped ? 'auto' : 'none'}
          >
            <ScrollView style={styles.cardScroll} showsVerticalScrollIndicator={false}>
              <View style={styles.cardContent}>
                <Text style={styles.answerLabel}>Answer:</Text>
                <Text style={styles.answerText}>{currentQuestion.answer}</Text>
                {currentQuestion.explanation && (
                  <>
                    <Text style={styles.explanationLabel}>Explanation:</Text>
                    <Text style={styles.explanationText}>{currentQuestion.explanation}</Text>
                  </>
                )}
              </View>
            </ScrollView>
            <View style={styles.flipHint}>
              <Ionicons name="refresh" size={20} color="#64748b" />
              <Text style={styles.flipHintText}>Tap to see question</Text>
            </View>
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
          <Text style={styles.flipButtonText}>{flipped ? 'Show Question' : 'Show Answer'}</Text>
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
    width: 40,
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
  },
  bookmarkButton: {
    padding: 8,
    width: 40,
    alignItems: 'flex-end',
  },
  headerActions: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  donateButton: {
    padding: 8,
    width: 40,
    alignItems: 'center',
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
    paddingHorizontal: 24,
    paddingVertical: 16,
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
    padding: 20,
  },
  cardBack: {
    backgroundColor: '#1a365d',
  },
  cardScroll: {
    flex: 1,
  },
  cardContent: {
    flex: 1,
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 16,
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
  },
  reference: {
    fontSize: 12,
    color: '#94a3b8',
    fontStyle: 'italic',
    marginTop: 16,
  },
  answerLabel: {
    fontSize: 16,
    fontWeight: '700',
    color: '#10b981',
    marginBottom: 12,
  },
  answerText: {
    fontSize: 15,
    color: '#e2e8f0',
    lineHeight: 24,
    marginBottom: 20,
  },
  explanationLabel: {
    fontSize: 16,
    fontWeight: '700',
    color: '#60a5fa',
    marginBottom: 8,
    marginTop: 8,
  },
  explanationText: {
    fontSize: 14,
    color: '#94a3b8',
    lineHeight: 22,
  },
  flipHint: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    paddingTop: 16,
    borderTopWidth: 1,
    borderTopColor: '#334155',
    marginTop: 12,
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
    width: 56,
    height: 56,
    borderRadius: 28,
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
    paddingHorizontal: 24,
    paddingVertical: 14,
    borderRadius: 12,
  },
  flipButtonText: {
    color: '#fff',
    fontSize: 15,
    fontWeight: '600',
  },
});
