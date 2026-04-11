import React, { useEffect, useState, useRef } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  TextInput,
  ScrollView,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useAuth } from '../contexts/AuthContext';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { questionService, miniScenarioService, ttsService, feedbackService } from '../services/api';
import DetectiveBotBubble from '../components/DetectiveBotBubble';
import ChatOverlay from '../components/ChatOverlay';

const MINI_TIME = 10 * 60; // 10 minutes

const showAlert = (title: string, message: string, buttons?: any[]) => {
  if (Platform.OS === 'web') {
    if (buttons && buttons.length > 1) {
      const confirmBtn = buttons.find((b: any) => b.style !== 'cancel');
      const result = window.confirm(title + '\n\n' + message);
      if (result && confirmBtn && confirmBtn.onPress) confirmBtn.onPress();
    } else {
      window.alert(title + '\n\n' + message);
      if (buttons?.[0]?.onPress) buttons[0].onPress();
    }
  } else {
    const { Alert } = require('react-native');
    Alert.alert(title, message, buttons);
  }
};

type Phase = 'start' | 'respond' | 'submitting' | 'result';

export default function MiniScenario() {
  const { sessionToken } = useAuth();
  const router = useRouter();
  const { scenarioId, title: paramTitle } = useLocalSearchParams<{ scenarioId: string; title: string }>();

  const [scenario, setScenario] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [response, setResponse] = useState('');
  const [timeRemaining, setTimeRemaining] = useState(MINI_TIME);
  const [phase, setPhase] = useState<Phase>('start');
  const [result, setResult] = useState<any>(null);
  const [isTTSPlaying, setIsTTSPlaying] = useState(false);
  const [chatVisible, setChatVisible] = useState(false);
  const [hintCount, setHintCount] = useState(0);
  const [showFeedbackForm, setShowFeedbackForm] = useState(false);
  const [feedbackType, setFeedbackType] = useState('incorrect_grade');
  const [feedbackMessage, setFeedbackMessage] = useState('');
  const [feedbackSubmitting, setFeedbackSubmitting] = useState(false);
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false);
  const [allScenarios, setAllScenarios] = useState<any[]>([]);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const startTimeRef = useRef<number>(0);
  const ttsRef = useRef<any>(null);

  useEffect(() => { loadScenario(); loadAllScenarios(); return () => { stopTTS(); if (timerRef.current) clearInterval(timerRef.current); }; }, [scenarioId]);

  const loadScenario = async () => {
    try {
      const data = await questionService.getQuestion(scenarioId!, sessionToken || undefined);
      setScenario(data);
      setTimeRemaining(data.time_limit || MINI_TIME);
    } catch (e: any) {
      console.error('Failed to load mini scenario:', e);
      if (e?.isPremiumRequired || e?.status === 403) {
        router.replace('/upgrade');
        return;
      }
    }
    finally { setLoading(false); }
  };

  const loadAllScenarios = async () => {
    if (allScenarios.length > 0) return;
    try {
      const data = await questionService.getQuestions('mini_scenario', 'cat_mini_scenario', sessionToken || undefined);
      setAllScenarios(data || []);
    } catch (e) { console.error('Failed to load scenario list:', e); }
  };

  const getNextScenario = () => {
    if (allScenarios.length === 0) return null;
    const currentIndex = allScenarios.findIndex((q: any) => q.question_id === scenarioId);
    if (currentIndex === -1 || currentIndex >= allScenarios.length - 1) return null;
    return allScenarios[currentIndex + 1];
  };

  const goToNextScenario = () => {
    const next = getNextScenario();
    if (!next) return;
    stopTTS();
    if (timerRef.current) clearInterval(timerRef.current);
    router.replace({
      pathname: '/mini-scenario',
      params: { scenarioId: next.question_id, title: next.title },
    });
  };

  // Timer
  useEffect(() => {
    if (phase === 'respond') {
      timerRef.current = setInterval(() => {
        setTimeRemaining(prev => {
          if (prev <= 1) {
            if (timerRef.current) clearInterval(timerRef.current);
            handleSubmit(true);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }
    return () => { if (timerRef.current) clearInterval(timerRef.current); };
  }, [phase]);

  const formatTime = (s: number) => {
    const m = Math.floor(s / 60);
    const sec = s % 60;
    return `${m}:${sec.toString().padStart(2, '0')}`;
  };

  // TTS
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

  const handleStart = () => {
    setPhase('respond');
    startTimeRef.current = Date.now();
    if (scenario) {
      const text = scenario.content;
      if (text) toggleTTS(text);
    }
  };

  const handleSubmit = async (timeUp = false) => {
    if (timerRef.current) clearInterval(timerRef.current);
    stopTTS();

    if (!response.trim() && !timeUp) {
      showAlert('Empty Response', 'Please write your investigative steps before submitting.');
      return;
    }

    setPhase('submitting');
    const timeTaken = Math.floor((Date.now() - startTimeRef.current) / 1000);

    try {
      const data = await miniScenarioService.submitResponse(
        scenarioId!,
        response,
        timeTaken,
        sessionToken || undefined
      );
      setResult(data);
      setPhase('result');
    } catch (e) {
      console.error('Failed to submit mini scenario:', e);
      setPhase('respond');
      showAlert('Error', 'Failed to submit response. Please try again.');
    }
  };

  const handleFeedbackSubmit = async () => {
    if (!feedbackMessage.trim()) {
      showAlert('Error', 'Please describe the issue or correction.');
      return;
    }
    setFeedbackSubmitting(true);
    try {
      await feedbackService.submit({
        response_id: result?.response_id || '',
        question_id: scenario?.question_id || scenarioId || '',
        feedback_type: feedbackType,
        user_message: feedbackMessage.trim(),
      }, sessionToken || undefined);
      setFeedbackSubmitted(true);
      setShowFeedbackForm(false);
    } catch (e) {
      console.error('Failed to submit feedback:', e);
      showAlert('Error', 'Failed to submit feedback. Please try again.');
    } finally {
      setFeedbackSubmitting(false);
    }
  };

  if (loading) {
    return (
      <SafeAreaView style={s.safe}>
        <View style={s.centered}><ActivityIndicator size="large" color="#60a5fa" /><Text style={s.loadingTxt}>Loading...</Text></View>
      </SafeAreaView>
    );
  }

  // START PHASE
  if (phase === 'start') {
    return (
      <SafeAreaView style={s.safe}>
        <ScrollView style={s.scroll} contentContainerStyle={s.content}>
          <TouchableOpacity style={s.backBtn} onPress={() => router.back()}>
            <Ionicons name="arrow-back" size={22} color="#60a5fa" />
            <Text style={s.backTxt}>Back</Text>
          </TouchableOpacity>

          <View style={s.startCard}>
            <View style={s.typeBadge}><Ionicons name="document-text" size={14} color="#60a5fa" /><Text style={s.typeTxt}>MINI SCENARIO</Text></View>
            <Text style={s.startTitle}>{scenario?.title || paramTitle}</Text>
            <Text style={s.startDesc}>
              This is a shorter scenario designed to sharpen your prioritization skills. You have 10 minutes to outline 8-12 bullet points of investigative steps.
            </Text>
            <Text style={s.startTip}>
              These mini-scenarios help you practice hitting all R.E.A.C.T.I.O.N. steps without the pressure of a full 20-minute exam. Focus on correct prioritization.
            </Text>

            <View style={s.infoRow}>
              <View style={s.infoBadge}><Ionicons name="time-outline" size={14} color="#fbbf24" /><Text style={s.infoTxt}>10 minutes</Text></View>
              <View style={s.infoBadge}><Ionicons name="list-outline" size={14} color="#fbbf24" /><Text style={s.infoTxt}>8-12 bullet points</Text></View>
              <View style={s.infoBadge}><Ionicons name="school-outline" size={14} color="#fbbf24" /><Text style={s.infoTxt}>AI Graded</Text></View>
            </View>

            <TouchableOpacity style={s.startBtn} onPress={handleStart}>
              <Ionicons name="play" size={20} color="#000" />
              <Text style={s.startBtnTxt}>Begin Scenario</Text>
            </TouchableOpacity>
          </View>
        </ScrollView>
      </SafeAreaView>
    );
  }

  // SUBMITTING PHASE
  if (phase === 'submitting') {
    return (
      <SafeAreaView style={s.safe}>
        <View style={s.centered}>
          <ActivityIndicator size="large" color="#60a5fa" />
          <Text style={s.loadingTxt}>AI is grading your response...</Text>
          <Text style={s.loadingSub}>This may take 15-30 seconds</Text>
        </View>
      </SafeAreaView>
    );
  }

  // RESULT PHASE
  if (phase === 'result' && result) {
    return (
      <SafeAreaView style={s.safe}>
        <ScrollView style={s.scroll} contentContainerStyle={s.content}>
          <TouchableOpacity style={s.backBtn} onPress={() => router.back()}>
            <Ionicons name="arrow-back" size={22} color="#60a5fa" />
            <Text style={s.backTxt}>Back</Text>
          </TouchableOpacity>

          <Text style={s.resultTitle}>Results</Text>

          {/* Grade */}
          <View style={s.gradeCard}>
            <Text style={s.gradeNum}>{result.grade != null ? Math.round(result.grade) : '--'}</Text>
            <Text style={s.gradeLabel}>/ 100</Text>
          </View>

          {/* Feedback */}
          <View style={s.feedbackCard}>
            <Text style={s.feedbackTitle}>R.E.A.C.T.I.O.N. Breakdown</Text>
            <Text style={s.feedbackTxt}>{result.feedback}</Text>
          </View>

          {/* Your response */}
          <View style={s.yourResponseCard}>
            <Text style={s.yourResponseTitle}>Your Response</Text>
            <Text style={s.yourResponseTxt}>{response}</Text>
          </View>

          {/* Feedback Section */}
          {feedbackSubmitted ? (
            <View style={s.fbSuccessCard}>
              <Ionicons name="checkmark-circle" size={24} color="#10b981" />
              <Text style={s.fbSuccessTxt}>
                Thank you! Your feedback has been submitted and will be reviewed by our admin team.
              </Text>
            </View>
          ) : showFeedbackForm ? (
            <View style={s.fbFormCard}>
              <View style={s.fbFormHeader}>
                <Text style={s.fbFormTitle}>Report Issue / Suggest Correction</Text>
                <TouchableOpacity onPress={() => setShowFeedbackForm(false)}>
                  <Ionicons name="close" size={22} color="#94a3b8" />
                </TouchableOpacity>
              </View>

              <Text style={s.fbLabel}>Issue Type</Text>
              <View style={s.fbTypeRow}>
                {[
                  { value: 'incorrect_grade', label: 'Incorrect Grade' },
                  { value: 'missing_info', label: 'Missing Info' },
                  { value: 'wrong_procedure', label: 'Wrong Procedure' },
                  { value: 'general', label: 'General' },
                ].map((opt) => (
                  <TouchableOpacity
                    key={opt.value}
                    style={[s.fbTypeBtn, feedbackType === opt.value && s.fbTypeBtnActive]}
                    onPress={() => setFeedbackType(opt.value)}
                  >
                    <Text style={[s.fbTypeTxt, feedbackType === opt.value && s.fbTypeTxtActive]}>
                      {opt.label}
                    </Text>
                  </TouchableOpacity>
                ))}
              </View>

              <Text style={s.fbLabel}>Your Correction / Suggestion</Text>
              <TextInput
                style={s.fbInput}
                multiline
                placeholder="Describe what the AI got wrong or what should be corrected..."
                placeholderTextColor="#475569"
                value={feedbackMessage}
                onChangeText={setFeedbackMessage}
                textAlignVertical="top"
              />

              <TouchableOpacity
                style={[s.fbSubmitBtn, feedbackSubmitting && s.fbSubmitBtnDisabled]}
                onPress={handleFeedbackSubmit}
                disabled={feedbackSubmitting}
              >
                {feedbackSubmitting ? (
                  <ActivityIndicator size="small" color="#fff" />
                ) : (
                  <>
                    <Ionicons name="send" size={16} color="#fff" />
                    <Text style={s.fbSubmitTxt}>Submit Feedback</Text>
                  </>
                )}
              </TouchableOpacity>
            </View>
          ) : (
            <TouchableOpacity style={s.fbBtn} onPress={() => setShowFeedbackForm(true)}>
              <Ionicons name="flag-outline" size={18} color="#f59e0b" />
              <Text style={s.fbBtnTxt}>Report Issue / Suggest Correction</Text>
            </TouchableOpacity>
          )}

          <View style={s.fbNotice}>
            <Ionicons name="information-circle-outline" size={14} color="#64748b" />
            <Text style={s.fbNoticeTxt}>
              Think the AI got something wrong? Submit a correction — your feedback helps improve grading accuracy. All suggestions are reviewed by our admin team.
            </Text>
          </View>

          <View style={{ flexDirection: 'row', gap: 10, marginTop: 8 }}>
            <TouchableOpacity style={s.retryBtn} onPress={() => { setResponse(''); setResult(null); setFeedbackSubmitted(false); setShowFeedbackForm(false); setFeedbackMessage(''); setTimeRemaining(scenario?.time_limit || MINI_TIME); setPhase('start'); }}>
              <Ionicons name="refresh" size={18} color="#000" />
              <Text style={s.retryTxt}>Try Again</Text>
            </TouchableOpacity>

            {getNextScenario() && (
              <TouchableOpacity style={s.nextBtn} onPress={goToNextScenario}>
                <Text style={s.nextTxt}>Next Scenario</Text>
                <Ionicons name="arrow-forward" size={18} color="#fff" />
              </TouchableOpacity>
            )}
          </View>

          <View style={{ height: 80 }} />
        </ScrollView>
      </SafeAreaView>
    );
  }

  // RESPOND PHASE
  const isTimeLow = timeRemaining < 120;

  return (
    <SafeAreaView style={s.safe}>
      <KeyboardAvoidingView style={{ flex: 1 }} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
        <ScrollView style={s.scroll} contentContainerStyle={s.content}>
          {/* Timer bar */}
          <View style={s.timerBar}>
            <TouchableOpacity style={s.backBtn} onPress={() => {
              showAlert('Leave Scenario?', 'Your progress will be lost.', [
                { text: 'Cancel', style: 'cancel' },
                { text: 'Leave', onPress: () => { stopTTS(); if (timerRef.current) clearInterval(timerRef.current); router.back(); } }
              ]);
            }}>
              <Ionicons name="arrow-back" size={20} color="#60a5fa" />
            </TouchableOpacity>
            <View style={[s.timerPill, isTimeLow && s.timerPillLow]}>
              <Ionicons name="time-outline" size={14} color={isTimeLow ? '#ef4444' : '#fbbf24'} />
              <Text style={[s.timerTxt, isTimeLow && s.timerTxtLow]}>{formatTime(timeRemaining)}</Text>
            </View>
            <TouchableOpacity onPress={() => toggleTTS(scenario?.content || '')} style={s.ttsBtn}>
              <Ionicons name={isTTSPlaying ? 'stop' : 'volume-high'} size={20} color="#60a5fa" />
            </TouchableOpacity>
          </View>

          {/* Scenario */}
          <Text style={s.respondTitle}>{scenario?.title}</Text>
          <View style={s.scenarioBox}>
            <Text style={s.scenarioTxt}>{scenario?.content}</Text>
          </View>

          {/* Instructions */}
          <View style={s.instructBox}>
            <Ionicons name="information-circle-outline" size={14} color="#60a5fa" />
            <Text style={s.instructTxt}>Outline your investigative steps in 8-12 bullet points using proper prioritization.</Text>
          </View>

          {/* Response area */}
          <TextInput
            style={s.textArea}
            multiline
            placeholder={"1. Ensure officer safety and render aid...\n2. Broadcast flash message with suspect description...\n3. Establish inner/outer perimeter...\n4. Separate and identify witnesses...\n..."}
            placeholderTextColor="#475569"
            value={response}
            onChangeText={setResponse}
            textAlignVertical="top"
          />

          {/* Submit */}
          <TouchableOpacity
            style={[s.submitBtn, !response.trim() && s.submitDisabled]}
            onPress={() => handleSubmit(false)}
            disabled={!response.trim()}
          >
            <Ionicons name="send" size={18} color={response.trim() ? '#fff' : '#64748b'} />
            <Text style={[s.submitTxt, !response.trim() && s.submitTxtDisabled]}>Submit Response</Text>
          </TouchableOpacity>

          <View style={{ height: 80 }} />
        </ScrollView>
      </KeyboardAvoidingView>

      {/* Bot 9165 */}
      <DetectiveBotBubble onPress={() => setChatVisible(true)} hintCount={hintCount} />
      <ChatOverlay
        visible={chatVisible}
        onClose={() => setChatVisible(false)}
        questionId={scenario?.question_id || scenarioId!}
        userCurrentResponse={response}
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
  loadingSub: { color: '#64748b', marginTop: 4, fontSize: 12 },

  backBtn: { flexDirection: 'row', alignItems: 'center', gap: 6, marginBottom: 8 },
  backTxt: { color: '#60a5fa', fontSize: 15, fontWeight: '600' },

  // Start phase
  startCard: { backgroundColor: '#1e293b', borderRadius: 16, padding: 20, alignItems: 'center', borderWidth: 1, borderColor: '#334155' },
  typeBadge: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#1e3a5f', paddingHorizontal: 12, paddingVertical: 4, borderRadius: 14, gap: 4, marginBottom: 12 },
  typeTxt: { color: '#60a5fa', fontSize: 11, fontWeight: '700' },
  startTitle: { fontSize: 20, fontWeight: '800', color: '#f1f5f9', textAlign: 'center', marginBottom: 10 },
  startDesc: { fontSize: 13, color: '#cbd5e1', textAlign: 'center', lineHeight: 20, marginBottom: 8 },
  startTip: { fontSize: 12, color: '#fbbf24', textAlign: 'center', lineHeight: 18, backgroundColor: 'rgba(251,191,36,0.1)', padding: 10, borderRadius: 8, marginBottom: 16 },
  infoRow: { flexDirection: 'row', gap: 8, marginBottom: 20, flexWrap: 'wrap', justifyContent: 'center' },
  infoBadge: { flexDirection: 'row', alignItems: 'center', gap: 4, backgroundColor: '#0f172a', paddingHorizontal: 10, paddingVertical: 6, borderRadius: 8 },
  infoTxt: { fontSize: 12, color: '#fbbf24', fontWeight: '600' },
  startBtn: { flexDirection: 'row', alignItems: 'center', gap: 8, backgroundColor: '#fbbf24', paddingHorizontal: 28, paddingVertical: 14, borderRadius: 28 },
  startBtnTxt: { fontSize: 16, fontWeight: '800', color: '#000' },

  // Timer bar
  timerBar: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: 12 },
  timerPill: { flexDirection: 'row', alignItems: 'center', gap: 4, backgroundColor: '#1e293b', paddingHorizontal: 12, paddingVertical: 6, borderRadius: 20 },
  timerPillLow: { backgroundColor: '#7f1d1d' },
  timerTxt: { fontSize: 16, fontWeight: '800', color: '#fbbf24' },
  timerTxtLow: { color: '#ef4444' },
  ttsBtn: { padding: 6 },

  // Respond phase
  respondTitle: { fontSize: 18, fontWeight: '800', color: '#f1f5f9', marginBottom: 10 },
  scenarioBox: { backgroundColor: '#1e293b', borderRadius: 12, padding: 14, marginBottom: 12, borderWidth: 1, borderColor: '#334155' },
  scenarioTxt: { fontSize: 14, color: '#cbd5e1', lineHeight: 22 },
  instructBox: { flexDirection: 'row', alignItems: 'flex-start', backgroundColor: 'rgba(96,165,250,0.1)', borderRadius: 10, padding: 10, marginBottom: 12, gap: 6 },
  instructTxt: { flex: 1, fontSize: 12, color: '#93c5fd', lineHeight: 18 },

  textArea: { backgroundColor: '#1e293b', borderRadius: 12, borderWidth: 1, borderColor: '#334155', padding: 14, fontSize: 14, color: '#f1f5f9', minHeight: 200, lineHeight: 22 },

  submitBtn: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8, backgroundColor: '#2563eb', paddingVertical: 14, borderRadius: 24, marginTop: 16 },
  submitDisabled: { backgroundColor: '#334155' },
  submitTxt: { fontSize: 15, fontWeight: '700', color: '#fff' },
  submitTxtDisabled: { color: '#64748b' },

  // Result phase
  resultTitle: { fontSize: 22, fontWeight: '800', color: '#f1f5f9', marginBottom: 16, textAlign: 'center' },
  gradeCard: { alignItems: 'center', backgroundColor: '#1e293b', borderRadius: 16, padding: 24, marginBottom: 16, borderWidth: 1, borderColor: '#334155' },
  gradeNum: { fontSize: 48, fontWeight: '900', color: '#60a5fa' },
  gradeLabel: { fontSize: 18, color: '#94a3b8', fontWeight: '600', marginTop: -4 },

  feedbackCard: { backgroundColor: '#1e293b', borderRadius: 12, padding: 14, marginBottom: 16, borderWidth: 1, borderColor: '#334155' },
  feedbackTitle: { fontSize: 15, fontWeight: '700', color: '#60a5fa', marginBottom: 10 },
  feedbackTxt: { fontSize: 13, color: '#cbd5e1', lineHeight: 22 },

  yourResponseCard: { backgroundColor: '#0f172a', borderRadius: 12, padding: 14, marginBottom: 16, borderWidth: 1, borderColor: '#1e293b' },
  yourResponseTitle: { fontSize: 13, fontWeight: '700', color: '#94a3b8', marginBottom: 6 },
  yourResponseTxt: { fontSize: 12, color: '#64748b', lineHeight: 20 },

  retryBtn: { flex: 1, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', backgroundColor: '#fbbf24', paddingHorizontal: 16, paddingVertical: 12, borderRadius: 24, gap: 8 },
  retryTxt: { fontSize: 15, fontWeight: '700', color: '#000' },
  nextBtn: { flex: 1, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', backgroundColor: '#2563eb', paddingHorizontal: 16, paddingVertical: 12, borderRadius: 24, gap: 8 },
  nextTxt: { fontSize: 15, fontWeight: '700', color: '#fff' },

  // Feedback styles
  fbBtn: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8, backgroundColor: '#1e293b', borderWidth: 1, borderColor: '#f59e0b', padding: 14, borderRadius: 12, marginTop: 16 },
  fbBtnTxt: { color: '#f59e0b', fontSize: 14, fontWeight: '600' },
  fbFormCard: { backgroundColor: '#1e293b', borderRadius: 16, padding: 16, marginTop: 16, borderWidth: 1, borderColor: '#334155' },
  fbFormHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 },
  fbFormTitle: { color: '#f1f5f9', fontSize: 16, fontWeight: '700' },
  fbLabel: { color: '#94a3b8', fontSize: 13, fontWeight: '600', marginBottom: 8, marginTop: 4 },
  fbTypeRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginBottom: 12 },
  fbTypeBtn: { paddingHorizontal: 12, paddingVertical: 8, borderRadius: 8, backgroundColor: '#0f172a', borderWidth: 1, borderColor: '#334155' },
  fbTypeBtnActive: { backgroundColor: '#1e3a8a', borderColor: '#2563eb' },
  fbTypeTxt: { color: '#94a3b8', fontSize: 12, fontWeight: '600' },
  fbTypeTxtActive: { color: '#93c5fd' },
  fbInput: { backgroundColor: '#0f172a', borderRadius: 10, borderWidth: 1, borderColor: '#334155', padding: 12, fontSize: 14, color: '#f1f5f9', minHeight: 100, lineHeight: 20, marginBottom: 12 },
  fbSubmitBtn: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8, backgroundColor: '#2563eb', paddingVertical: 12, borderRadius: 10 },
  fbSubmitBtnDisabled: { opacity: 0.6 },
  fbSubmitTxt: { color: '#fff', fontSize: 14, fontWeight: '700' },
  fbSuccessCard: { flexDirection: 'row', alignItems: 'center', gap: 10, backgroundColor: '#064e3b', borderRadius: 12, padding: 14, marginTop: 16, borderWidth: 1, borderColor: '#10b981' },
  fbSuccessTxt: { flex: 1, color: '#a7f3d0', fontSize: 13, lineHeight: 20 },
  fbNotice: { flexDirection: 'row', alignItems: 'flex-start', gap: 6, marginTop: 10, paddingHorizontal: 4 },
  fbNoticeTxt: { flex: 1, color: '#64748b', fontSize: 11, lineHeight: 16 },
});
