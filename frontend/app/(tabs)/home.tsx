import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet, ActivityIndicator, RefreshControl, Dimensions } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useAuth } from '../../contexts/AuthContext';
import { useRouter } from 'expo-router';
import { statsService, categoryService } from '../../services/api';

const { width } = Dimensions.get('window');
const isWide = width > 700;

const testOptions = [
  { name: '25 Question Quiz', desc: 'Quick practice test', time: '~15 min', icon: 'flash' as const, color: '#3b82f6', route: '/quiz' },
  { name: '50 Question Test', desc: 'Standard practice exam', time: '~30 min', icon: 'document-text' as const, color: '#8b5cf6', route: '/mcq-test' },
  { name: 'Full Practice Exam', desc: '105 questions — Simulates actual test', time: '~90 min', icon: 'trophy' as const, color: '#f59e0b', route: '/practice-exam' },
];

const part2Sections = [
  { name: 'Written Scenarios', desc: 'Full 20-minute timed scenarios with AI grading', count: 20, icon: 'create' as const, color: '#3b82f6' },
  { name: 'Ranking Questions', desc: 'Rank actions in correct priority order', count: 20, icon: 'bar-chart' as const, color: '#06b6d4' },
  { name: 'Most Appropriate', desc: 'Select the BEST action for each scenario', count: 10, icon: 'checkmark-circle' as const, color: '#10b981' },
  { name: 'Least Appropriate', desc: 'Select the WORST action for each scenario', count: 10, icon: 'alert-circle' as const, color: '#ef4444' },
  { name: 'Legal Trap', desc: 'Tricky legal and constitutional questions', count: 30, icon: 'shield' as const, color: '#f97316' },
  { name: 'Digital Evidence', desc: 'Modern digital evidence handling', count: 10, icon: 'desktop' as const, color: '#14b8a6' },
  { name: 'Mini Scenarios', desc: 'Short written scenarios with AI grading', count: 10, icon: 'help-circle' as const, color: '#a855f7' },
];

const categoryIcons: Record<string, { icon: string; color: string }> = {
  'gold': { icon: 'star', color: '#f59e0b' },
  'ilcs': { icon: 'scale', color: '#8b5cf6' },
  'part2': { icon: 'create', color: '#3b82f6' },
  'ranking': { icon: 'bar-chart', color: '#06b6d4' },
  'most': { icon: 'checkmark-circle', color: '#10b981' },
  'least': { icon: 'alert-circle', color: '#ef4444' },
  'legal': { icon: 'shield', color: '#f97316' },
  'digital': { icon: 'desktop', color: '#14b8a6' },
  'mini': { icon: 'help-circle', color: '#a855f7' },
};

function StatCard({ icon, value, label, sublabel, color, progress }: {
  icon: string; value: string | number; label: string; sublabel?: string; color: string; progress?: number;
}) {
  return (
    <View style={[styles.statCard, { borderColor: color + '22' }]}>
      <View style={{ position: 'absolute', top: -20, right: -20, width: 80, height: 80, borderRadius: 40, backgroundColor: color + '08' }} />
      <View style={{ flexDirection: 'row', alignItems: 'center', gap: 10, marginBottom: 12 }}>
        <View style={{ backgroundColor: color + '18', borderRadius: 10, padding: 8 }}>
          <Ionicons name={icon as any} size={20} color={color} />
        </View>
        <Text style={{ color: '#94a3b8', fontSize: 13, fontWeight: '500' }}>{label}</Text>
      </View>
      <Text style={{ fontSize: 28, fontWeight: '700', color: '#f1f5f9', marginBottom: 2 }}>{value}</Text>
      {sublabel && <Text style={{ color: '#64748b', fontSize: 12 }}>{sublabel}</Text>}
      {progress !== undefined && (
        <View style={{ marginTop: 10, height: 4, borderRadius: 2, backgroundColor: '#1e293b' }}>
          <View style={{ height: '100%', borderRadius: 2, backgroundColor: color, width: `${Math.min(progress, 100)}%` }} />
        </View>
      )}
    </View>
  );
}

