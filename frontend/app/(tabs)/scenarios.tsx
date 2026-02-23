import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet, ActivityIndicator, Platform } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useAuth } from '../../contexts/AuthContext';
import { useRouter } from 'expo-router';
import { questionService } from '../../services/api';

export default function Scenarios() {
  const { sessionToken, hasPaid, isGuest, user } = useAuth();
  const router = useRouter();
  const [scenarios, setScenarios] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showGradingInfo, setShowGradingInfo] = useState(false);

  useEffect(() => {
    loadScenarios();
  }, [sessionToken]);

  const loadScenarios = async () => {
    try {
      setLoading(true);
      const data = await questionService.getQuestions(
        'scenario',
        'cat_detective_part2',
        sessionToken || undefined
      );
      setScenarios(data || []);
    } catch (error) {
      console.error('Failed to load scenarios:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleStartScenario = (scenarioId: string) => {
    router.push({ pathname: '/practice-scenario', params: { scenarioId } });
  };

  const handleUpgrade = () => {
    router.push('/upgrade');
  };

  const isAdmin = user?.role === 'admin';
  const canAccess = hasPaid || isAdmin;

  if (loading) {
    return (
      <SafeAreaView style={st.container}>
        <View style={st.loadingContainer}>
          <ActivityIndicator size="large" color="#10b981" />
          <Text style={st.loadingText}>Loading scenarios...</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={st.container}>
      <ScrollView style={st.scrollView} contentContainerStyle={st.scrollContent} showsVerticalScrollIndicator={false}>

        {/* Premium Header */}
        <View style={st.premiumHeader}>
          <View style={st.premiumBadge}>
            <Ionicons name="star" size={14} color="#fff" />
            <Text style={st.premiumBadgeText}>PREMIUM</Text>
          </View>
          <Text style={st.headerTitle}>Detective Part 2 Scenarios</Text>
          <Text style={st.headerSubtitle}>
            Timed scenarios with AI grading{'\n'}Based on I/O Solutions methodology
          </Text>
        </View>

        {/* Info Card */}
        <View style={st.infoCard}>
          <View style={st.infoRow}>
            <View style={st.infoItem}>
              <Ionicons name="time" size={20} color="#f59e0b" />
              <Text style={st.infoLabel}>15-20 min</Text>
              <Text style={st.infoDesc}>Per scenario</Text>
            </View>
            <View style={st.infoDivider} />
            <View style={st.infoItem}>
              <Ionicons name="document-text" size={20} color="#3b82f6" />
              <Text style={st.infoLabel}>{scenarios.length}</Text>
              <Text style={st.infoDesc}>Scenarios</Text>
            </View>
            <View style={st.infoDivider} />
            <View style={st.infoItem}>
              <Ionicons name="sparkles" size={20} color="#10b981" />
              <Text style={st.infoLabel}>AI</Text>
              <Text style={st.infoDesc}>Graded</Text>
            </View>
            <View style={st.infoDivider} />
            <View style={st.infoItem}>
              <Ionicons name="volume-high" size={20} color="#8b5cf6" />
              <Text style={st.infoLabel}>Audio</Text>
              <Text style={st.infoDesc}>Read aloud</Text>
            </View>
          </View>
        </View>

        {/* I/O Solutions Grading Method Explanation */}
        <TouchableOpacity
          style={st.gradingCard}
          onPress={() => setShowGradingInfo(!showGradingInfo)}
          activeOpacity={0.8}
        >
          <View style={st.gradingHeader}>
            <View style={st.gradingIconWrap}>
              <Ionicons name="school" size={20} color="#f59e0b" />
            </View>
            <View style={{ flex: 1 }}>
              <Text style={st.gradingTitle}>How You're Graded</Text>
              <Text style={st.gradingSubtitle}>I/O Solutions Scoring Method</Text>
            </View>
            <Ionicons name={showGradingInfo ? 'chevron-up' : 'chevron-down'} size={20} color="#64748b" />
          </View>

          {showGradingInfo && (
            <View style={st.gradingBody}>
              <Text style={st.gradingText}>
                These scenarios simulate the CPD Detective Part 2 written exam format used by I/O Solutions. Each scenario is graded on the following criteria:
              </Text>

              <View style={st.gradingItem}>
                <View style={[st.gradingDot, { backgroundColor: '#ef4444' }]} />
                <View style={{ flex: 1 }}>
                  <Text style={st.gradingItemTitle}>Mandatory Actions</Text>
                  <Text style={st.gradingItemDesc}>
                    Critical steps that MUST be in your response — securing the scene, notifying OEMC, requesting evidence technicians, etc. Missing these will significantly impact your score.
                  </Text>
                </View>
              </View>

              <View style={st.gradingItem}>
                <View style={[st.gradingDot, { backgroundColor: '#3b82f6' }]} />
                <View style={{ flex: 1 }}>
                  <Text style={st.gradingItemTitle}>General Order & ILCS Citations</Text>
                  <Text style={st.gradingItemDesc}>
                    Reference specific CPD General Orders (G04-02, G06-01, S04-29, etc.) and relevant Illinois Compiled Statutes. Proper citations show you know the legal framework.
                  </Text>
                </View>
              </View>

              <View style={st.gradingItem}>
                <View style={[st.gradingDot, { backgroundColor: '#10b981' }]} />
                <View style={{ flex: 1 }}>
                  <Text style={st.gradingItemTitle}>Investigative Thoroughness</Text>
                  <Text style={st.gradingItemDesc}>
                    Comprehensive approach — witness canvass, evidence preservation, POD/video review, case documentation, and proper chain of custody.
                  </Text>
                </View>
              </View>

              <View style={st.gradingItem}>
                <View style={[st.gradingDot, { backgroundColor: '#f59e0b' }]} />
                <View style={{ flex: 1 }}>
                  <Text style={st.gradingItemTitle}>Professional Communication</Text>
                  <Text style={st.gradingItemDesc}>
                    Clear, organized writing with logical progression. Use professional language and demonstrate command of CPD procedures.
                  </Text>
                </View>
              </View>

              <View style={st.gradingItem}>
                <View style={[st.gradingDot, { backgroundColor: '#8b5cf6' }]} />
                <View style={{ flex: 1 }}>
                  <Text style={st.gradingItemTitle}>Curveball Response</Text>
                  <Text style={st.gradingItemDesc}>
                    Mid-scenario complications test your ability to adapt. You'll receive a "wrench" twist that changes the situation and must adjust your approach accordingly.
                  </Text>
                </View>
              </View>

              <View style={st.timerNote}>
                <Ionicons name="time" size={16} color="#f59e0b" />
                <Text style={st.timerNoteText}>
                  Standard scenarios: 15 minutes  •  Complex scenarios: 20 minutes
                </Text>
              </View>
            </View>
          )}
        </TouchableOpacity>

        {/* Locked content for non-paid users */}
        {!canAccess && (
          <View style={st.lockedOverlay}>
            <Ionicons name="lock-closed" size={48} color="#f59e0b" />
            <Text style={st.lockedTitle}>Premium Content</Text>
            <Text style={st.lockedDesc}>
              Unlock all {scenarios.length} detective scenarios with timed practice, curveball complications, and AI-powered grading using the I/O Solutions scoring matrix.
            </Text>
            <View style={st.lockedFeatures}>
              {[
                { icon: 'checkmark-circle', text: '15-20 minute timed written responses' },
                { icon: 'checkmark-circle', text: 'Scenarios read aloud to you' },
                { icon: 'checkmark-circle', text: 'Mid-scenario curveball twists' },
                { icon: 'checkmark-circle', text: 'AI grading on mandatory actions & GO citations' },
                { icon: 'checkmark-circle', text: 'Detailed feedback & improvement tips' },
              ].map((f, i) => (
                <View key={i} style={st.lockedFeatureRow}>
                  <Ionicons name={f.icon as any} size={18} color="#10b981" />
                  <Text style={st.lockedFeatureText}>{f.text}</Text>
                </View>
              ))}
            </View>
            <TouchableOpacity style={st.unlockButton} onPress={handleUpgrade}>
              <Ionicons name="lock-open" size={20} color="#fff" />
              <Text style={st.unlockButtonText}>Unlock Premium — $25.00</Text>
            </TouchableOpacity>
            <Text style={st.unlockSubtext}>One-time payment • Lifetime access</Text>
          </View>
        )}

        {/* Scenario List - shown to paid users */}
        {canAccess && (
          <>
            <Text style={st.sectionTitle}>All Scenarios</Text>
            {scenarios.map((scenario, index) => (
              <TouchableOpacity
                key={scenario.question_id || index}
                style={st.scenarioCard}
                onPress={() => handleStartScenario(scenario.question_id)}
                activeOpacity={0.7}
              >
                <View style={st.scenarioCardHeader}>
                  <View style={st.scenarioNumber}>
                    <Text style={st.scenarioNumberText}>{index + 1}</Text>
                  </View>
                  <View style={st.scenarioCardContent}>
                    <Text style={st.scenarioTitle}>{scenario.title}</Text>
                    <Text style={st.scenarioDesc} numberOfLines={2}>
                      {scenario.description || scenario.content || ''}
                    </Text>
                    <View style={st.scenarioMeta}>
                      <View style={st.metaTag}>
                        <Ionicons name="time-outline" size={12} color="#94a3b8" />
                        <Text style={st.metaText}>{scenario.is_complex ? '20 min' : '15 min'}</Text>
                      </View>
                      {scenario.difficulty && (
                        <View style={[st.difficultyBadge, scenario.difficulty === 'Hard' ? st.diffHard : st.diffMedium]}>
                          <Text style={st.difficultyText}>{scenario.difficulty}</Text>
                        </View>
                      )}
                      {scenario.is_complex && (
                        <View style={[st.difficultyBadge, { backgroundColor: '#4c1d95' }]}>
                          <Text style={st.difficultyText}>Complex</Text>
                        </View>
                      )}
                      <View style={st.metaTag}>
                        <Ionicons name="volume-high-outline" size={12} color="#8b5cf6" />
                        <Text style={[st.metaText, { color: '#8b5cf6' }]}>Audio</Text>
                      </View>
                      {(scenario.is_complex || scenario.has_wrench) && (
                        <View style={st.metaTag}>
                          <Ionicons name="flash" size={12} color="#f59e0b" />
                          <Text style={[st.metaText, { color: '#f59e0b' }]}>Curveball</Text>
                        </View>
                      )}
                    </View>
                  </View>
                  <Ionicons name="chevron-forward" size={20} color="#64748b" />
                </View>
              </TouchableOpacity>
            ))}
          </>
        )}

        {/* Preview for non-paid - show scenario titles but locked */}
        {!canAccess && (
          <>
            <Text style={st.sectionTitle}>Scenario Preview</Text>
            {scenarios.map((scenario, index) => (
              <TouchableOpacity
                key={scenario.question_id || index}
                style={st.lockedCard}
                onPress={handleUpgrade}
                activeOpacity={0.7}
              >
                <View style={st.scenarioCardHeader}>
                  <View style={[st.scenarioNumber, st.lockedNumber]}>
                    <Ionicons name="lock-closed" size={14} color="#64748b" />
                  </View>
                  <View style={st.scenarioCardContent}>
                    <Text style={st.lockedScenarioTitle}>{scenario.title}</Text>
                    <Text style={st.lockedScenarioDesc} numberOfLines={1}>
                      {scenario.is_complex ? '20 min • Complex' : '15 min'} • Tap to unlock
                    </Text>
                  </View>
                </View>
              </TouchableOpacity>
            ))}
            <TouchableOpacity style={[st.unlockButton, { marginTop: 16 }]} onPress={handleUpgrade}>
              <Ionicons name="lock-open" size={20} color="#fff" />
              <Text style={st.unlockButtonText}>Unlock All Scenarios</Text>
            </TouchableOpacity>
          </>
        )}

        <View style={{ height: 40 }} />
      </ScrollView>
    </SafeAreaView>
  );
}

const st = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0c0c0c' },
  scrollView: { flex: 1 },
  scrollContent: { padding: 20, paddingBottom: 40 },
  loadingContainer: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  loadingText: { color: '#94a3b8', marginTop: 12, fontSize: 15 },

  // Premium Header
  premiumHeader: { alignItems: 'center', marginBottom: 20, paddingTop: 8 },
  premiumBadge: { flexDirection: 'row', alignItems: 'center', gap: 5, backgroundColor: '#f59e0b', paddingHorizontal: 14, paddingVertical: 6, borderRadius: 20, marginBottom: 12 },
  premiumBadgeText: { color: '#fff', fontSize: 12, fontWeight: '700', letterSpacing: 1 },
  headerTitle: { fontSize: 24, fontWeight: 'bold', color: '#fff', textAlign: 'center', marginBottom: 6 },
  headerSubtitle: { fontSize: 15, color: '#94a3b8', textAlign: 'center', lineHeight: 22 },

  // Info Card
  infoCard: { backgroundColor: '#1e293b', borderRadius: 16, padding: 16, marginBottom: 16 },
  infoRow: { flexDirection: 'row', justifyContent: 'space-around', alignItems: 'center' },
  infoItem: { alignItems: 'center', flex: 1 },
  infoDivider: { width: 1, height: 40, backgroundColor: '#334155' },
  infoLabel: { color: '#fff', fontSize: 16, fontWeight: '700', marginTop: 6 },
  infoDesc: { color: '#64748b', fontSize: 12, marginTop: 2 },

  // Grading Info Card
  gradingCard: { backgroundColor: '#1e293b', borderRadius: 16, padding: 18, marginBottom: 20, borderWidth: 1, borderColor: '#334155' },
  gradingHeader: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  gradingIconWrap: { width: 40, height: 40, borderRadius: 12, backgroundColor: 'rgba(245,158,11,0.15)', alignItems: 'center', justifyContent: 'center' },
  gradingTitle: { fontSize: 16, fontWeight: '700', color: '#fff' },
  gradingSubtitle: { fontSize: 13, color: '#f59e0b', fontWeight: '500', marginTop: 2 },
  gradingBody: { marginTop: 16, borderTopWidth: 1, borderTopColor: '#334155', paddingTop: 16 },
  gradingText: { fontSize: 14, color: '#cbd5e1', lineHeight: 22, marginBottom: 16 },
  gradingItem: { flexDirection: 'row', gap: 12, marginBottom: 14 },
  gradingDot: { width: 8, height: 8, borderRadius: 4, marginTop: 6 },
  gradingItemTitle: { fontSize: 14, fontWeight: '700', color: '#fff', marginBottom: 4 },
  gradingItemDesc: { fontSize: 13, color: '#94a3b8', lineHeight: 20 },
  timerNote: { flexDirection: 'row', alignItems: 'center', gap: 8, backgroundColor: 'rgba(245,158,11,0.1)', borderRadius: 10, padding: 12, marginTop: 4 },
  timerNoteText: { fontSize: 13, color: '#f59e0b', fontWeight: '600' },

  // Locked Overlay
  lockedOverlay: { backgroundColor: '#1e293b', borderRadius: 16, padding: 24, marginBottom: 24, alignItems: 'center', borderWidth: 1, borderColor: 'rgba(245, 158, 11, 0.2)' },
  lockedTitle: { fontSize: 22, fontWeight: 'bold', color: '#fff', marginTop: 12, marginBottom: 8 },
  lockedDesc: { fontSize: 14, color: '#94a3b8', textAlign: 'center', lineHeight: 22, marginBottom: 16 },
  lockedFeatures: { width: '100%', marginBottom: 20 },
  lockedFeatureRow: { flexDirection: 'row', alignItems: 'center', gap: 10, marginBottom: 10 },
  lockedFeatureText: { color: '#e2e8f0', fontSize: 14, fontWeight: '500' },

  // Unlock Button
  unlockButton: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8, backgroundColor: '#10b981', paddingVertical: 16, paddingHorizontal: 24, borderRadius: 12, width: '100%' },
  unlockButtonText: { color: '#fff', fontSize: 17, fontWeight: '700' },
  unlockSubtext: { color: '#64748b', fontSize: 13, marginTop: 8 },

  // Section Title
  sectionTitle: { fontSize: 18, fontWeight: 'bold', color: '#fff', marginBottom: 14 },

  // Scenario Cards (unlocked)
  scenarioCard: { backgroundColor: '#1e293b', borderRadius: 14, padding: 16, marginBottom: 12, borderWidth: 1, borderColor: '#334155' },
  scenarioCardHeader: { flexDirection: 'row', alignItems: 'center' },
  scenarioNumber: { width: 36, height: 36, borderRadius: 10, backgroundColor: '#10b981', alignItems: 'center', justifyContent: 'center', marginRight: 14 },
  scenarioNumberText: { color: '#fff', fontSize: 15, fontWeight: '700' },
  scenarioCardContent: { flex: 1 },
  scenarioTitle: { fontSize: 15, fontWeight: '600', color: '#fff', marginBottom: 4 },
  scenarioDesc: { fontSize: 13, color: '#94a3b8', lineHeight: 18, marginBottom: 8 },
  scenarioMeta: { flexDirection: 'row', gap: 8, flexWrap: 'wrap' },
  metaTag: { flexDirection: 'row', alignItems: 'center', gap: 4 },
  metaText: { fontSize: 11, color: '#94a3b8' },
  difficultyBadge: { paddingHorizontal: 8, paddingVertical: 2, borderRadius: 6 },
  diffHard: { backgroundColor: '#7f1d1d' },
  diffMedium: { backgroundColor: '#1e3a5f' },
  difficultyText: { fontSize: 11, color: '#fff', fontWeight: '600' },

  // Locked Cards (preview)
  lockedCard: { backgroundColor: '#1e293b', borderRadius: 14, padding: 14, marginBottom: 8, opacity: 0.5 },
  lockedNumber: { backgroundColor: '#334155' },
  lockedScenarioTitle: { fontSize: 14, fontWeight: '600', color: '#94a3b8', marginBottom: 2 },
  lockedScenarioDesc: { fontSize: 12, color: '#64748b' },
});

