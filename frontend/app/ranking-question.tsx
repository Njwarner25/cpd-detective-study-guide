import React, { useEffect, useState, useRef } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  ActivityIndicator,
  Platform,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useAuth } from '../contexts/AuthContext';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { questionService, rankingService, ttsService } from '../services/api';
import DetectiveBotBubble from '../components/DetectiveBotBubble';
import ChatOverlay from '../components/ChatOverlay';

type Phase = 'loading' | 'ranking' | 'submitting' | 'result';

interface RankingItem {
  label: string;
  text: string;
}

interface ItemScore {
  item_index: number;
  label: string;
  text: string;
  user_position: number;
  correct_position: number;
  displacement: number;
  score: number;
}

export default function RankingQuestion() {
  const { sessionToken } = useAuth();
  const router = useRouter();
  const { questionId, title: paramTitle, categoryId: paramCategoryId } = useLocalSearchParams<{ questionId: string; title: string; categoryId?: string }>();

  const [phase, setPhase] = useState<Phase>('loading');
  const [question, setQuestion] = useState<any>(null);
  const [items, setItems] = useState<RankingItem[]>([]);
  const [selectedOrder, setSelectedOrder] = useState<number[]>([]);
  const [result, setResult] = useState<any>(null);
  const [allQuestions, setAllQuestions] = useState<any[]>([]);
  const startTime = useRef(Date.now());

  // TTS state
  const [isTTSPlaying, setIsTTSPlaying] = useState(false);
  const ttsRef = useRef<any>(null);

  // Chatbot state
  const [chatVisible, setChatVisible] = useState(false);
  const [hintCount, setHintCount] = useState(0);

  useEffect(() => {
    loadQuestion();
    loadAllQuestions();
    return () => stopTTS();
  }, [questionId]);

  const loadAllQuestions = async () => {
    if (allQuestions.length > 0) return;
    try {
      const catId = paramCategoryId || 'cat_ranking';
      const typeFilter = paramCategoryId ? undefined : 'ranking';
      const data = await questionService.getQuestions(typeFilter, catId, sessionToken || undefined);
      setAllQuestions(data || []);
    } catch (e) {
      console.error('Failed to load question list:', e);
    }
  };

  const getNextQuestion = () => {
    if (allQuestions.length === 0) return null;
    const currentIndex = allQuestions.findIndex((q: any) => q.question_id === questionId);
    if (currentIndex === -1 || currentIndex >= allQuestions.length - 1) return null;
    return allQuestions[currentIndex + 1];
  };

  const goToNextQuestion = () => {
    const next = getNextQuestion();
    if (!next) return;
    stopTTS();
    setSelectedOrder([]);
    setResult(null);
    setPhase('loading');
    setHintCount(0);
    if (next.type === 'ranking') {
      router.replace({
        pathname: '/ranking-question',
        params: { questionId: next.question_id, title: next.title, categoryId: paramCategoryId || '' },
      });
    } else {
      router.replace({
        pathname: '/exam-question',
        params: { questionId: next.question_id, title: next.title, questionType: next.type || 'most_appropriate', categoryId: paramCategoryId || '' },
      });
    }
  };

  // TTS functions
  const toggleTTS = async (text: string) => {
    if (isTTSPlaying) { stopTTS(); return; }
    try {
      stopTTS();
      setIsTTSPlaying(true);
      const audioUrl = await ttsService.generateSpeech(text, sessionToken || undefined, 'nova');
      const audio = new Audio(audioUrl);
      audio.onended = () => { setIsTTSPlaying(false); URL.revokeObjectURL(audioUrl); };
      audio.onerror = () => { setIsTTSPlaying(false); URL.revokeObjectURL(audioUrl); };
      ttsRef.current = audio;
      await audio.play();
    } catch (e) {
      console.error('TTS error:', e);
      setIsTTSPlaying(false);
      if (Platform.OS === 'web' && 'speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.95;
        utterance.onend = () => setIsTTSPlaying(false);
        utterance.onerror = () => setIsTTSPlaying(false);
        ttsRef.current = utterance;
        window.speechSynthesis.speak(utterance);
        setIsTTSPlaying(true);
      }
    }
  };

  const stopTTS = () => {
    if (ttsRef.current) {
      if (ttsRef.current instanceof Audio) { ttsRef.current.pause(); ttsRef.current.currentTime = 0; }
      else if (Platform.OS === 'web' && 'speechSynthesis' in window) { window.speechSynthesis.cancel(); }
    }
    setIsTTSPlaying(false);
  };

  const loadQuestion = async () => {
    try {
      const data = await questionService.getQuestion(questionId!, sessionToken || undefined);
      setQuestion(data);
      setItems(data.items || []);
      setPhase('ranking');
      startTime.current = Date.now();
    } catch (e: any) {
      console.error('Failed to load ranking question:', e);
      if (e?.isPremiumRequired || e?.status === 403) {
        router.replace('/upgrade');
      } else {
        // Show error state instead of infinite spinner
        setPhase('ranking');
      }
    }
  };

  const handleSelectItem = (index: number) => {
    if (selectedOrder.includes(index)) {
      // Remove this item and all after it (reset from this point)
      const pos = selectedOrder.indexOf(index);
      setSelectedOrder(selectedOrder.slice(0, pos));
    } else {
      setSelectedOrder([...selectedOrder, index]);
    }
  };

  const handleClearAll = () => {
    setSelectedOrder([]);
  };

  const handleSubmit = async () => {
    if (selectedOrder.length !== items.length) return;
    setPhase('submitting');
    const timeTaken = Math.floor((Date.now() - startTime.current) / 1000);
    try {
      const data = await rankingService.submitResponse(
        questionId!,
        selectedOrder,
        timeTaken,
        sessionToken || undefined
      );
      setResult(data);
      setPhase('result');
    } catch (e) {
      console.error('Failed to submit ranking:', e);
      setPhase('ranking');
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 2) return '#22c55e';
    if (score >= 1) return '#86efac';
    if (score === 0) return '#94a3b8';
    if (score === -1) return '#f87171';
    return '#ef4444';
  };

  const getScoreBg = (score: number) => {
    if (score >= 2) return '#166534';
    if (score >= 1) return '#14532d';
    if (score === 0) return '#334155';
    if (score === -1) return '#7f1d1d';
    return '#991b1b';
  };

  const getScoreLabel = (score: number) => {
    if (score === 2) return 'Correct';
    if (score === 1) return 'Close';
    if (score === 0) return 'Neutral';
    if (score === -1) return 'Counter-productive';
    return 'Harmful';
  };

  // Loading state
  if (phase === 'loading') {
    return (
      <SafeAreaView style={s.safe}>
        <View style={s.centered}>
          <ActivityIndicator size="large" color="#60a5fa" />
          <Text style={s.loadingTxt}>Loading question...</Text>
        </View>
      </SafeAreaView>
    );
  }

  // Submitting state
  if (phase === 'submitting') {
    return (
      <SafeAreaView style={s.safe}>
        <View style={s.centered}>
          <ActivityIndicator size="large" color="#60a5fa" />
          <Text style={s.loadingTxt}>Grading your ranking...</Text>
        </View>
      </SafeAreaView>
    );
  }

  // Result state
  if (phase === 'result' && result) {
    const itemScores: ItemScore[] = result.item_scores || [];
    const sorted = [...itemScores].sort((a, b) => a.correct_position - b.correct_position);

    return (
      <SafeAreaView style={s.safe}>
        <ScrollView style={s.scroll} contentContainerStyle={s.content}>
          {/* Header */}
          <TouchableOpacity style={s.backBtn} onPress={() => router.back()}>
            <Ionicons name="arrow-back" size={22} color="#60a5fa" />
            <Text style={s.backTxt}>Back to Scenarios</Text>
          </TouchableOpacity>

          <Text style={s.resultTitle}>Results</Text>

          {/* Score Card */}
          <View style={s.scoreCard}>
            <Text style={s.scoreNum}>{result.normalized_score}</Text>
            <Text style={s.scoreLabel}>/ 100</Text>
            <Text style={s.rawScore}>Raw: {result.total_raw} / {result.max_possible}</Text>
          </View>

          {/* I/O Scoring Legend */}
          <View style={s.legendCard}>
            <Text style={s.legendTitle}>I/O Solutions Scoring</Text>
            <View style={s.legendRow}>
              <View style={[s.legendBadge, { backgroundColor: '#166534' }]}><Text style={s.legendVal}>+2</Text></View>
              <Text style={s.legendTxt}>Correct position</Text>
            </View>
            <View style={s.legendRow}>
              <View style={[s.legendBadge, { backgroundColor: '#14532d' }]}><Text style={s.legendVal}>+1</Text></View>
              <Text style={s.legendTxt}>Off by 1 (close)</Text>
            </View>
            <View style={s.legendRow}>
              <View style={[s.legendBadge, { backgroundColor: '#334155' }]}><Text style={s.legendVal}> 0</Text></View>
              <Text style={s.legendTxt}>Off by 2 (neutral)</Text>
            </View>
            <View style={s.legendRow}>
              <View style={[s.legendBadge, { backgroundColor: '#7f1d1d' }]}><Text style={s.legendVal}>-1</Text></View>
              <Text style={s.legendTxt}>Off by 3 (counterproductive)</Text>
            </View>
            <View style={s.legendRow}>
              <View style={[s.legendBadge, { backgroundColor: '#991b1b' }]}><Text style={s.legendVal}>-2</Text></View>
              <Text style={s.legendTxt}>Off by 4+ (harmful)</Text>
            </View>
          </View>

          {/* Per-item results sorted by correct order */}
          <Text style={s.sectionHead}>Correct Order vs. Your Ranking</Text>
          {sorted.map((item, i) => (
            <View key={i} style={[s.resultItem, { borderLeftColor: getScoreColor(item.score), borderLeftWidth: 3 }]}>
              <View style={s.resultTop}>
                <View style={s.posRow}>
                  <Text style={s.posLabel}>Correct:</Text>
                  <View style={s.posBadge}><Text style={s.posNum}>#{item.correct_position}</Text></View>
                  <Text style={s.posLabel}>Yours:</Text>
                  <View style={[s.posBadge, { backgroundColor: item.displacement === 0 ? '#166534' : '#334155' }]}>
                    <Text style={s.posNum}>#{item.user_position}</Text>
                  </View>
                </View>
                <View style={[s.scoreBadge, { backgroundColor: getScoreBg(item.score) }]}>
                  <Text style={[s.scoreBadgeTxt, { color: getScoreColor(item.score) }]}>
                    {item.score > 0 ? '+' : ''}{item.score}
                  </Text>
                </View>
              </View>
              <Text style={s.resultItemLabel}>{item.label}. {item.text}</Text>
              <Text style={[s.resultTag, { color: getScoreColor(item.score) }]}>{getScoreLabel(item.score)}</Text>
            </View>
          ))}

          {/* Explanation */}
          {result.explanation && (
            <View style={s.explanationCard}>
              <Ionicons name="bulb-outline" size={18} color="#fbbf24" />
              <Text style={s.explanationTitle}>Explanation</Text>
              <Text style={s.explanationTxt}>{result.explanation}</Text>
            </View>
          )}

          {/* Try Again / Next */}
          <View style={s.resultActions}>
            <TouchableOpacity style={s.retryBtn} onPress={() => { setSelectedOrder([]); setResult(null); setPhase('ranking'); startTime.current = Date.now(); }}>
              <Ionicons name="refresh" size={18} color="#000" />
              <Text style={s.retryTxt}>Try Again</Text>
            </TouchableOpacity>

            {getNextQuestion() && (
              <TouchableOpacity style={s.nextBtn} onPress={goToNextQuestion}>
                <Text style={s.nextTxt}>Next Question</Text>
                <Ionicons name="arrow-forward" size={18} color="#fff" />
              </TouchableOpacity>
            )}
          </View>

          <View style={{ height: 120 }} />
        </ScrollView>

        {/* Bot 9165 */}
        <DetectiveBotBubble onPress={() => setChatVisible(true)} hintCount={hintCount} />
        <ChatOverlay
          visible={chatVisible}
          onClose={() => setChatVisible(false)}
          questionId={question?.question_id || questionId!}
          userCurrentResponse={`Submitted ranking. Score: ${result.normalized_score}/100`}
          onHintReceived={(count) => setHintCount(count)}
        />
      </SafeAreaView>
    );
  }

  // Ranking phase — handle missing question data
  if (!question || items.length === 0) {
    return (
      <SafeAreaView style={s.safe}>
        <View style={s.centered}>
          <Ionicons name="alert-circle-outline" size={48} color="#f87171" />
          <Text style={[s.loadingTxt, { color: '#f87171', marginTop: 12 }]}>Failed to load question</Text>
          <TouchableOpacity style={{ marginTop: 16, backgroundColor: '#2563eb', paddingHorizontal: 24, paddingVertical: 10, borderRadius: 12 }} onPress={() => { setPhase('loading'); loadQuestion(); }}>
            <Text style={{ color: '#fff', fontWeight: '700', fontSize: 14 }}>Retry</Text>
          </TouchableOpacity>
          <TouchableOpacity style={{ marginTop: 10 }} onPress={() => router.back()}>
            <Text style={{ color: '#60a5fa', fontSize: 14 }}>Go Back</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  const allSelected = selectedOrder.length === items.length;

  return (
    <SafeAreaView style={s.safe}>
      <ScrollView style={s.scroll} contentContainerStyle={s.content}>
        {/* Header */}
        <TouchableOpacity style={s.backBtn} onPress={() => router.back()}>
          <Ionicons name="arrow-back" size={22} color="#60a5fa" />
          <Text style={s.backTxt}>Back</Text>
        </TouchableOpacity>

        <View style={s.headerBadgeRow}>
          <View style={s.typeBadge}><Ionicons name="list" size={12} color="#60a5fa" /><Text style={s.typeTxt}>RANKING</Text></View>
          {question?.difficulty && (
            <View style={[s.diffBadge, question.difficulty === 'hard' ? s.diffH : s.diffM]}>
              <Text style={s.diffTxt}>{question.difficulty}</Text>
            </View>
          )}
        </View>

        <Text style={s.qTitle}>{question?.title || paramTitle}</Text>

        {/* Scenario Text */}
        <View style={s.scenarioCard}>
          <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <Text style={[s.scenarioTxt, { flex: 1 }]}>{question?.content}</Text>
            <TouchableOpacity onPress={() => toggleTTS(question?.content || '')} style={s.ttsBtn}>
              <Ionicons name={isTTSPlaying ? 'stop' : 'volume-high'} size={18} color="#60a5fa" />
            </TouchableOpacity>
          </View>
        </View>

        {/* Instructions */}
        <View style={s.instructCard}>
          <Ionicons name="information-circle-outline" size={16} color="#60a5fa" />
          <Text style={s.instructTxt}>
            Tap each action in the order you would perform it (1st, 2nd, 3rd...). Tap a numbered action to undo from that point.
          </Text>
        </View>

        {/* Progress indicator */}
        <Text style={s.progressTxt}>{selectedOrder.length} of {items.length} ranked</Text>

        {/* Items to rank */}
        {items.map((item, index) => {
          const orderPos = selectedOrder.indexOf(index);
          const isSelected = orderPos !== -1;
          const rank = orderPos + 1;

          return (
            <TouchableOpacity
              key={index}
              style={[s.rankItem, isSelected && s.rankItemSelected]}
              onPress={() => handleSelectItem(index)}
              activeOpacity={0.7}
            >
              <View style={s.rankRow}>
                {isSelected ? (
                  <View style={s.rankBadge}>
                    <Text style={s.rankNum}>{rank}</Text>
                  </View>
                ) : (
                  <View style={s.rankBadgeEmpty}>
                    <Text style={s.rankLabel}>{item.label}</Text>
                  </View>
                )}
                <Text style={[s.rankTxt, isSelected && s.rankTxtSelected]}>{item.text}</Text>
              </View>
            </TouchableOpacity>
          );
        })}

        {/* Action buttons */}
        <View style={s.actions}>
          {selectedOrder.length > 0 && (
            <TouchableOpacity style={s.clearBtn} onPress={handleClearAll}>
              <Ionicons name="close-circle-outline" size={18} color="#f87171" />
              <Text style={s.clearTxt}>Clear All</Text>
            </TouchableOpacity>
          )}
          <TouchableOpacity
            style={[s.submitBtn, !allSelected && s.submitDisabled]}
            onPress={handleSubmit}
            disabled={!allSelected}
          >
            <Ionicons name="checkmark-circle" size={18} color={allSelected ? '#000' : '#64748b'} />
            <Text style={[s.submitTxt, !allSelected && s.submitTxtDisabled]}>Submit Ranking</Text>
          </TouchableOpacity>
        </View>

        <View style={{ height: 120 }} />
      </ScrollView>

      {/* Bot 9165 */}
      <DetectiveBotBubble onPress={() => setChatVisible(true)} hintCount={hintCount} />
      <ChatOverlay
        visible={chatVisible}
        onClose={() => setChatVisible(false)}
        questionId={question?.question_id || questionId!}
        userCurrentResponse={selectedOrder.length > 0 ? `Current ranking order: ${selectedOrder.map((idx, pos) => `${pos + 1}. ${items[idx]?.label}`).join(', ')}` : ''}
        onHintReceived={(count) => setHintCount(count)}
      />
    </SafeAreaView>
  );
}

const s = StyleSheet.create({
  safe: { flex: 1, backgroundColor: '#0f172a' },
  scroll: { flex: 1 },
  content: { padding: 16, paddingBottom: 100 },
  centered: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  loadingTxt: { color: '#94a3b8', marginTop: 12, fontSize: 14 },

  // Navigation
  backBtn: { flexDirection: 'row', alignItems: 'center', gap: 6, marginBottom: 16 },
  backTxt: { color: '#60a5fa', fontSize: 15, fontWeight: '600' },

  // Header
  headerBadgeRow: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 8 },
  typeBadge: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#1e3a5f', paddingHorizontal: 10, paddingVertical: 4, borderRadius: 12, gap: 4 },
  typeTxt: { color: '#60a5fa', fontSize: 11, fontWeight: '700' },
  diffBadge: { paddingHorizontal: 8, paddingVertical: 2, borderRadius: 6 },
  diffH: { backgroundColor: '#7f1d1d' },
  diffM: { backgroundColor: '#1e3a5f' },
  diffTxt: { fontSize: 11, color: '#fff', fontWeight: '600' },
  qTitle: { fontSize: 20, fontWeight: '800', color: '#f1f5f9', marginBottom: 12 },

  // Scenario
  scenarioCard: { backgroundColor: '#1e293b', borderRadius: 12, padding: 14, marginBottom: 12, borderWidth: 1, borderColor: '#334155' },
  scenarioTxt: { fontSize: 14, color: '#cbd5e1', lineHeight: 22 },

  // Instructions
  instructCard: { flexDirection: 'row', alignItems: 'flex-start', backgroundColor: 'rgba(96,165,250,0.1)', borderRadius: 10, padding: 10, marginBottom: 12, gap: 8 },
  instructTxt: { flex: 1, fontSize: 12, color: '#93c5fd', lineHeight: 18 },

  // Progress
  progressTxt: { fontSize: 13, color: '#94a3b8', fontWeight: '600', marginBottom: 10 },

  // Ranking items
  rankItem: { backgroundColor: '#1e293b', borderRadius: 10, padding: 12, marginBottom: 8, borderWidth: 1, borderColor: '#334155' },
  rankItemSelected: { borderColor: '#60a5fa', backgroundColor: '#172554' },
  rankRow: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  rankBadge: { width: 30, height: 30, borderRadius: 15, backgroundColor: '#2563eb', alignItems: 'center', justifyContent: 'center' },
  rankNum: { fontSize: 14, fontWeight: '800', color: '#fff' },
  rankBadgeEmpty: { width: 30, height: 30, borderRadius: 15, backgroundColor: '#334155', alignItems: 'center', justifyContent: 'center' },
  rankLabel: { fontSize: 13, fontWeight: '700', color: '#94a3b8' },
  rankTxt: { flex: 1, fontSize: 13, color: '#cbd5e1', lineHeight: 19 },
  rankTxtSelected: { color: '#f1f5f9' },

  // Actions
  actions: { flexDirection: 'row', justifyContent: 'center', gap: 12, marginTop: 16 },
  clearBtn: { flexDirection: 'row', alignItems: 'center', gap: 6, paddingHorizontal: 16, paddingVertical: 10, borderRadius: 20, borderWidth: 1, borderColor: '#7f1d1d' },
  clearTxt: { color: '#f87171', fontSize: 14, fontWeight: '600' },
  submitBtn: { flexDirection: 'row', alignItems: 'center', gap: 6, backgroundColor: '#fbbf24', paddingHorizontal: 20, paddingVertical: 10, borderRadius: 20 },
  submitDisabled: { backgroundColor: '#334155' },
  submitTxt: { fontSize: 14, fontWeight: '700', color: '#000' },
  submitTxtDisabled: { color: '#64748b' },

  // Results
  resultTitle: { fontSize: 22, fontWeight: '800', color: '#f1f5f9', marginBottom: 16, textAlign: 'center' },
  scoreCard: { alignItems: 'center', backgroundColor: '#1e293b', borderRadius: 16, padding: 24, marginBottom: 16, borderWidth: 1, borderColor: '#334155' },
  scoreNum: { fontSize: 48, fontWeight: '900', color: '#60a5fa' },
  scoreLabel: { fontSize: 18, color: '#94a3b8', fontWeight: '600', marginTop: -4 },
  rawScore: { fontSize: 13, color: '#64748b', marginTop: 8 },

  // Legend
  legendCard: { backgroundColor: '#1e293b', borderRadius: 12, padding: 14, marginBottom: 16, borderWidth: 1, borderColor: '#334155' },
  legendTitle: { fontSize: 14, fontWeight: '700', color: '#e2e8f0', marginBottom: 10 },
  legendRow: { flexDirection: 'row', alignItems: 'center', marginBottom: 6, gap: 8 },
  legendBadge: { width: 32, height: 22, borderRadius: 6, alignItems: 'center', justifyContent: 'center' },
  legendVal: { fontSize: 12, fontWeight: '800', color: '#fff' },
  legendTxt: { fontSize: 12, color: '#94a3b8' },

  // Per-item results
  sectionHead: { fontSize: 15, fontWeight: '700', color: '#e2e8f0', marginBottom: 10 },
  resultItem: { backgroundColor: '#1e293b', borderRadius: 10, padding: 12, marginBottom: 8 },
  resultTop: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: 6 },
  posRow: { flexDirection: 'row', alignItems: 'center', gap: 6 },
  posLabel: { fontSize: 11, color: '#94a3b8' },
  posBadge: { backgroundColor: '#1e3a5f', paddingHorizontal: 8, paddingVertical: 2, borderRadius: 8 },
  posNum: { fontSize: 12, fontWeight: '700', color: '#fff' },
  scoreBadge: { paddingHorizontal: 10, paddingVertical: 3, borderRadius: 8 },
  scoreBadgeTxt: { fontSize: 14, fontWeight: '800' },
  resultItemLabel: { fontSize: 13, color: '#cbd5e1', lineHeight: 19, marginBottom: 4 },
  resultTag: { fontSize: 11, fontWeight: '600' },

  // Explanation
  explanationCard: { backgroundColor: 'rgba(251,191,36,0.08)', borderRadius: 12, padding: 14, marginTop: 12, marginBottom: 16 },
  explanationTitle: { fontSize: 14, fontWeight: '700', color: '#fbbf24', marginTop: 4, marginBottom: 6 },
  explanationTxt: { fontSize: 13, color: '#fde68a', lineHeight: 20 },

  // Result actions
  resultActions: { flexDirection: 'row', gap: 12, marginTop: 8 },
  retryBtn: { flex: 1, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', backgroundColor: '#fbbf24', paddingHorizontal: 16, paddingVertical: 12, borderRadius: 24, gap: 8 },
  retryTxt: { fontSize: 15, fontWeight: '700', color: '#000' },
  nextBtn: { flex: 1, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', backgroundColor: '#2563eb', paddingHorizontal: 16, paddingVertical: 12, borderRadius: 24, gap: 8 },
  nextTxt: { fontSize: 15, fontWeight: '700', color: '#fff' },

  // TTS
  ttsBtn: { padding: 8, borderRadius: 20, backgroundColor: 'rgba(96,165,250,0.15)', marginLeft: 8 },
});
