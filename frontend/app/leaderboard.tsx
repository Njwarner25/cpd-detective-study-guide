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
import { statsService } from '../services/api';

export default function Leaderboard() {
  const { sessionToken, isGuest } = useAuth();
  const router = useRouter();
  const [leaderboard, setLeaderboard] = useState<any[]>([]);
  const [userRank, setUserRank] = useState<number | null>(null);
  const [userStats, setUserStats] = useState<any>(null);
  const [totalParticipants, setTotalParticipants] = useState(0);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    loadLeaderboard();
  }, []);

  const loadLeaderboard = async () => {
    try {
      const data = await statsService.getLeaderboard(sessionToken || undefined);
      setLeaderboard(data.leaderboard || []);
      setUserRank(data.user_rank);
      setUserStats(data.user_stats);
      setTotalParticipants(data.total_participants || 0);
      setMessage(data.message || null);
    } catch (error) {
      console.error('Failed to load leaderboard:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = useCallback(() => {
    setRefreshing(true);
    loadLeaderboard();
  }, []);

  const getRankIcon = (rank: number) => {
    if (rank === 1) return { name: 'trophy', color: '#fbbf24' };
    if (rank === 2) return { name: 'medal', color: '#94a3b8' };
    if (rank === 3) return { name: 'medal', color: '#cd7f32' };
    return null;
  };

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.header}>
          <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
            <Ionicons name="arrow-back" size={24} color="#fff" />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Leaderboard</Text>
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
        <Text style={styles.headerTitle}>Leaderboard</Text>
        <View style={styles.backButton} />
      </View>

      {isGuest ? (
        <View style={styles.guestContainer}>
          <Ionicons name="trophy-outline" size={80} color="#334155" />
          <Text style={styles.guestTitle}>Register to See Rankings</Text>
          <Text style={styles.guestText}>
            Create an account to track your progress and see how you rank against other detectives-in-training!
          </Text>
          <TouchableOpacity 
            style={styles.registerButton}
            onPress={() => router.push('/(auth)/login')}
          >
            <Text style={styles.registerButtonText}>Register Now</Text>
          </TouchableOpacity>
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
          {/* User's Current Rank */}
          {userStats && (
            <View style={styles.userRankCard}>
              <View style={styles.userRankHeader}>
                <Ionicons name="person-circle" size={40} color="#2563eb" />
                <View style={styles.userRankInfo}>
                  <Text style={styles.userRankLabel}>Your Ranking</Text>
                  <Text style={styles.userRankText}>
                    #{userRank} of {totalParticipants} participants
                  </Text>
                </View>
              </View>
              <View style={styles.userStatsRow}>
                <View style={styles.userStatItem}>
                  <Text style={styles.userStatValue}>{userStats.avg_score}%</Text>
                  <Text style={styles.userStatLabel}>Avg Score</Text>
                </View>
                <View style={styles.userStatItem}>
                  <Text style={styles.userStatValue}>{userStats.best_score}%</Text>
                  <Text style={styles.userStatLabel}>Best Score</Text>
                </View>
                <View style={styles.userStatItem}>
                  <Text style={styles.userStatValue}>{userStats.total_attempts}</Text>
                  <Text style={styles.userStatLabel}>Attempts</Text>
                </View>
              </View>
            </View>
          )}

          {/* Leaderboard Table */}
          <View style={styles.tableContainer}>
            <Text style={styles.tableTitle}>Top Performers</Text>
            
            {leaderboard.length === 0 ? (
              <View style={styles.emptyState}>
                <Ionicons name="podium-outline" size={48} color="#334155" />
                <Text style={styles.emptyText}>No scores yet. Be the first!</Text>
              </View>
            ) : (
              <>
                <View style={styles.tableHeader}>
                  <Text style={[styles.tableHeaderText, { width: 50 }]}>Rank</Text>
                  <Text style={[styles.tableHeaderText, { flex: 1 }]}>Name</Text>
                  <Text style={[styles.tableHeaderText, { width: 60 }]}>Avg</Text>
                  <Text style={[styles.tableHeaderText, { width: 60 }]}>Best</Text>
                </View>
                
                {leaderboard.map((entry, index) => {
                  const rankIcon = getRankIcon(entry.rank);
                  return (
                    <View 
                      key={index} 
                      style={[
                        styles.tableRow,
                        entry.is_current_user && styles.currentUserRow
                      ]}
                    >
                      <View style={[styles.rankCell, { width: 50 }]}>
                        {rankIcon ? (
                          <Ionicons name={rankIcon.name as any} size={20} color={rankIcon.color} />
                        ) : (
                          <Text style={styles.rankText}>{entry.rank}</Text>
                        )}
                      </View>
                      <View style={[styles.nameCell, { flex: 1 }]}>
                        <Text style={styles.nameText} numberOfLines={1}>
                          {entry.name}
                          {entry.is_current_user && ' (You)'}
                        </Text>
                      </View>
                      <Text style={[styles.scoreText, { width: 60 }]}>{entry.avg_score}%</Text>
                      <Text style={[styles.scoreText, { width: 60 }]}>{entry.best_score}%</Text>
                    </View>
                  );
                })}
              </>
            )}
          </View>

          <Text style={styles.disclaimer}>
            Rankings are based on scenario response scores graded by AI.
          </Text>
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
  guestContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 32,
  },
  guestTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#fff',
    marginTop: 24,
    marginBottom: 8,
  },
  guestText: {
    fontSize: 16,
    color: '#64748b',
    textAlign: 'center',
    lineHeight: 24,
    marginBottom: 24,
  },
  registerButton: {
    backgroundColor: '#2563eb',
    paddingHorizontal: 32,
    paddingVertical: 14,
    borderRadius: 12,
  },
  registerButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    padding: 16,
    paddingBottom: 32,
  },
  userRankCard: {
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 20,
    marginBottom: 20,
    borderWidth: 1,
    borderColor: '#2563eb',
  },
  userRankHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 16,
    marginBottom: 16,
  },
  userRankInfo: {
    flex: 1,
  },
  userRankLabel: {
    fontSize: 14,
    color: '#64748b',
  },
  userRankText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  userStatsRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    borderTopWidth: 1,
    borderTopColor: '#334155',
    paddingTop: 16,
  },
  userStatItem: {
    alignItems: 'center',
  },
  userStatValue: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2563eb',
  },
  userStatLabel: {
    fontSize: 12,
    color: '#64748b',
    marginTop: 4,
  },
  tableContainer: {
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 16,
    marginBottom: 16,
  },
  tableTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 16,
  },
  emptyState: {
    alignItems: 'center',
    padding: 32,
  },
  emptyText: {
    fontSize: 16,
    color: '#64748b',
    marginTop: 12,
  },
  tableHeader: {
    flexDirection: 'row',
    paddingBottom: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#334155',
    marginBottom: 8,
  },
  tableHeaderText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#64748b',
    textTransform: 'uppercase',
  },
  tableRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#1e293b',
  },
  currentUserRow: {
    backgroundColor: '#2563eb20',
    borderRadius: 8,
    marginHorizontal: -8,
    paddingHorizontal: 8,
  },
  rankCell: {
    alignItems: 'center',
  },
  rankText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#94a3b8',
  },
  nameCell: {
    paddingRight: 8,
  },
  nameText: {
    fontSize: 15,
    color: '#fff',
  },
  scoreText: {
    fontSize: 15,
    color: '#10b981',
    fontWeight: '600',
    textAlign: 'center',
  },
  disclaimer: {
    fontSize: 12,
    color: '#64748b',
    textAlign: 'center',
    fontStyle: 'italic',
  },
});
