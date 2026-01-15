import React, { useEffect, useState, useCallback } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  RefreshControl,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useAuth } from '../contexts/AuthContext';
import { useRouter } from 'expo-router';
import { bookmarkService } from '../services/api';

export default function Bookmarks() {
  const { sessionToken } = useAuth();
  const router = useRouter();
  const [bookmarks, setBookmarks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadBookmarks();
  }, []);

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

  const onRefresh = useCallback(() => {
    setRefreshing(true);
    loadBookmarks();
  }, []);

  const handleRemoveBookmark = async (questionId: string) => {
    try {
      await bookmarkService.toggleBookmark(questionId, sessionToken || undefined);
      setBookmarks(prev => prev.filter(b => b.question_id !== questionId));
    } catch (error) {
      console.error('Failed to remove bookmark:', error);
    }
  };

  const handleOpenItem = (item: any) => {
    if (item.type === 'flashcard') {
      router.push({
        pathname: '/study',
        params: { category: item.category_id || 'all' }
      });
    } else if (item.type === 'scenario') {
      router.push({
        pathname: '/practice-scenario',
        params: { scenarioId: item.question_id }
      });
    } else if (item.type === 'multiple_choice') {
      router.push({
        pathname: '/quiz',
        params: { count: '25' }
      });
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'flashcard':
        return 'layers';
      case 'scenario':
        return 'document-text';
      case 'multiple_choice':
        return 'checkbox';
      default:
        return 'bookmark';
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'flashcard':
        return '#10b981';
      case 'scenario':
        return '#f59e0b';
      case 'multiple_choice':
        return '#2563eb';
      default:
        return '#64748b';
    }
  };

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.header}>
          <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
            <Ionicons name="arrow-back" size={24} color="#fff" />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Bookmarks</Text>
          <View style={styles.backButton} />
        </View>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#2563eb" />
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
          <Ionicons name="arrow-back" size={24} color="#fff" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Bookmarks</Text>
        <View style={styles.backButton} />
      </View>

      {bookmarks.length === 0 ? (
        <View style={styles.emptyContainer}>
          <Ionicons name="bookmark-outline" size={80} color="#334155" />
          <Text style={styles.emptyTitle}>No Bookmarks Yet</Text>
          <Text style={styles.emptyText}>
            Save questions for later by tapping the bookmark icon while studying
          </Text>
        </View>
      ) : (
        <ScrollView
          style={styles.scrollView}
          contentContainerStyle={styles.scrollContent}
          refreshControl={
            <RefreshControl
              refreshing={refreshing}
              onRefresh={onRefresh}
              tintColor="#2563eb"
            />
          }
        >
          <Text style={styles.countText}>{bookmarks.length} bookmarked item{bookmarks.length !== 1 ? 's' : ''}</Text>
          
          {bookmarks.map((item) => (
            <TouchableOpacity
              key={item.question_id}
              style={styles.bookmarkCard}
              onPress={() => handleOpenItem(item)}
              activeOpacity={0.7}
            >
              <View style={[styles.typeIcon, { backgroundColor: getTypeColor(item.type) + '20' }]}>
                <Ionicons name={getTypeIcon(item.type)} size={24} color={getTypeColor(item.type)} />
              </View>
              
              <View style={styles.cardContent}>
                <View style={styles.cardHeader}>
                  <View style={[styles.typeBadge, { backgroundColor: getTypeColor(item.type) }]}>
                    <Text style={styles.typeBadgeText}>{item.type.replace('_', ' ')}</Text>
                  </View>
                  <Text style={styles.categoryText}>{item.category_name}</Text>
                </View>
                
                <Text style={styles.titleText} numberOfLines={2}>
                  {item.title || item.question || 'Untitled'}
                </Text>
                
                {item.reference && (
                  <Text style={styles.referenceText} numberOfLines={1}>
                    {item.reference}
                  </Text>
                )}
              </View>
              
              <TouchableOpacity
                style={styles.removeButton}
                onPress={() => handleRemoveBookmark(item.question_id)}
                hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
              >
                <Ionicons name="bookmark" size={24} color="#f59e0b" />
              </TouchableOpacity>
            </TouchableOpacity>
          ))}
        </ScrollView>
      )}
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
  backButton: {
    padding: 8,
    width: 40,
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
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
    padding: 32,
  },
  emptyTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#fff',
    marginTop: 24,
    marginBottom: 8,
  },
  emptyText: {
    fontSize: 16,
    color: '#64748b',
    textAlign: 'center',
    lineHeight: 24,
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    padding: 16,
    paddingBottom: 32,
  },
  countText: {
    fontSize: 14,
    color: '#64748b',
    marginBottom: 16,
  },
  bookmarkCard: {
    backgroundColor: '#1e293b',
    borderRadius: 12,
    padding: 16,
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
    gap: 12,
  },
  typeIcon: {
    width: 48,
    height: 48,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
  },
  cardContent: {
    flex: 1,
    gap: 6,
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  typeBadge: {
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 4,
  },
  typeBadgeText: {
    color: '#fff',
    fontSize: 10,
    fontWeight: '600',
    textTransform: 'capitalize',
  },
  categoryText: {
    fontSize: 12,
    color: '#64748b',
  },
  titleText: {
    fontSize: 15,
    color: '#fff',
    fontWeight: '500',
    lineHeight: 20,
  },
  referenceText: {
    fontSize: 12,
    color: '#94a3b8',
    fontStyle: 'italic',
  },
  removeButton: {
    padding: 8,
  },
});
