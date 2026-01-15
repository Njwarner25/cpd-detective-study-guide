import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet, ActivityIndicator } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useAuth } from '../../contexts/AuthContext';
import { useRouter } from 'expo-router';
import { questionService, categoryService } from '../../services/api';

export default function Flashcards() {
  const { sessionToken } = useAuth();
  const router = useRouter();
  const [questions, setQuestions] = useState<any[]>([]);
  const [categories, setCategories] = useState<any[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, [selectedCategory]);

  const loadData = async () => {
    try {
      const [questionsData, categoriesData] = await Promise.all([
        questionService.getQuestions('flashcard', selectedCategory || undefined, sessionToken || undefined),
        categoryService.getCategories()
      ]);
      setQuestions(questionsData);
      setCategories(categoriesData);
    } catch (error) {
      console.error('Failed to load flashcards:', error);
    } finally {
      setLoading(false);
    }
  };

  const startStudy = () => {
    if (questions.length > 0) {
      router.push({
        pathname: '/study',
        params: { category: selectedCategory || 'all' }
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
      <ScrollView style={styles.scrollView}>
        <View style={styles.header}>
          <Text style={styles.title}>Flashcards</Text>
          <Text style={styles.subtitle}>{questions.length} questions available</Text>
        </View>

        {/* Category Filter */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Select Category</Text>
          <View style={styles.categoryContainer}>
            <TouchableOpacity
              style={[styles.categoryChip, !selectedCategory && styles.categoryChipActive]}
              onPress={() => setSelectedCategory(null)}
            >
              <Text style={[styles.categoryChipText, !selectedCategory && styles.categoryChipTextActive]}>
                All
              </Text>
            </TouchableOpacity>
            {categories.map((category) => (
              <TouchableOpacity
                key={category.category_id}
                style={[
                  styles.categoryChip,
                  selectedCategory === category.category_id && styles.categoryChipActive
                ]}
                onPress={() => setSelectedCategory(category.category_id)}
              >
                <Text style={[
                  styles.categoryChipText,
                  selectedCategory === category.category_id && styles.categoryChipTextActive
                ]}>
                  {category.name}
                </Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* Questions List */}
        <View style={styles.section}>
          {questions.length > 0 ? (
            <>
              <TouchableOpacity style={styles.startButton} onPress={startStudy}>
                <Ionicons name="play" size={24} color="#fff" />
                <Text style={styles.startButtonText}>Start Studying</Text>
              </TouchableOpacity>

              <Text style={styles.sectionTitle}>Available Questions</Text>
              {questions.map((question) => (
                <View key={question.question_id} style={styles.questionCard}>
                  <View style={styles.questionHeader}>
                    <View style={[styles.badge, styles[`badge${question.difficulty}`]]}>
                      <Text style={styles.badgeText}>{question.difficulty}</Text>
                    </View>
                    <Text style={styles.categoryBadge}>{question.category_name}</Text>
                  </View>
                  <Text style={styles.questionTitle}>{question.title}</Text>
                  {question.reference && (
                    <Text style={styles.reference}>{question.reference}</Text>
                  )}
                </View>
              ))}
            </>
          ) : (
            <View style={styles.emptyState}>
              <Ionicons name="layers-outline" size={64} color="#64748b" />
              <Text style={styles.emptyText}>No flashcards found</Text>
              <Text style={styles.emptySubtext}>Try selecting a different category</Text>
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
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 8,
  },
  categoryScroll: {
    flexDirection: 'row',
  },
  categoryChip: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    backgroundColor: '#1e293b',
    marginRight: 8,
    borderWidth: 1,
    borderColor: '#334155',
  },
  categoryChipActive: {
    backgroundColor: '#2563eb',
    borderColor: '#2563eb',
  },
  categoryChipText: {
    color: '#94a3b8',
    fontSize: 14,
    fontWeight: '600',
  },
  categoryChipTextActive: {
    color: '#fff',
  },
  startButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#2563eb',
    padding: 16,
    borderRadius: 12,
    gap: 8,
    marginBottom: 16,
  },
  startButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
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
    fontSize: 16,
    color: '#fff',
    fontWeight: '500',
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
  },
});
