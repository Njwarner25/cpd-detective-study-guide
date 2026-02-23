// frontend/app/upgrade.tsx - Welcome + Premium Upgrade Screen
// This is the FIRST screen users see after login
import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ScrollView, ActivityIndicator, Alert, Platform, Linking } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import { useAuth } from '../contexts/AuthContext';
import { paymentService } from '../services/api';

// Cross-platform alert helper - Alert.alert does NOT work on web
const showAlert = (title: string, message: string, buttons?: Array<{text: string, style?: string, onPress?: () => void}>) => {
  if (Platform.OS === 'web') {
    if (buttons && buttons.length > 1) {
      const confirmButton = buttons.find(b => b.style !== 'cancel');
      const result = window.confirm(`${title}\n\n${message}`);
      if (result && confirmButton?.onPress) {
        confirmButton.onPress();
      }
    } else if (buttons && buttons.length === 1 && buttons[0].onPress) {
      window.alert(`${title}\n\n${message}`);
      buttons[0].onPress();
    } else {
      window.alert(`${title}\n\n${message}`);
    }
  } else {
    Alert.alert(title, message, buttons as any);
  }
};

export default function Upgrade() {
  const router = useRouter();
  const { user, sessionToken, isGuest, hasPaid, refreshPaymentStatus } = useAuth();
  const [loading, setLoading] = useState(false);
  const [verifying, setVerifying] = useState(false);

  const handleUpgrade = async () => {
    console.log('[Upgrade] handleUpgrade called');
    console.log('[Upgrade] isGuest:', isGuest, 'sessionToken:', sessionToken ? 'exists' : 'null');
    if (isGuest) {
      console.log('[Upgrade] User is guest, showing alert');
      showAlert('Account Required', 'Please create an account before purchasing premium access.', [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Register', onPress: () => router.push('/(auth)/login') },
      ]);
      return;
    }
    setLoading(true);
    try {
      console.log('[Upgrade] Calling createCheckoutSession...');
      const { checkout_url } = await paymentService.createCheckoutSession(sessionToken || undefined);
      console.log('[Upgrade] Got checkout_url:', checkout_url);
      if (Platform.OS === 'web') { window.location.href = checkout_url; }
      else { await Linking.openURL(checkout_url); }
    } catch (error: any) {
      console.error('[Upgrade] Error:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to start checkout.';
      showAlert('Error', errorMessage);
    } finally { setLoading(false); }
  };

  const handleVerifyPayment = async () => {
    setVerifying(true);
    try {
      const paid = await refreshPaymentStatus();
      if (paid) {
        showAlert('Premium Activated!', 'Your premium access is now active.', [
          { text: 'Start Studying', onPress: () => router.replace('/(tabs)/home') }
        ]);
      } else {
        showAlert('Payment Not Found', 'We have not received your payment yet. Please wait and try again.');
      }
    } catch (error) { showAlert('Error', 'Failed to verify payment.'); }
    finally { setVerifying(false); }
  };

  if (hasPaid) { router.replace('/(tabs)/home'); return null; }

  return (
    <SafeAreaView style={st.container}>
      <ScrollView style={st.scrollView} contentContainerStyle={st.scrollContent} showsVerticalScrollIndicator={false}>
        <View style={st.congratsSection}>
          <Text style={st.congratsEmoji}>{String.fromCodePoint(0x1F389)}</Text>
          <Text style={st.congratsTitle}>Congratulations, {user?.name?.split(' ')[0] || 'Detective'}!</Text>
          <Text style={st.congratsSubtitle}>You passed Part 1 of the Detective Exam.</Text>
          <View style={st.congratsDivider} />
          <Text style={st.congratsText}>Now it is time to prepare for Part 2 - the scenario-based assessment. This app was built by a fellow officer to give you the best chance at earning that promotion.</Text>
        </View>
        <View style={st.previewCard}>
          <Text style={st.previewTitle}>What's Inside</Text>
          {[
            { icon: 'document-text', color: '#3b82f6', bg: '#1e3a5f', title: '20 Practice Scenarios', desc: 'Real exam-style scenarios covering every category' },
            { icon: 'sparkles', color: '#f59e0b', bg: '#1a1a2e', title: 'AI-Powered Grading', desc: 'Instant feedback graded by GPT-4' },
            { icon: 'build', color: '#F97316', bg: '#0f2922', title: 'Curveball Complications', desc: 'Mid-response twists just like the real exam' },
            { icon: 'trophy', color: '#8b5cf6', bg: '#1a0f2e', title: 'Leaderboard & Progress', desc: 'Track improvement and rank against others' },
            { icon: 'infinite', color: '#10b981', bg: '#0f2922', title: 'Lifetime Access', desc: 'Pay once, study forever' },
          ].map((item, i) => (
            <View key={i} style={st.previewItem}>
              <View style={[st.previewIcon, { backgroundColor: item.bg }]}>
                <Ionicons name={item.icon} size={20} color={item.color} />
              </View>
              <View style={st.previewContent}>
                <Text style={st.previewItemTitle}>{item.title}</Text>
                <Text style={st.previewItemDesc}>{item.desc}</Text>
              </View>
            </View>
          ))}
        </View>
        <View style={st.gradingCard}>
          <View style={st.gradingHeader}>
            <Ionicons name="school" size={22} color="#60a5fa" />
            <Text style={st.gradingTitle}>I/O Solutions Grading Matrix</Text>
          </View>
          <Text style={st.gradingIntro}>Part 2 is scored by I/O Solutions using a structured behavioral checklist. Assessors evaluate your written response against Mandatory Courses of Action using a standardized rubric.</Text>
          <Text style={st.gradingSectionTitle}>How Responses Are Scored</Text>
          {[
            { sc: '+2', bg: '#064e3b', l: 'Fully addresses the action with specific detail' },
            { sc: '+1', bg: '#1e3a5f', l: 'Mentions the action but lacks specificity' },
            { sc: '0', bg: '#334155', l: 'Action not addressed in the response' },
            { sc: '-1', bg: '#7f1d1d', l: 'Incorrect procedure or policy violation' },
          ].map((r, i) => (
            <View key={i} style={st.scoreRow}>
              <View style={[st.scoreBadge, { backgroundColor: r.bg }]}>
                <Text style={st.scoreBadgeText}>{r.sc}</Text>
              </View>
              <Text style={st.scoreLabel}>{r.l}</Text>
            </View>
          ))}
          <View style={st.gradingDivider} />
          <Text style={st.gradingSectionTitle}>Evaluation Categories</Text>
          {[
            { i: 'shield-checkmark', t: 'Responding to & Investigating Crimes' },
            { i: 'search', t: 'Information Collection & Analysis' },
            { i: 'finger-print', t: 'Evidence Collection & Preservation' },
            { i: 'hand-left', t: 'Arrest-Related Activities' },
            { i: 'briefcase', t: 'Court-Related Activities' },
            { i: 'chatbubbles', t: 'Communication & Coordination' },
          ].map((c, i) => (
            <View key={i} style={st.categoryItem}>
              <Ionicons name={c.i} size={16} color="#10b981" />
              <Text style={st.categoryText}>{c.t}</Text>
            </View>
          ))}
          <View style={st.gradingDivider} />
          <View style={st.aiMatchNote}>
            <Ionicons name="checkmark-circle" size={18} color="#10b981" />
            <Text style={st.aiMatchText}>Our AI grading evaluates your response against the same Mandatory Courses of Action and weighted scoring - giving you real exam-level feedback before test day.</Text>
          </View>
        </View>
        <View style={st.priceCard}>
          <View style={st.priceBadgeRow}>
            <View style={st.premiumBadge}>
              <Ionicons name="star" size={14} color="#fff" />
              <Text style={st.premiumBadgeText}>PREMIUM</Text>
            </View>
          </View>
          <View style={st.priceRow}>
            <Text style={st.priceAmount}>$25</Text>
            <View style={st.priceDetails}>
              <Text style={st.priceLabel}>one-time payment</Text>
              <Text style={st.priceNote}>Not a subscription. Never charged again.</Text>
            </View>
          </View>
          <View style={st.priceDivider} />
          <Text style={st.disclaimerText}>100% of proceeds go directly toward server costs, AI grading fees, and keeping this study tool running for CPD officers.</Text>
        </View>
        <View style={st.noteCard}>
          <Ionicons name="heart" size={20} color="#f59e0b" />
          <View style={st.noteContent}>
            <Text style={st.noteTitle}>From a Fellow Officer</Text>
            <Text style={st.noteText}>I built this because I wanted something better than flashcards to prepare for Part 2. The AI grading and server costs made it impossible to keep free. Thank you for supporting this tool.</Text>
          </View>
        </View>
        <TouchableOpacity style={[st.upgradeButton, loading && st.buttonDisabled]} onPress={handleUpgrade} disabled={loading}>
          {loading ? <ActivityIndicator color="#fff" /> : (
            <><Ionicons name="lock-open" size={20} color="#fff" /><Text style={st.upgradeButtonText}>Unlock Premium - $25.00</Text></>
          )}
        </TouchableOpacity>
        <TouchableOpacity style={st.verifyButton} onPress={handleVerifyPayment} disabled={verifying}>
          {verifying ? <ActivityIndicator color="#60a5fa" size="small" /> : <Text style={st.verifyButtonText}>Already paid? Tap to verify</Text>}
        </TouchableOpacity>
        <TouchableOpacity style={st.freeButton} onPress={() => router.replace('/(tabs)/home')}>
          <Text style={st.freeButtonText}>Continue with free content</Text>
        </TouchableOpacity>
        <Text style={st.secureText}>Secure payment powered by Stripe</Text>
      </ScrollView>
    </SafeAreaView>
  );
}

const st = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0c0c0c' },
  scrollView: { flex: 1 },
  scrollContent: { padding: 20, paddingBottom: 40 },
  congratsSection: { alignItems: 'center', marginBottom: 24, paddingTop: 8 },
  congratsEmoji: { fontSize: 48, marginBottom: 12 },
  congratsTitle: { fontSize: 26, fontWeight: 'bold', color: '#fff', textAlign: 'center', marginBottom: 6 },
  congratsSubtitle: { fontSize: 17, fontWeight: '600', color: '#10b981', textAlign: 'center', marginBottom: 16 },
  congratsDivider: { width: 40, height: 3, backgroundColor: '#2563eb', borderRadius: 2, marginBottom: 16 },
  congratsText: { fontSize: 15, color: '#94a3b8', textAlign: 'center', lineHeight: 23, maxWidth: 340 },
  previewCard: { backgroundColor: '#1e293b', borderRadius: 16, padding: 20, marginBottom: 16 },
  previewTitle: { fontSize: 18, fontWeight: 'bold', color: '#fff', marginBottom: 16 },
  previewItem: { flexDirection: 'row', alignItems: 'center', marginBottom: 14 },
  previewIcon: { width: 40, height: 40, borderRadius: 12, alignItems: 'center', justifyContent: 'center', marginRight: 12 },
  previewContent: { flex: 1 },
  previewItemTitle: { fontSize: 15, fontWeight: '600', color: '#fff', marginBottom: 2 },
  previewItemDesc: { fontSize: 13, color: '#94a3b8' },
  gradingCard: { backgroundColor: '#1e293b', borderRadius: 16, padding: 20, marginBottom: 16 },
  gradingHeader: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 12 },
  gradingTitle: { fontSize: 18, fontWeight: 'bold', color: '#fff' },
  gradingIntro: { fontSize: 14, color: '#94a3b8', lineHeight: 22, marginBottom: 16 },
  gradingSectionTitle: { fontSize: 15, fontWeight: '600', color: '#e2e8f0', marginBottom: 10 },
  scoreRow: { flexDirection: 'row', alignItems: 'center', marginBottom: 8 },
  scoreBadge: { width: 36, height: 28, borderRadius: 6, alignItems: 'center', justifyContent: 'center', marginRight: 12 },
  scoreBadgeText: { fontSize: 13, fontWeight: 'bold', color: '#fff' },
  scoreLabel: { flex: 1, fontSize: 14, color: '#94a3b8' },
  categoryItem: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 6 },
  categoryText: { fontSize: 14, color: '#e2e8f0', fontWeight: '500' },
  aiMatchNote: { flexDirection: 'row', gap: 10, alignItems: 'flex-start' },
  aiMatchText: { flex: 1, fontSize: 13, color: '#10b981', lineHeight: 20, fontWeight: '500' },
  priceCard: { backgroundColor: '#1e293b', borderRadius: 16, padding: 20, marginBottom: 16, borderWidth: 1, borderColor: 'rgba(16, 185, 129, 0.2)' },
  priceBadgeRow: { flexDirection: 'row', marginBottom: 14 },
  premiumBadge: { flexDirection: 'row', alignItems: 'center', gap: 5, backgroundColor: '#f59e0b', paddingHorizontal: 12, paddingVertical: 5, borderRadius: 16 },
  premiumBadgeText: { color: '#fff', fontSize: 11, fontWeight: '700', letterSpacing: 1 },
  priceRow: { flexDirection: 'row', alignItems: 'center', gap: 14, marginBottom: 14 },
  priceAmount: { fontSize: 52, fontWeight: 'bold', color: '#10b981' },
  priceDetails: { flex: 1 },
  priceLabel: { fontSize: 16, fontWeight: '600', color: '#e2e8f0', marginBottom: 2 },
  priceNote: { fontSize: 13, color: '#64748b' },
  priceDivider: { height: 1, backgroundColor: '#334155', marginBottom: 14 },
  disclaimerText: { fontSize: 13, color: '#94a3b8', lineHeight: 20 },
  noteCard: { backgroundColor: '#1e293b', borderRadius: 12, padding: 16, marginBottom: 24, flexDirection: 'row', gap: 12, borderWidth: 1, borderColor: 'rgba(245, 158, 11, 0.08)' },
  noteContent: { flex: 1 },
  noteTitle: { color: '#f59e0b', fontSize: 15, fontWeight: '700', marginBottom: 6 },
  noteText: { color: '#94a3b8', fontSize: 13, lineHeight: 20 },
  upgradeButton: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8, backgroundColor: '#10b981', padding: 18, borderRadius: 12, marginBottom: 12 },
  buttonDisabled: { opacity: 0.7 },
  upgradeButtonText: { color: '#fff', fontSize: 18, fontWeight: '700' },
  verifyButton: { alignItems: 'center', padding: 12, marginBottom: 4 },
  verifyButtonText: { color: '#60a5fa', fontSize: 14, fontWeight: '500' },
  freeButton: { alignItems: 'center', padding: 12, marginBottom: 8 },
  freeButtonText: { color: '#64748b', fontSize: 14 },
  secureText: { textAlign: 'center', fontSize: 12, color: '#475569', marginBottom: 8 },
  gradingDivider: { height: 1, backgroundColor: '#334155', marginVertical: 12 },
});
