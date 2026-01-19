import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet, ActivityIndicator } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useAuth } from '../../contexts/AuthContext';
import { useRouter } from 'expo-router';
import { questionService, categoryService } from '../../services/api';

export default function Scenarios() {
  const { sessionToken } = useAuth();
  const router = useRouter();
  const [scenarios, setScenarios] = useState<any[]>([]);
  const [categories, setCategories] = useState<any[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, [selectedCategory]);

  const loadData = async () => {
    try {
      const [scenariosData, categoriesData] = await Promise.all([
        questionService.getQuestions('scenario', selectedCategory || undefined, sessionToken || undefined),
        categoryService.getCategories()
      ]);
      setScenarios(scenariosData);
      setCategories(categoriesData);
    } catch (error) {
      console.error('Failed to load scenarios:', error);
    } finally {
      setLoading(false);
    }
  };

  const startScenario = (scenarioId: string) => {
    router.push({
      pathname: '/practice-scenario',
      params: { scenarioId }
    });
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
          <Text style={styles.title}>Practice Scenarios</Text>
          <Text style={styles.subtitle}>{scenarios.length} scenarios available</Text>
          <View style={styles.infoCard}>
            <Ionicons name="time" size={20} color="#f59e0b" />
            <Text style={styles.infoText}>Each scenario has a 7-minute timer</Text>
          </View>
        </View>

        {/* Category Filter */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Select Category</Text>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.categoryScroll}>
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
          </ScrollView>
        </View>

        {/* Gold Scenarios Section */}
        {scenarios.filter(s => s.is_gold).length > 0 && (
          <View style={styles.goldSection}>
            <View style={styles.goldHeader}>
              <Ionicons name="star" size={24} color="#fbbf24" />
              <Text style={styles.goldTitle}>Gold Scenarios</Text>
            </View>
            <Text style={styles.goldSubtitle}>
              Based on previous practice scenarios from the testing company
            </Text>
            {scenarios.filter(s => s.is_gold).map((scenario) => (
              <TouchableOpacity
                key={scenario.question_id}
                style={styles.goldScenarioCard}
                onPress={() => startScenario(scenario.question_id)}
              >
                <View style={styles.scenarioHeader}>
                  <View style={styles.goldBadge}>
                    <Ionicons name="star" size={12} color="#78350f" />
                    <Text style={styles.goldBadgeText}>GOLD</Text>
                  </View>
                  <View style={[styles.badge, styles[`badge${scenario.difficulty}`]]}>
                    <Text style={styles.badgeText}>{scenario.difficulty}</Text>
                  </View>
                </View>
                <Text style={styles.goldScenarioTitle}>{scenario.title}</Text>
                <Text style={styles.scenarioPreview} numberOfLines={3}>
                  {scenario.content}
                </Text>
                <View style={styles.goldStartButton}>
                  <Text style={styles.goldStartButtonText}>Start Scenario</Text>
                  <Ionicons name="arrow-forward" size={16} color="#fbbf24" />
                </View>
              </TouchableOpacity>
            ))}
          </View>
        )}

        {/* Regular Scenarios List */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>All Scenarios</Text>
          {scenarios.filter(s => !s.is_gold).length > 0 ? (
            scenarios.filter(s => !s.is_gold).map((scenario) => (
              <TouchableOpacity
                key={scenario.question_id}
                style={styles.scenarioCard}
                onPress={() => startScenario(scenario.question_id)}
              >
                <View style={styles.scenarioHeader}>
                  <View style={[styles.badge, styles[`badge${scenario.difficulty}`]]}>
                    <Text style={styles.badgeText}>{scenario.difficulty}</Text>
                  </View>
                  <Text style={styles.categoryBadge}>{scenario.category_name}</Text>
                </View>
                <Text style={styles.scenarioTitle}>{scenario.title}</Text>
                <Text style={styles.scenarioPreview} numberOfLines={3}>
                  {scenario.content}
                </Text>
                {scenario.reference && (
                  <Text style={styles.reference}>{scenario.reference}</Text>
                )}
                <View style={styles.startButton}>
                  <Text style={styles.startButtonText}>Start Scenario</Text>
                  <Ionicons name="arrow-forward" size={16} color="#2563eb" />
                </View>
              </TouchableOpacity>
            ))
          ) : (
            <View style={styles.emptyState}>
              <Ionicons name="document-text-outline" size={64} color="#64748b" />
              <Text style={styles.emptyText}>No scenarios found</Text>
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
  infoCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#422006',
    padding: 12,
    borderRadius: 8,
    gap: 8,
    marginTop: 12,
  },
  infoText: {
    color: '#fbbf24',
    fontSize: 14,
    fontWeight: '500',
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
  scenarioCard: {
    backgroundColor: '#1e293b',
    padding: 16,
    borderRadius: 12,
    gap: 12,
  },
  scenarioHeader: {
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
    fontSize: 18,
    color: '#fff',
    fontWeight: '600',
  },
  scenarioPreview: {
    fontSize: 14,
    color: '#94a3b8',
    lineHeight: 20,
  },
  reference: {
    fontSize: 12,
    color: '#94a3b8',
    fontStyle: 'italic',
  },
  startButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 6,
    paddingVertical: 8,
    borderTopWidth: 1,
    borderTopColor: '#334155',
    marginTop: 4,
  },
  startButtonText: {
    color: '#2563eb',
    fontSize: 14,
    fontWeight: '600',
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