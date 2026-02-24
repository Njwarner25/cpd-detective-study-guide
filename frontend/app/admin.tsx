import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  RefreshControl,
  TextInput,
  Alert,
  Platform,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import { useAuth } from '../contexts/AuthContext';
import { adminService } from '../services/api';

const showAlert = (title: string, message: string, buttons?: Array<{text: string, style?: string, onPress?: () => void}>) => {
  if (Platform.OS === 'web') {
    if (buttons && buttons.length > 1) {
      const confirmButton = buttons.find(b => b.style !== 'cancel');
      const result = window.confirm(title + '\n\n' + message);
      if (result && confirmButton?.onPress) {
        confirmButton.onPress();
      }
    } else if (buttons && buttons.length === 1 && buttons[0].onPress) {
      window.alert(title + '\n\n' + message);
      buttons[0].onPress();
    } else {
      window.alert(title + '\n\n' + message);
    }
  } else {
    Alert.alert(title, message, buttons as any);
  }
};

interface Analytics {
  users: {
    total_registered: number;
    total_guest_sessions: number;
    active_today: number;
    active_this_week: number;
    active_this_month: number;
    new_registrations_week: number;
  };
  content: {
    total_flashcards: number;
    total_scenarios: number;
    total_mcqs: number;
    total_questions: number;
  };
  activity: {
    total_scenario_responses: number;
    total_quiz_attempts: number;
    average_scenario_score: number | null;
  };
  popular_categories: Array<{ category: string; attempts: number }>;
  recent_activity: Array<{
    user_name: string;
    question_id: string;
    ai_grade: number | null;
    submitted_at: string;
  }>;
  daily_active_users: Array<{ date: string; day: string; active_users: number }>;
}

interface UserInfo {
  email: string;
  name: string;
  role: string;
  has_paid: boolean;
  granted_by: string | null;
  created_at: string;
}

