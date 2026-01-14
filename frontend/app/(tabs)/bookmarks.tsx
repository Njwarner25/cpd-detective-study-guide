import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet, ActivityIndicator, RefreshControl } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useAuth } from '../../contexts/AuthContext';
import { useRouter } from 'expo-router';
import { bookmarkService } from '../../services/api';

export default function Bookmarks() {
  const { sessionToken } = useAuth();
  const router = useRouter();
  const [bookmarks, setBookmarks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const loadBookmarks = async () => {
    try {
      const data = await bookmarkService.getBookmarks(sessionToken || undefined);
      setBookmarks(data);
    } catch (error) {
      console.error('Failed to load bookmarks:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    loadBookmarks();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    loadBookmarks();
  };

  const handleQuestionPress = (question: any) => {
    if (question.type === 'flashcard') {
      router.push({
        pathname: '/study',
        params: { questionId: question.question_id }
      });
    } else {
      router.push({
        pathname: '/practice-scenario',
        params: { scenarioId: question.question_id }
      });
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

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView 
        style={styles.scrollView}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor="#2563eb" />
        }
      >
        <View style={styles.header}>
          <Text style={styles.title}>Bookmarks</Text>
          <Text style={styles.subtitle}>{bookmarks.length} saved questions</Text>
        </View>

        <View style={styles.section}>
          {bookmarks.length > 0 ? (
            bookmarks.map((question) => (
              <TouchableOpacity
                key={question.question_id}
                style={styles.questionCard}
                onPress={() => handleQuestionPress(question)}
              >
                <View style={styles.questionHeader}>
                  <View style={styles.typeIndicator}>
                    <Ionicons 
                      name={question.type === 'flashcard' ? 'layers' : 'document-text'} 
                      size={16} 
                      color={question.type === 'flashcard' ? '#3b82f6' : '#10b981'} 
                    />
                    <Text style={styles.typeText}>{question.type}</Text>
                  </View>
                  <View style={[styles.badge, styles[`badge${question.difficulty}`]]}>
                    <Text style={styles.badgeText}>{question.difficulty}</Text>
                  </View>
                  <Ionicons name="bookmark" size={20} color="#f59e0b" />
                </View>
                
                <Text style={styles.questionTitle}>{question.title}</Text>
                <Text style={styles.categoryBadge}>{question.category_name}</Text>
                
                {question.reference && (
                  <Text style={styles.reference}>{question.reference}</Text>
                )}
              </TouchableOpacity>
            ))
          ) : (
            <View style={styles.emptyState}>
              <Ionicons name="bookmark-outline" size={64} color="#64748b" />
              <Text style={styles.emptyText}>No bookmarks yet</Text>
              <Text style={styles.emptySubtext}>Bookmark questions to find them here later</Text>
              <TouchableOpacity 
                style={styles.exploreButton}
                onPress={() => router.push('/(tabs)/flashcards')}
              >
                <Text style={styles.exploreButtonText}>Explore Questions</Text>
              </TouchableOpacity>
            </View>
          )}
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
  scrollView: {
    flex: 1,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  header: {
    padding: 24,
    paddingBottom: 16,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
  },
  subtitle: {
    fontSize: 16,
    color: '#94a3b8',
    marginTop: 4,
  },
  section: {
    padding: 24,
    paddingTop: 8,
    gap: 12,
  },
  questionCard: {
    backgroundColor: '#1e293b',
    padding: 16,
    borderRadius: 12,
    gap: 8,
  },
  questionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  typeIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    flex: 1,
  },
  typeText: {
    fontSize: 12,
    color: '#94a3b8',
    textTransform: 'capitalize',
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
  questionTitle: {
    fontSize: 16,
    color: '#fff',
    fontWeight: '600',
  },
  categoryBadge: {
    fontSize: 12,
    color: '#64748b',
  },
  reference: {
    fontSize: 12,
    color: '#94a3b8',
    fontStyle: 'italic',
  },
  emptyState: {
    alignItems: 'center',
    paddingVertical: 48,
    gap: 12,
  },
  emptyText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#94a3b8',
  },
  emptySubtext: {
    fontSize: 14,
    color: '#64748b',
    textAlign: 'center',
  },
  exploreButton: {
    backgroundColor: '#2563eb',
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 8,
    marginTop: 8,
  },
  exploreButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
});