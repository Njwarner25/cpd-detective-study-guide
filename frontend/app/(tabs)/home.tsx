import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet, ActivityIndicator, RefreshControl } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useAuth } from '../../contexts/AuthContext';
import { useRouter } from 'expo-router';
import { statsService, categoryService } from '../../services/api';

export default function Home() {
  const { user, sessionToken } = useAuth();
  const router = useRouter();
  const [stats, setStats] = useState<any>(null);
  const [categories, setCategories] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const loadData = async () => {
    try {
      const [statsData, categoriesData] = await Promise.all([
        statsService.getStats(sessionToken || undefined),
        categoryService.getCategories()
      ]);
      setStats(statsData);
      setCategories(categoriesData);
    } catch (error) {
      console.error('Failed to load data:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    loadData();
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
          <Text style={styles.greeting}>Welcome back,</Text>
          <Text style={styles.name}>{user?.name || 'Officer'}</Text>
        </View>

        {/* Stats Cards */}
        <View style={styles.statsGrid}>
          <View style={styles.statCard}>
            <Ionicons name="layers" size={24} color="#3b82f6" />
            <Text style={styles.statValue}>{stats?.total_flashcards || 0}</Text>
            <Text style={styles.statLabel}>Flashcards</Text>
            <Text style={styles.statSubLabel}>{stats?.attempted_flashcards || 0} studied</Text>
          </View>

          <View style={styles.statCard}>
            <Ionicons name="document-text" size={24} color="#10b981" />
            <Text style={styles.statValue}>{stats?.total_scenarios || 0}</Text>
            <Text style={styles.statLabel}>Scenarios</Text>
            <Text style={styles.statSubLabel}>{stats?.attempted_scenarios || 0} completed</Text>
          </View>

          <View style={styles.statCard}>
            <Ionicons name="bookmark" size={24} color="#f59e0b" />
            <Text style={styles.statValue}>{stats?.bookmarks || 0}</Text>
            <Text style={styles.statLabel}>Bookmarked</Text>
          </View>

          <View style={styles.statCard}>
            <Ionicons name="trophy" size={24} color="#8b5cf6" />
            <Text style={styles.statValue}>
              {stats?.average_score ? `${Math.round(stats.average_score)}%` : '-'}
            </Text>
            <Text style={styles.statLabel}>Avg Score</Text>
            <Text style={styles.statSubLabel}>{stats?.total_responses || 0} responses</Text>
          </View>
        </View>

        {/* Quick Actions */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Quick Start</Text>
          
          {/* NEW: Full Practice Exam */}
          <TouchableOpacity 
            style={[styles.actionCard, styles.featuredCard]}
            onPress={() => router.push('/practice-exam')}
          >
            <View style={[styles.actionIcon, { backgroundColor: '#8b5cf6' }]}>
              <Ionicons name="trophy" size={24} color="#fff" />
            </View>
            <View style={styles.actionContent}>
              <Text style={styles.actionTitle}>Full Practice Exam ⭐</Text>
              <Text style={styles.actionDescription}>105 questions • 90-minute timer • Simulates actual test</Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color="#8b5cf6" />
          </TouchableOpacity>
          
          <TouchableOpacity 
            style={styles.actionCard}
            onPress={() => router.push('/flashcards')}
          >
            <View style={[styles.actionIcon, { backgroundColor: '#3b82f6' }]}>
              <Ionicons name="layers" size={24} color="#fff" />
            </View>
            <View style={styles.actionContent}>
              <Text style={styles.actionTitle}>Study Flashcards</Text>
              <Text style={styles.actionDescription}>Review questions on CPD directives and Illinois law</Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color="#64748b" />
          </TouchableOpacity>

          <TouchableOpacity 
            style={styles.actionCard}
            onPress={() => router.push('/scenarios')}
          >
            <View style={[styles.actionIcon, { backgroundColor: '#10b981' }]}>
              <Ionicons name="document-text" size={24} color="#fff" />
            </View>
            <View style={styles.actionContent}>
              <Text style={styles.actionTitle}>Practice Scenarios</Text>
              <Text style={styles.actionDescription}>7-minute timed scenarios with AI grading</Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color="#64748b" />
          </TouchableOpacity>

          <TouchableOpacity 
            style={styles.actionCard}
            onPress={() => router.push('/bookmarks')}
          >
            <View style={[styles.actionIcon, { backgroundColor: '#f59e0b' }]}>
              <Ionicons name="bookmark" size={24} color="#fff" />
            </View>
            <View style={styles.actionContent}>
              <Text style={styles.actionTitle}>Bookmarked Questions</Text>
              <Text style={styles.actionDescription}>Review your saved questions</Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color="#64748b" />
          </TouchableOpacity>
        </View>

        {/* Categories */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Study Categories</Text>
          {categories.map((category) => (
            <View key={category.category_id} style={styles.categoryCard}>
              <View style={styles.categoryHeader}>
                <Ionicons name="folder" size={20} color="#2563eb" />
                <Text style={styles.categoryName}>{category.name}</Text>
              </View>
              <Text style={styles.categoryDescription}>{category.description}</Text>
            </View>
          ))}
        </View>

        {user?.role === 'admin' && (
          <View style={styles.section}>
            <TouchableOpacity 
              style={styles.adminButton}
              onPress={() => router.push('/admin')}
            >
              <Ionicons name="settings" size={20} color="#fff" />
              <Text style={styles.adminButtonText}>Admin Panel</Text>
            </TouchableOpacity>
          </View>
        )}
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
  greeting: {
    fontSize: 16,
    color: '#94a3b8',
  },
  name: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    marginTop: 4,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    padding: 16,
    gap: 12,
  },
  statCard: {
    flex: 1,
    minWidth: '45%',
    backgroundColor: '#1e293b',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    gap: 8,
  },
  statValue: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
  },
  statLabel: {
    fontSize: 14,
    color: '#cbd5e1',
    fontWeight: '600',
  },
  statSubLabel: {
    fontSize: 12,
    color: '#64748b',
  },
  section: {
    padding: 24,
    paddingTop: 8,
    gap: 12,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 8,
  },
  actionCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1e293b',
    padding: 16,
    borderRadius: 12,
    gap: 12,
  },
  featuredCard: {
    borderWidth: 2,
    borderColor: '#8b5cf6',
    backgroundColor: '#1e1b4b',
  },
  actionIcon: {
    width: 48,
    height: 48,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
  },
  actionContent: {
    flex: 1,
    gap: 4,
  },
  actionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#fff',
  },
  actionDescription: {
    fontSize: 14,
    color: '#94a3b8',
  },
  categoryCard: {
    backgroundColor: '#1e293b',
    padding: 16,
    borderRadius: 12,
    gap: 8,
  },
  categoryHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  categoryName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#fff',
  },
  categoryDescription: {
    fontSize: 14,
    color: '#94a3b8',
    marginLeft: 28,
  },
  adminButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#7c3aed',
    padding: 16,
    borderRadius: 12,
    gap: 8,
  },
  adminButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});