export default function AdminDashboard() {
  const router = useRouter();
  const { user, sessionToken } = useAuth();
  const [analytics, setAnalytics] = useState<Analytics | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'analytics' | 'users'>('analytics');

  // Premium grant state
  const [grantEmail, setGrantEmail] = useState('');
  const [granting, setGranting] = useState(false);

  // User list state
  const [users, setUsers] = useState<UserInfo[]>([]);
  const [loadingUsers, setLoadingUsers] = useState(false);
  const [userFilter, setUserFilter] = useState('');

  const fetchAnalytics = async () => {
    try {
      setError(null);
      const data = await adminService.getAnalytics(sessionToken || undefined);
      setAnalytics(data);
    } catch (err: any) {
      console.error('Failed to fetch analytics:', err);
      if (err.response?.status === 403) {
        setError('Admin access required');
      } else {
        setError('Failed to load analytics');
      }
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const fetchUsers = async () => {
    try {
      setLoadingUsers(true);
      const data = await adminService.getUsers(sessionToken || undefined);
      setUsers(data.users || []);
    } catch (err: any) {
      console.error('Failed to fetch users:', err);
      showAlert('Error', 'Failed to load users');
    } finally {
      setLoadingUsers(false);
    }
  };

  useEffect(() => {
    fetchAnalytics();
  }, [sessionToken]);

  useEffect(() => {
    if (activeTab === 'users' && users.length === 0) {
      fetchUsers();
    }
  }, [activeTab]);

  const onRefresh = () => {
    setRefreshing(true);
    fetchAnalytics();
    if (activeTab === 'users') {
      fetchUsers();
    }
  };

  const handleGrantPremium = async () => {
    if (!grantEmail.trim()) {
      showAlert('Error', 'Please enter an email address');
      return;
    }
    setGranting(true);
    try {
      const result = await adminService.grantPremium(grantEmail.trim(), sessionToken || undefined);
      showAlert('Success', result.message);
      setGrantEmail('');
      fetchUsers();
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Failed to grant premium';
      showAlert('Error', msg);
    } finally {
      setGranting(false);
    }
  };

  const handleRevokePremium = async (email: string) => {
    showAlert('Confirm Revoke', 'Are you sure you want to revoke premium access from ' + email + '?', [
      { text: 'Cancel', style: 'cancel' },
      {
        text: 'Revoke',
        style: 'destructive',
        onPress: async () => {
          try {
            const result = await adminService.revokePremium(email, sessionToken || undefined);
            showAlert('Success', result.message);
            fetchUsers();
          } catch (err: any) {
            const msg = err.response?.data?.detail || 'Failed to revoke premium';
            showAlert('Error', msg);
          }
        },
      },
    ]);
  };

  const handleGrantFromList = async (email: string) => {
    try {
      const result = await adminService.grantPremium(email, sessionToken || undefined);
      showAlert('Success', result.message);
      fetchUsers();
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Failed to grant premium';
      showAlert('Error', msg);
    }
  };

  const filteredUsers = users.filter(u => {
    if (!userFilter) return true;
    const q = userFilter.toLowerCase();
    return u.email.toLowerCase().includes(q) || u.name.toLowerCase().includes(q);
  });

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#2563eb" />
          <Text style={styles.loadingText}>Loading analytics...</Text>
        </View>
      </SafeAreaView>
    );
  }

  if (error) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.header}>
          <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
            <Ionicons name="arrow-back" size={24} color="#fff" />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Admin Dashboard</Text>
          <View style={styles.backButton} />
        </View>
        <View style={styles.errorContainer}>
          <Ionicons name="lock-closed" size={64} color="#ef4444" />
          <Text style={styles.errorText}>{error}</Text>
          <TouchableOpacity style={styles.retryButton} onPress={() => router.back()}>
            <Text style={styles.retryButtonText}>Go Back</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  const maxDailyUsers = Math.max(...(analytics?.daily_active_users.map(d => d.active_users) || [1]));

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
          <Ionicons name="arrow-back" size={24} color="#fff" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Admin Dashboard</Text>
        <TouchableOpacity onPress={onRefresh} style={styles.backButton}>
          <Ionicons name="refresh" size={24} color="#fff" />
        </TouchableOpacity>
      </View>

      {/* Tab Switcher */}
      <View style={styles.tabBar}>
        <TouchableOpacity
          style={[styles.tab, activeTab === 'analytics' && styles.activeTab]}
          onPress={() => setActiveTab('analytics')}
        >
          <Ionicons name="bar-chart" size={18} color={activeTab === 'analytics' ? '#fff' : '#64748b'} />
          <Text style={[styles.tabText, activeTab === 'analytics' && styles.activeTabText]}>Analytics</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.tab, activeTab === 'users' && styles.activeTab]}
          onPress={() => setActiveTab('users')}
        >
          <Ionicons name="people" size={18} color={activeTab === 'users' ? '#fff' : '#64748b'} />
          <Text style={[styles.tabText, activeTab === 'users' && styles.activeTabText]}>Users & Premium</Text>
        </TouchableOpacity>
      </View>

      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor="#2563eb" />
        }
      >
        {activeTab === 'users' ? (
          <>
            {/* Grant Premium Section */}
            <View style={styles.section}>
              <View style={styles.sectionHeader}>
                <Ionicons name="star" size={20} color="#f59e0b" />
                <Text style={styles.sectionTitle}>Grant Premium Access</Text>
              </View>
              <Text style={styles.grantDescription}>
                Enter a registered user's email to grant them premium access.
              </Text>
              <View style={styles.grantRow}>
                <TextInput
                  style={styles.grantInput}
                  placeholder="user@email.com"
                  placeholderTextColor="#64748b"
                  value={grantEmail}
                  onChangeText={setGrantEmail}
                  keyboardType="email-address"
                  autoCapitalize="none"
                />
                <TouchableOpacity
                  style={[styles.grantButton, granting && styles.buttonDisabled]}
                  onPress={handleGrantPremium}
                  disabled={granting}
                >
                  {granting ? (
                    <ActivityIndicator size="small" color="#fff" />
                  ) : (
                    <><Ionicons name="star" size={16} color="#fff" /><Text style={styles.grantButtonText}>Grant</Text></>
                  )}
                </TouchableOpacity>
              </View>
            </View>

            {/* User List Section */}
            <View style={styles.section}>
              <View style={styles.sectionHeader}>
                <Ionicons name="people" size={20} color="#2563eb" />
                <Text style={styles.sectionTitle}>All Users ({users.length})</Text>
                <TouchableOpacity onPress={fetchUsers} style={styles.refreshUsersBtn}>
                  <Ionicons name="refresh" size={16} color="#64748b" />
                </TouchableOpacity>
              </View>

              <TextInput
                style={styles.searchInput}
                placeholder="Search by email or name..."
                placeholderTextColor="#64748b"
                value={userFilter}
                onChangeText={setUserFilter}
              />

              {loadingUsers ? (
                <ActivityIndicator size="large" color="#2563eb" style={{ marginVertical: 20 }} />
              ) : (
                filteredUsers.map((u, index) => (
                  <View key={index} style={styles.userRow}>
                    <View style={styles.userInfo}>
                      <View style={styles.userNameRow}>
                        <Text style={styles.userName}>{u.name || 'No Name'}</Text>
                        {u.role === 'admin' && (
                          <View style={styles.adminBadge}>
                            <Text style={styles.adminBadgeText}>ADMIN</Text>
                          </View>
                        )}
                        {u.role === 'guest' && (
                          <View style={styles.guestBadge}>
                            <Text style={styles.guestBadgeText}>GUEST</Text>
                          </View>
                        )}
                      </View>
                      <Text style={styles.userEmail}>{u.email}</Text>
                      <View style={styles.userStatusRow}>
                        {u.has_paid ? (
                          <View style={styles.premiumBadge}>
                            <Ionicons name="star" size={12} color="#f59e0b" />
                            <Text style={styles.premiumBadgeText}>Premium</Text>
                          </View>
                        ) : (
                          <View style={styles.freeBadge}>
                            <Text style={styles.freeBadgeText}>Free</Text>
                          </View>
                        )}
                        {u.granted_by && (
                          <Text style={styles.grantedByText}>Granted by admin</Text>
                        )}
                      </View>
                    </View>
                    {u.role !== 'admin' && u.role !== 'guest' && (
                      <View style={styles.userActions}>
                        {u.has_paid ? (
                          <TouchableOpacity
                            style={styles.revokeButton}
                            onPress={() => handleRevokePremium(u.email)}
                          >
                            <Ionicons name="close-circle" size={16} color="#ef4444" />
                            <Text style={styles.revokeButtonText}>Revoke</Text>
                          </TouchableOpacity>
                        ) : (
                          <TouchableOpacity
                            style={styles.grantSmallButton}
                            onPress={() => handleGrantFromList(u.email)}
                          >
                            <Ionicons name="star" size={16} color="#f59e0b" />
                            <Text style={styles.grantSmallButtonText}>Grant</Text>
                          </TouchableOpacity>
                        )}
                      </View>
                    )}
                  </View>
                ))
              )}
            </View>
          </>
        ) : (
          <>
            {/* Quick Actions */}
            <View style={styles.section}>
              <View style={styles.sectionHeader}>
                <Ionicons name="flash" size={20} color="#2563eb" />
                <Text style={styles.sectionTitle}>Quick Actions</Text>
              </View>
              <TouchableOpacity
                style={styles.actionCard}
                onPress={() => router.push('/admin-questions')}
              >
                <Ionicons name="create" size={32} color="#2563eb" />
                <View style={styles.actionContent}>
                  <Text style={styles.actionTitle}>Manage Questions</Text>
                  <Text style={styles.actionDescription}>Edit, delete, or add questions</Text>
                </View>
                <Ionicons name="chevron-forward" size={24} color="#64748b" />
              </TouchableOpacity>
            </View>

            {/* User Stats Section */}
            <View style={styles.section}>
              <View style={styles.sectionHeader}>
                <Ionicons name="people" size={20} color="#2563eb" />
                <Text style={styles.sectionTitle}>User Statistics</Text>
              </View>
              <View style={styles.statsGrid}>
                <View style={[styles.statCard, styles.statCardBlue]}>
                  <Text style={styles.statNumber}>{analytics?.users.total_registered || 0}</Text>
                  <Text style={styles.statLabel}>Registered Users</Text>
                </View>
                <View style={[styles.statCard, styles.statCardGreen]}>
                  <Text style={styles.statNumber}>{analytics?.users.active_today || 0}</Text>
                  <Text style={styles.statLabel}>Active Today</Text>
                </View>
                <View style={[styles.statCard, styles.statCardYellow]}>
                  <Text style={styles.statNumber}>{analytics?.users.active_this_week || 0}</Text>
                  <Text style={styles.statLabel}>Active This Week</Text>
                </View>
                <View style={[styles.statCard, styles.statCardPurple]}>
                  <Text style={styles.statNumber}>{analytics?.users.total_guest_sessions || 0}</Text>
                  <Text style={styles.statLabel}>Guest Sessions</Text>
                </View>
              </View>
              <View style={styles.infoRow}>
                <View style={styles.infoItem}>
                  <Ionicons name="person-add" size={16} color="#10b981" />
                  <Text style={styles.infoText}>
                    {analytics?.users.new_registrations_week || 0} new this week
                  </Text>
                </View>
                <View style={styles.infoItem}>
                  <Ionicons name="calendar" size={16} color="#60a5fa" />
                  <Text style={styles.infoText}>
                    {analytics?.users.active_this_month || 0} active this month
                  </Text>
                </View>
              </View>
            </View>

            {/* Daily Active Users Chart */}
            <View style={styles.section}>
              <View style={styles.sectionHeader}>
                <Ionicons name="bar-chart" size={20} color="#10b981" />
                <Text style={styles.sectionTitle}>Daily Active Users (7 Days)</Text>
              </View>
              <View style={styles.chartContainer}>
                {analytics?.daily_active_users.map((day, index) => (
                  <View key={index} style={styles.chartBar}>
                    <Text style={styles.chartValue}>{day.active_users}</Text>
                    <View
                      style={[
                        styles.bar,
                        { height: Math.max((day.active_users / maxDailyUsers) * 100, 5) },
                      ]}
                    />
                    <Text style={styles.chartLabel}>{day.day}</Text>
                  </View>
                ))}
              </View>
            </View>

            {/* Content Stats Section */}
            <View style={styles.section}>
              <View style={styles.sectionHeader}>
                <Ionicons name="library" size={20} color="#f59e0b" />
                <Text style={styles.sectionTitle}>Content Statistics</Text>
              </View>
              <View style={styles.contentStats}>
                <View style={styles.contentStatItem}>
                  <View style={[styles.contentIcon, { backgroundColor: '#1e3a8a' }]}>
                    <Ionicons name="layers" size={24} color="#60a5fa" />
                  </View>
                  <View>
                    <Text style={styles.contentStatNumber}>{analytics?.content.total_flashcards || 0}</Text>
                    <Text style={styles.contentStatLabel}>Flashcards</Text>
                  </View>
                </View>
                <View style={styles.contentStatItem}>
                  <View style={[styles.contentIcon, { backgroundColor: '#7c2d12' }]}>
                    <Ionicons name="document-text" size={24} color="#f59e0b" />
                  </View>
                  <View>
                    <Text style={styles.contentStatNumber}>{analytics?.content.total_scenarios || 0}</Text>
                    <Text style={styles.contentStatLabel}>Scenarios</Text>
                  </View>
                </View>
                <View style={styles.contentStatItem}>
                  <View style={[styles.contentIcon, { backgroundColor: '#14532d' }]}>
                    <Ionicons name="checkbox" size={24} color="#10b981" />
                  </View>
                  <View>
                    <Text style={styles.contentStatNumber}>{analytics?.content.total_mcqs || 0}</Text>
                    <Text style={styles.contentStatLabel}>MCQs</Text>
                  </View>
                </View>
              </View>
              <View style={styles.totalContent}>
                <Text style={styles.totalContentText}>
                  Total Questions: {analytics?.content.total_questions || 0}
                </Text>
              </View>
            </View>

            {/* Activity Stats Section */}
            <View style={styles.section}>
              <View style={styles.sectionHeader}>
                <Ionicons name="pulse" size={20} color="#ec4899" />
                <Text style={styles.sectionTitle}>Activity Statistics</Text>
              </View>
              <View style={styles.activityStats}>
                <View style={styles.activityItem}>
                  <Text style={styles.activityNumber}>{analytics?.activity.total_scenario_responses || 0}</Text>
                  <Text style={styles.activityLabel}>Scenario Responses</Text>
                </View>
                <View style={styles.activityDivider} />
                <View style={styles.activityItem}>
                  <Text style={styles.activityNumber}>{analytics?.activity.total_quiz_attempts || 0}</Text>
                  <Text style={styles.activityLabel}>Quiz Attempts</Text>
                </View>
                <View style={styles.activityDivider} />
                <View style={styles.activityItem}>
                  <Text style={styles.activityNumber}>
                    {analytics?.activity.average_scenario_score
                      ? analytics.activity.average_scenario_score + '%'
                      : 'N/A'}
                  </Text>
                  <Text style={styles.activityLabel}>Avg Score</Text>
                </View>
              </View>
            </View>

            {/* Popular Categories */}
            {analytics?.popular_categories && analytics.popular_categories.length > 0 && (
              <View style={styles.section}>
                <View style={styles.sectionHeader}>
                  <Ionicons name="trending-up" size={20} color="#8b5cf6" />
                  <Text style={styles.sectionTitle}>Popular Categories</Text>
                </View>
                {analytics.popular_categories.map((cat, index) => (
                  <View key={index} style={styles.categoryItem}>
                    <View style={styles.categoryRank}>
                      <Text style={styles.categoryRankText}>#{index + 1}</Text>
                    </View>
                    <Text style={styles.categoryName}>{cat.category}</Text>
                    <Text style={styles.categoryAttempts}>{cat.attempts} attempts</Text>
                  </View>
                ))}
              </View>
            )}

            {/* Recent Activity */}
            {analytics?.recent_activity && analytics.recent_activity.length > 0 && (
              <View style={styles.section}>
                <View style={styles.sectionHeader}>
                  <Ionicons name="time" size={20} color="#06b6d4" />
                  <Text style={styles.sectionTitle}>Recent Activity</Text>
                </View>
                {analytics.recent_activity.slice(0, 5).map((activity, index) => (
                  <View key={index} style={styles.activityRow}>
                    <View style={styles.activityAvatar}>
                      <Ionicons name="person" size={16} color="#64748b" />
                    </View>
                    <View style={styles.activityInfo}>
                      <Text style={styles.activityUserName}>{activity.user_name}</Text>
                      <Text style={styles.activityTime}>
                        {new Date(activity.submitted_at).toLocaleDateString()}
                      </Text>
                    </View>
                    {activity.ai_grade !== null && (
                      <View
                        style={[
                          styles.activityGrade,
                          { backgroundColor: activity.ai_grade >= 70 ? '#064e3b' : '#7f1d1d' },
                        ]}
                      >
                        <Text style={styles.activityGradeText}>{activity.ai_grade}%</Text>
                      </View>
                    )}
                  </View>
                ))}
              </View>
            )}

            <View style={styles.footer}>
              <Text style={styles.footerText}>Last updated: {new Date().toLocaleString()}</Text>
            </View>
          </>
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
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    color: '#94a3b8',
    marginTop: 12,
    fontSize: 16,
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  errorText: {
    color: '#ef4444',
    fontSize: 18,
    marginTop: 16,
    marginBottom: 24,
  },
  retryButton: {
    backgroundColor: '#1e293b',
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 8,
  },
  retryButtonText: {
    color: '#fff',
    fontSize: 16,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#1e293b',
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
  tabBar: {
    flexDirection: 'row',
    paddingHorizontal: 16,
    paddingTop: 12,
    paddingBottom: 4,
    gap: 8,
  },
  tab: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 6,
    paddingVertical: 10,
    borderRadius: 10,
    backgroundColor: '#1e293b',
  },
  activeTab: {
    backgroundColor: '#2563eb',
  },
  tabText: {
    color: '#64748b',
    fontSize: 14,
    fontWeight: '600',
  },
  activeTabText: {
    color: '#fff',
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    padding: 16,
    paddingBottom: 32,
  },
  section: {
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 16,
    marginBottom: 16,
  },
  actionCard: {
    backgroundColor: '#0f172a',
    borderRadius: 12,
    padding: 16,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 16,
    borderWidth: 1,
    borderColor: '#2563eb',
  },
  actionContent: {
    flex: 1,
  },
  actionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#fff',
    marginBottom: 4,
  },
  actionDescription: {
    fontSize: 13,
    color: '#94a3b8',
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 16,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#fff',
    flex: 1,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
  statCard: {
    flex: 1,
    minWidth: '45%',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  statCardBlue: {
    backgroundColor: '#1e3a8a',
  },
  statCardGreen: {
    backgroundColor: '#064e3b',
  },
  statCardYellow: {
    backgroundColor: '#78350f',
  },
  statCardPurple: {
    backgroundColor: '#581c87',
  },
  statNumber: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#fff',
  },
  statLabel: {
    fontSize: 12,
    color: '#94a3b8',
    marginTop: 4,
    textAlign: 'center',
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 16,
    paddingTop: 16,
    borderTopWidth: 1,
    borderTopColor: '#334155',
  },
  infoItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  infoText: {
    color: '#94a3b8',
    fontSize: 13,
  },
  chartContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-end',
    height: 140,
    paddingTop: 20,
  },
  chartBar: {
    flex: 1,
    alignItems: 'center',
  },
  chartValue: {
    color: '#94a3b8',
    fontSize: 11,
    marginBottom: 4,
  },
  bar: {
    width: 24,
    backgroundColor: '#10b981',
    borderRadius: 4,
    minHeight: 5,
  },
  chartLabel: {
    color: '#64748b',
    fontSize: 11,
    marginTop: 8,
  },
  contentStats: {
    gap: 12,
  },
  contentStatItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  contentIcon: {
    width: 48,
    height: 48,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
  },
  contentStatNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  contentStatLabel: {
    fontSize: 13,
    color: '#94a3b8',
  },
  totalContent: {
    marginTop: 16,
    paddingTop: 16,
    borderTopWidth: 1,
    borderTopColor: '#334155',
    alignItems: 'center',
  },
  totalContentText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#10b981',
  },
  activityStats: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  activityItem: {
    flex: 1,
    alignItems: 'center',
  },
  activityNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  activityLabel: {
    fontSize: 11,
    color: '#94a3b8',
    marginTop: 4,
    textAlign: 'center',
  },
  activityDivider: {
    width: 1,
    height: 40,
    backgroundColor: '#334155',
  },
  categoryItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#334155',
  },
  categoryRank: {
    width: 28,
    height: 28,
    borderRadius: 14,
    backgroundColor: '#8b5cf6',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  categoryRankText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: 'bold',
  },
  categoryName: {
    flex: 1,
    color: '#fff',
    fontSize: 14,
  },
  categoryAttempts: {
    color: '#64748b',
    fontSize: 12,
  },
  activityRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#334155',
  },
  activityAvatar: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: '#334155',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  activityInfo: {
    flex: 1,
  },
  activityUserName: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '500',
  },
  activityTime: {
    color: '#64748b',
    fontSize: 12,
  },
  activityGrade: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 8,
  },
  activityGradeText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: 'bold',
  },
  footer: {
    alignItems: 'center',
    paddingVertical: 16,
  },
  footerText: {
    color: '#64748b',
    fontSize: 12,
  },
  // Premium grant styles
  grantDescription: {
    color: '#94a3b8',
    fontSize: 14,
    marginBottom: 12,
  },
  grantRow: {
    flexDirection: 'row',
    gap: 8,
  },
  grantInput: {
    flex: 1,
    backgroundColor: '#0f172a',
    borderRadius: 10,
    padding: 12,
    color: '#fff',
    fontSize: 15,
    borderWidth: 1,
    borderColor: '#334155',
  },
  grantButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    backgroundColor: '#f59e0b',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderRadius: 10,
  },
  grantButtonText: {
    color: '#fff',
    fontWeight: '700',
    fontSize: 14,
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  // Search input
  searchInput: {
    backgroundColor: '#0f172a',
    borderRadius: 10,
    padding: 12,
    color: '#fff',
    fontSize: 14,
    borderWidth: 1,
    borderColor: '#334155',
    marginBottom: 12,
  },
  refreshUsersBtn: {
    padding: 4,
  },
  // User row styles
  userRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#334155',
  },
  userInfo: {
    flex: 1,
  },
  userNameRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 2,
  },
  userName: {
    color: '#fff',
    fontSize: 15,
    fontWeight: '600',
  },
  userEmail: {
    color: '#94a3b8',
    fontSize: 13,
    marginBottom: 4,
  },
  userStatusRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  premiumBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    backgroundColor: '#78350f',
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 6,
  },
  premiumBadgeText: {
    color: '#fcd34d',
    fontSize: 11,
    fontWeight: '600',
  },
  freeBadge: {
    backgroundColor: '#334155',
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 6,
  },
  freeBadgeText: {
    color: '#94a3b8',
    fontSize: 11,
    fontWeight: '600',
  },
  adminBadge: {
    backgroundColor: '#7c3aed',
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 4,
  },
  adminBadgeText: {
    color: '#fff',
    fontSize: 10,
    fontWeight: '700',
  },
  guestBadge: {
    backgroundColor: '#78350f',
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 4,
  },
  guestBadgeText: {
    color: '#fcd34d',
    fontSize: 10,
    fontWeight: '700',
  },
  grantedByText: {
    color: '#64748b',
    fontSize: 11,
    fontStyle: 'italic',
  },
  userActions: {
    marginLeft: 8,
  },
  revokeButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    backgroundColor: '#7f1d1d',
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 8,
  },
  revokeButtonText: {
    color: '#fca5a5',
    fontSize: 12,
    fontWeight: '600',
  },
  grantSmallButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    backgroundColor: '#78350f',
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 8,
  },
  grantSmallButtonText: {
    color: '#fcd34d',
    fontSize: 12,
    fontWeight: '600',
  },
});