function RankBadge({ rank }: { rank: number }) {
  const medals: Record<number, string> = { 1: '\u{1F947}', 2: '\u{1F948}', 3: '\u{1F949}' };
  if (medals[rank]) return <Text style={{ fontSize: 18 }}>{medals[rank]}</Text>;
  return <Text style={{ color: '#64748b', fontWeight: '600', fontSize: 14, width: 24, textAlign: 'center' }}>{rank}</Text>;
}

export default function Home() {
  const { user, sessionToken, hasPaid } = useAuth();
  const router = useRouter();
  const [stats, setStats] = useState<any>(null);
  const [categories, setCategories] = useState<any[]>([]);
  const [leaderboard, setLeaderboard] = useState<any[]>([]);
  const [userRank, setUserRank] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const loadData = async () => {
    try {
      const [statsData, categoriesData, leaderboardData] = await Promise.all([
        statsService.getStats(sessionToken || undefined),
        categoryService.getCategories(),
        statsService.getLeaderboard(sessionToken || undefined).catch(() => ({ leaderboard: [], user_rank: null })),
      ]);
      setStats(statsData);
      setCategories(categoriesData);
      setLeaderboard(leaderboardData.leaderboard?.slice(0, 5) || []);
      setUserRank(leaderboardData.user_rank);
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
          <ActivityIndicator size="large" color="#3b82f6" />
        </View>
      </SafeAreaView>
    );
  }

  const flashcardsTotal = stats?.total_flashcards || 0;
  const flashcardsStudied = stats?.attempted_flashcards || 0;
  const scenariosTotal = stats?.total_scenarios || 0;
  const scenariosCompleted = stats?.attempted_scenarios || 0;
  const bookmarked = stats?.bookmarks || 0;
  const avgScore = stats?.average_score ? `${Math.round(stats.average_score)}%` : '\u2014';
  const totalResponses = stats?.total_responses || 0;

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        style={styles.scrollView}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor="#3b82f6" />}
      >
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.greeting}>Welcome back,</Text>
          <Text style={styles.name}>{user?.name || 'Officer'}</Text>
          <Text style={styles.subtitle}>Keep up the great work — you're making progress!</Text>
        </View>

        {/* Feedback Announcement */}
        <View style={styles.announcementBanner}>
          <View style={styles.announcementIcon}>
            <Ionicons name="megaphone" size={20} color="#f59e0b" />
          </View>
          <View style={{ flex: 1 }}>
            <Text style={styles.announcementTitle}>Help Us Improve AI Grading</Text>
            <Text style={styles.announcementText}>
              After completing a scenario, you can report incorrect grades or suggest corrections. Your feedback helps improve grading accuracy for everyone.
            </Text>
            <TouchableOpacity onPress={() => router.push('/updates')} style={styles.announcementLink}>
              <Text style={styles.announcementLinkText}>View Corrections & Updates</Text>
              <Ionicons name="arrow-forward" size={14} color="#f59e0b" />
            </TouchableOpacity>
          </View>
        </View>

        {/* Stats Row */}
        <View style={styles.statsGrid}>
          <StatCard icon="book" value={flashcardsTotal} label="Flashcards" sublabel={`${flashcardsStudied} studied`} color="#3b82f6" progress={flashcardsTotal > 0 ? (flashcardsStudied / flashcardsTotal) * 100 : 0} />
          <StatCard icon="document-text" value={scenariosTotal} label="Scenarios" sublabel={`${scenariosCompleted} completed`} color="#10b981" progress={scenariosTotal > 0 ? (scenariosCompleted / scenariosTotal) * 100 : 0} />
          <StatCard icon="bookmark" value={bookmarked} label="Bookmarked" sublabel="Save cards to review" color="#f59e0b" />
          <StatCard icon="trending-up" value={avgScore} label="Avg Score" sublabel={`${totalResponses} responses`} color="#8b5cf6" />
        </View>

        {/* Quick Start + Leaderboard */}
        <View style={isWide ? styles.rowLayout : undefined}>
          {/* Practice Tests */}
          <View style={[styles.section, isWide && { flex: 1 }]}>
            <View style={styles.sectionHeader}>
              <Ionicons name="flash" size={18} color="#f59e0b" />
              <Text style={styles.sectionTitle}>Quick Start — Practice Tests</Text>
            </View>
            {testOptions.map((test, i) => (
              <TouchableOpacity key={i} style={styles.testCard} onPress={() => router.push(test.route as any)} activeOpacity={0.7}>
                <View style={[styles.testIcon, { backgroundColor: test.color + '18' }]}>
                  <Ionicons name={test.icon as any} size={22} color={test.color} />
                </View>
                <View style={{ flex: 1 }}>
                  <Text style={styles.testName}>{test.name}</Text>
                  <Text style={styles.testDesc}>{test.desc}</Text>
                </View>
                <View style={{ flexDirection: 'row', alignItems: 'center', gap: 6 }}>
                  <Ionicons name="time" size={14} color="#475569" />
                  <Text style={{ color: '#475569', fontSize: 13 }}>{test.time}</Text>
                </View>
                <Ionicons name="chevron-forward" size={18} color="#475569" />
              </TouchableOpacity>
            ))}
          </View>

          {/* Leaderboard */}
          <View style={[styles.leaderboardCard, isWide && { width: 340 }]}>
            <View style={styles.sectionHeader}>
              <Ionicons name="trophy" size={18} color="#f59e0b" />
              <Text style={styles.sectionTitle}>Top Performers</Text>
            </View>
            {leaderboard.length > 0 ? leaderboard.map((entry: any, i: number) => (
              <View key={i} style={[styles.leaderboardRow, i === 0 && styles.leaderboardFirst]}>
                <RankBadge rank={entry.rank || i + 1} />
                <Text style={[styles.leaderboardName, i < 3 && { fontWeight: '600', color: '#f1f5f9' }]} numberOfLines={1}>
                  {entry.name}
                </Text>
                <Text style={styles.leaderboardAvg}>{Math.round(entry.average_score || entry.avg || 0)}%</Text>
                <Text style={styles.leaderboardBest}>{Math.round(entry.best_score || entry.best || 0)}%</Text>
              </View>
            )) : (
              <Text style={{ color: '#64748b', fontSize: 13, textAlign: 'center', paddingVertical: 20 }}>No scores yet — be the first!</Text>
            )}
            {userRank && (
              <View style={styles.userRankBadge}>
                <Ionicons name="people" size={14} color="#60a5fa" />
                <Text style={{ color: '#94a3b8', fontSize: 13 }}>Your rank:</Text>
                <Text style={{ fontWeight: '600', color: '#60a5fa', fontSize: 13 }}>#{userRank}</Text>
              </View>
            )}
            <TouchableOpacity style={styles.viewAllBtn} onPress={() => router.push('/leaderboard')} activeOpacity={0.7}>
              <Text style={{ color: '#60a5fa', fontSize: 13, fontWeight: '600' }}>View Full Rankings</Text>
              <Ionicons name="chevron-forward" size={14} color="#60a5fa" />
            </TouchableOpacity>
          </View>
        </View>

        {/* Premium Upgrade Banner */}
        {!hasPaid && user?.role !== 'admin' && (
          <TouchableOpacity style={styles.premiumBanner} onPress={() => router.push('/upgrade')} activeOpacity={0.8}>
            <View style={{ position: 'absolute', top: 0, left: 0, right: 0, height: 3, backgroundColor: '#8b5cf6', borderTopLeftRadius: 16, borderTopRightRadius: 16 }} />
            <View style={{ flexDirection: 'row', alignItems: 'center', gap: 10, marginBottom: 6 }}>
              <Ionicons name="create" size={20} color="#8b5cf6" />
              <Text style={{ fontSize: 18, fontWeight: '700', color: '#f1f5f9' }}>Part 2 — Detective Exam</Text>
              <View style={styles.premiumTag}>
                <Text style={styles.premiumTagText}>PREMIUM</Text>
              </View>
            </View>
            <Text style={{ color: '#64748b', fontSize: 13, marginBottom: 14 }}>I/O Solutions mixed-method exam simulation with AI grading</Text>
            <View style={styles.unlockBtn}>
              <Ionicons name="lock-open" size={16} color="#fff" />
              <Text style={{ color: '#fff', fontSize: 15, fontWeight: '700' }}>Unlock Premium — $25.00</Text>
            </View>
          </TouchableOpacity>
        )}

        {/* Part 2 Exam Section (for paid users) */}
        {(hasPaid || user?.role === 'admin') && (
          <View style={styles.part2Section}>
            <View style={{ position: 'absolute', top: 0, left: 0, right: 0, height: 3, backgroundColor: '#8b5cf6', borderTopLeftRadius: 16, borderTopRightRadius: 16 }} />
            <View style={{ flexDirection: 'row', alignItems: 'center', gap: 10, marginBottom: 6 }}>
              <Ionicons name="create" size={20} color="#8b5cf6" />
              <Text style={{ fontSize: 18, fontWeight: '700', color: '#f1f5f9' }}>Part 2 — Detective Exam</Text>
              <View style={styles.premiumTag}>
                <Text style={styles.premiumTagText}>PREMIUM</Text>
              </View>
            </View>
            <Text style={{ color: '#64748b', fontSize: 13, marginBottom: 16 }}>I/O Solutions mixed-method exam simulation with AI grading</Text>

            {/* Grading Info */}
            <View style={{ flexDirection: isWide ? 'row' : 'column', gap: 10, marginBottom: 16 }}>
              <View style={styles.infoBadge}>
                <Ionicons name="ribbon" size={18} color="#8b5cf6" />
                <View>
                  <Text style={{ fontSize: 13, fontWeight: '600', color: '#e2e8f0' }}>How You're Graded</Text>
                  <Text style={{ fontSize: 11, color: '#64748b' }}>I/O Solutions methodology</Text>
                </View>
              </View>
              <View style={[styles.infoBadge, { backgroundColor: 'rgba(59,130,246,0.08)', borderColor: 'rgba(59,130,246,0.2)' }]}>
                <Ionicons name="checkmark-circle" size={18} color="#3b82f6" />
                <View>
                  <Text style={{ fontSize: 13, fontWeight: '600', color: '#e2e8f0' }}>R.E.A.C.T.I.O.N. Framework</Text>
                  <Text style={{ fontSize: 11, color: '#64748b' }}>Structured response guide</Text>
                </View>
              </View>
            </View>

            {/* Part 2 Scenario Types */}
            <View style={isWide ? styles.part2Grid : undefined}>
              {part2Sections.map((sec, i) => (
                <TouchableOpacity key={i} style={[styles.part2Card, { borderColor: sec.color + '15' }]} activeOpacity={0.7} onPress={() => router.push('/scenarios')}>
                  <View style={[styles.part2Icon, { backgroundColor: sec.color + '15' }]}>
                    <Ionicons name={sec.icon as any} size={18} color={sec.color} />
                  </View>
                  <View style={{ flex: 1, minWidth: 0 }}>
                    <Text style={{ fontSize: 14, fontWeight: '600', color: '#f1f5f9' }}>{sec.name}</Text>
                    <Text style={{ fontSize: 12, color: '#64748b' }} numberOfLines={1}>{sec.desc}</Text>
                  </View>
                  <View style={[styles.part2Count, { backgroundColor: sec.color + '15' }]}>
                    <Text style={{ color: sec.color, fontSize: 13, fontWeight: '700' }}>{sec.count}</Text>
                  </View>
                  <Ionicons name="chevron-forward" size={16} color="#475569" />
                </TouchableOpacity>
              ))}
            </View>
          </View>
        )}

        {/* Study Categories */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Ionicons name="layers" size={18} color="#8b5cf6" />
            <Text style={styles.sectionTitle}>Study Categories</Text>
          </View>
          <View style={isWide ? styles.categoriesGrid : undefined}>
            {categories.map((cat: any) => {
              const catStyle = categoryIcons[cat.category_id] || { icon: 'folder', color: '#3b82f6' };
              return (
                <View key={cat.category_id} style={[styles.categoryCard, { borderColor: catStyle.color + '15' }]}>
                  <View style={{ position: 'absolute', top: -30, right: -30, width: 80, height: 80, borderRadius: 40, backgroundColor: catStyle.color + '06' }} />
                  <View style={{ flexDirection: 'row', alignItems: 'center', gap: 10, marginBottom: 8 }}>
                    <View style={{ backgroundColor: catStyle.color + '15', borderRadius: 8, padding: 6 }}>
                      <Ionicons name={catStyle.icon as any} size={18} color={catStyle.color} />
                    </View>
                    <Text style={{ fontSize: 14, fontWeight: '600', color: '#f1f5f9' }}>{cat.name}</Text>
                  </View>
                  <Text style={{ color: '#64748b', fontSize: 12, lineHeight: 18, marginBottom: 10 }}>{cat.description}</Text>
                  <View style={{ flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' }}>
                    <Text style={{ fontSize: 12, color: '#475569' }}>{cat.question_count || 0} questions</Text>
                    <Ionicons name="chevron-forward" size={16} color={catStyle.color} style={{ opacity: 0.6 }} />
                  </View>
                </View>
              );
            })}
          </View>
        </View>

        {/* Admin Button */}
        {user?.role === 'admin' && (
          <View style={styles.section}>
            <TouchableOpacity style={styles.adminButton} onPress={() => router.push('/admin')}>
              <Ionicons name="settings" size={20} color="#fff" />
              <Text style={styles.adminButtonText}>Admin Panel</Text>
            </TouchableOpacity>
          </View>
        )}

        <View style={{ height: 40 }} />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0b1120',
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
    paddingBottom: 8,
  },
  greeting: {
    fontSize: 14,
    color: '#64748b',
  },
  name: {
    fontSize: 24,
    fontWeight: '700',
    color: '#f1f5f9',
    marginTop: 2,
  },
  subtitle: {
    fontSize: 13,
    color: '#64748b',
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
    minWidth: '45%' as any,
    backgroundColor: '#0f172a',
    borderRadius: 16,
    padding: 18,
    borderWidth: 1,
    position: 'relative',
    overflow: 'hidden',
  },
  rowLayout: {
    flexDirection: 'row',
    gap: 16,
    paddingHorizontal: 16,
  },
  section: {
    padding: 16,
    gap: 10,
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 4,
  },
  sectionTitle: {
    fontSize: 17,
    fontWeight: '700',
    color: '#f1f5f9',
  },
  testCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#0f172a',
    borderRadius: 14,
    padding: 16,
    gap: 14,
    borderWidth: 1,
    borderColor: '#1e293b',
  },
  testIcon: {
    borderRadius: 12,
    padding: 10,
  },
  testName: {
    fontSize: 15,
    fontWeight: '600',
    color: '#f1f5f9',
  },
  testDesc: {
    fontSize: 13,
    color: '#64748b',
    marginTop: 2,
  },
  leaderboardCard: {
    backgroundColor: '#0f172a',
    borderRadius: 16,
    padding: 20,
    margin: 16,
    marginTop: 0,
    borderWidth: 1,
    borderColor: '#1e293b',
    gap: 6,
  },
  leaderboardRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    paddingVertical: 8,
    paddingHorizontal: 10,
    borderRadius: 10,
  },
  leaderboardFirst: {
    backgroundColor: 'rgba(245,158,11,0.06)',
    borderWidth: 1,
    borderColor: 'rgba(245,158,11,0.15)',
  },
  leaderboardName: {
    flex: 1,
    fontSize: 14,
    color: '#94a3b8',
  },
  leaderboardAvg: {
    fontSize: 13,
    fontWeight: '600',
    color: '#10b981',
    minWidth: 45,
    textAlign: 'right',
  },
  leaderboardBest: {
    fontSize: 12,
    color: '#64748b',
    minWidth: 35,
    textAlign: 'right',
  },
  userRankBadge: {
    marginTop: 10,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    backgroundColor: 'rgba(59,130,246,0.08)',
    borderWidth: 1,
    borderColor: 'rgba(59,130,246,0.15)',
    borderRadius: 10,
    padding: 10,
  },
  viewAllBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 4,
    marginTop: 8,
    paddingVertical: 8,
  },
  premiumBanner: {
    margin: 16,
    backgroundColor: '#0f172a',
    borderRadius: 16,
    padding: 22,
    borderWidth: 1,
    borderColor: 'rgba(139,92,246,0.2)',
    position: 'relative',
    overflow: 'hidden',
  },
  premiumTag: {
    backgroundColor: '#f59e0b',
    paddingHorizontal: 10,
    paddingVertical: 3,
    borderRadius: 20,
  },
  premiumTagText: {
    color: '#fff',
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 1,
  },
  unlockBtn: {
    backgroundColor: '#10b981',
    borderRadius: 10,
    paddingVertical: 12,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
  },
  part2Section: {
    margin: 16,
    backgroundColor: '#0f172a',
    borderRadius: 16,
    padding: 22,
    borderWidth: 1,
    borderColor: 'rgba(139,92,246,0.2)',
    position: 'relative',
    overflow: 'hidden',
  },
  infoBadge: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    backgroundColor: 'rgba(139,92,246,0.08)',
    borderWidth: 1,
    borderColor: 'rgba(139,92,246,0.2)',
    borderRadius: 10,
    padding: 12,
  },
  part2Grid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 10,
  },
  part2Card: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    backgroundColor: 'rgba(15,23,42,0.6)',
    borderRadius: 12,
    padding: 14,
    borderWidth: 1,
    minWidth: isWide ? '48%' as any : undefined,
    flex: isWide ? 1 : undefined,
    marginBottom: isWide ? 0 : 6,
  },
  part2Icon: {
    borderRadius: 10,
    padding: 8,
  },
  part2Count: {
    borderRadius: 20,
    minWidth: 36,
    height: 36,
    alignItems: 'center',
    justifyContent: 'center',
  },
  categoriesGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
  categoryCard: {
    backgroundColor: '#0f172a',
    borderRadius: 14,
    padding: 18,
    borderWidth: 1,
    position: 'relative',
    overflow: 'hidden',
    minWidth: isWide ? '30%' as any : undefined,
    flex: isWide ? 1 : undefined,
    marginBottom: isWide ? 0 : 8,
  },
  announcementBanner: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 12,
    marginHorizontal: 16,
    marginTop: 4,
    marginBottom: 4,
    backgroundColor: 'rgba(245,158,11,0.08)',
    borderWidth: 1,
    borderColor: 'rgba(245,158,11,0.2)',
    borderRadius: 14,
    padding: 16,
  },
  announcementIcon: {
    backgroundColor: 'rgba(245,158,11,0.15)',
    borderRadius: 10,
    padding: 8,
    marginTop: 2,
  },
  announcementTitle: {
    fontSize: 15,
    fontWeight: '700',
    color: '#fbbf24',
    marginBottom: 4,
  },
  announcementText: {
    fontSize: 13,
    color: '#94a3b8',
    lineHeight: 19,
  },
  announcementLink: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    marginTop: 8,
  },
  announcementLinkText: {
    fontSize: 13,
    color: '#f59e0b',
    fontWeight: '600',
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
