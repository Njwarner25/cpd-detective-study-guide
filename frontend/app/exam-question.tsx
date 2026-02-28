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
import { questionService, examService, ttsService } from '../services/api';
import DetectiveBotBubble from '../components/DetectiveBotBubble';
import ChatOverlay from '../components/ChatOverlay';

type Phase = 'loading' | 'answering' | 'submitting' | 'result';

const TYPE_CONFIG: Record<string, { icon: string; color: string; label: string; prompt: string }> = {
  most_appropriate: { icon: 'checkmark-circle', color: '#22c55e', label: 'MOST APPROPRIATE', prompt: 'Select the MOST appropriate action' },
  least_appropriate: { icon: 'alert-circle', color: '#f87171', label: 'LEAST APPROPRIATE', prompt: 'Select the LEAST appropriate action' },
  legal_trap: { icon: 'warning', color: '#fbbf24', label: 'LEGAL TRAP', prompt: 'Select the correct answer' },
  digital_evidence: { icon: 'phone-portrait', color: '#60a5fa', label: 'DIGITAL EVIDENCE', prompt: 'Select the most appropriate action' },
};

export default function ExamQuestion() {
  const { sessionToken } = useAuth();
  const router = useRouter();
  const { questionId, title: paramTitle, questionType } = useLocalSearchParams<{ questionId: string; title: string; questionType: string }>();

  const [phase, setPhase] = useState<Phase>('loading');
  const [question, setQuestion] = useState<any>(null);
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
  const [result, setResult] = useState<any>(null);
  const [isTTSPlaying, setIsTTSPlaying] = useState(false);
  const [chatVisible, setChatVisible] = useState(false);
  const [hintCount, setHintCount] = useState(0);
  const [allQuestions, setAllQuestions] = useState<any[]>([]);
  const startTime = useRef(Date.now());
  const ttsRef = useRef<any>(null);

  const config = TYPE_CONFIG[questionType || 'most_appropriate'] || TYPE_CONFIG.most_appropriate;

  useEffect(() => { loadQuestion(); loadAllQuestions(); return () => stopTTS(); }, [questionId]);

  const loadQuestion = async () => {
    try {
      const data = await questionService.getQuestion(questionId!, sessionToken || undefined);
      setQuestion(data);
      setPhase('answering');
      startTime.current = Date.now();
    } catch (e) {
      console.error('Failed to load exam question:', e);
    }
  };

  const loadAllQuestions = async () => {
    if (allQuestions.length > 0) return;
    try {
      const type = questionType || 'most_appropriate';
      const catId = `cat_${type}`;
      const data = await questionService.getQuestions(type, catId, sessionToken || undefined);
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
    setSelectedAnswer(null);
    setResult(null);
    setPhase('loading');
    setHintCount(0);
    router.replace({
      pathname: '/exam-question',
      params: { questionId: next.question_id, title: next.title, questionType: questionType || 'most_appropriate' },
    });
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

  const handleSubmit = async () => {
    if (!selectedAnswer) return;
    setPhase('submitting');
    const timeTaken = Math.floor((Date.now() - startTime.current) / 1000);
    try {
      const data = await examService.submitAnswer(questionId!, selectedAnswer, timeTaken, sessionToken || undefined);
      setResult(data);
      setPhase('result');
    } catch (e) {
      console.error('Failed to submit answer:', e);
      setPhase('answering');
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

  if (phase === 'loading' || phase === 'submitting') {
    return (
      <SafeAreaView style={s.safe}>
        <View style={s.centered}>
          <ActivityIndicator size="large" color="#60a5fa" />
          <Text style={s.loadingTxt}>{phase === 'loading' ? 'Loading question...' : 'Grading...'}</Text>
        </View>
      </SafeAreaView>
    );
  }

  // RESULT PHASE
  if (phase === 'result' && result) {
    const options = result.option_feedback || [];
    return (
      <SafeAreaView style={s.safe}>
        <ScrollView style={s.scroll} contentContainerStyle={s.content}>
          <TouchableOpacity style={s.backBtn} onPress={() => router.back()}>
            <Ionicons name="arrow-back" size={22} color="#60a5fa" />
            <Text style={s.backTxt}>Back</Text>
          </TouchableOpacity>

          {/* Score */}
          <View style={[s.resultBanner, { backgroundColor: result.is_correct ? '#166534' : '#7f1d1d' }]}>
            <Ionicons name={result.is_correct ? 'checkmark-circle' : 'close-circle'} size={32} color="#fff" />
            <Text style={s.resultBannerTxt}>{result.is_correct ? 'Correct!' : 'Incorrect'}</Text>
            <View style={[s.ioResultBadge, { backgroundColor: getScoreBg(result.io_score) }]}>
              <Text style={[s.ioResultVal, { color: getScoreColor(result.io_score) }]}>
                {result.io_score > 0 ? '+' : ''}{result.io_score}
              </Text>
            </View>
          </View>

          {/* Scenario recap */}
          <Text style={s.scenarioRecap}>{question?.content}</Text>
          <Text style={s.questionRecap}>{question?.question}</Text>

          {/* Per-option breakdown */}
          <Text style={s.sectionHead}>Answer Breakdown</Text>
          {options.map((opt: any, i: number) => (
            <View
              key={i}
              style={[
                s.optResult,
                opt.is_correct && { borderColor: '#22c55e', borderWidth: 2 },
                opt.is_selected && !opt.is_correct && { borderColor: '#ef4444', borderWidth: 2 },
              ]}
            >
              <View style={s.optResultTop}>
                <Text style={s.optResultLabel}>{opt.label}.</Text>
                <Text style={[s.optResultTxt, opt.is_correct && { color: '#22c55e' }]}>{opt.text}</Text>
                <View style={[s.ioSmallBadge, { backgroundColor: getScoreBg(opt.io_score) }]}>
                  <Text style={[s.ioSmallVal, { color: getScoreColor(opt.io_score) }]}>
                    {opt.io_score > 0 ? '+' : ''}{opt.io_score}
                  </Text>
                </View>
              </View>
              {opt.is_correct && <Text style={s.correctTag}>Correct Answer</Text>}
              {opt.is_selected && !opt.is_correct && <Text style={s.selectedTag}>Your Answer</Text>}
            </View>
          ))}

          {/* Explanation */}
          <View style={s.explanationCard}>
            <Ionicons name="bulb-outline" size={18} color="#fbbf24" />
            <Text style={s.explanationTitle}>Explanation</Text>
            <Text style={s.explanationTxt}>{result.explanation}</Text>
            {result.reference && <Text style={s.refTxt}>{result.reference}</Text>}
          </View>

          {/* Next / Try Again */}
          <View style={s.resultActions}>
            <TouchableOpacity style={s.retryBtn} onPress={() => { setSelectedAnswer(null); setResult(null); setPhase('answering'); startTime.current = Date.now(); }}>
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

          <View style={{ height: 80 }} />
        </ScrollView>
      </SafeAreaView>
    );
  }

  // ANSWERING PHASE
  const options = question?.options || [];
  const scenarioText = question?.content || '';
  const questionText = question?.question || config.prompt;

  return (
    <SafeAreaView style={s.safe}>
      <ScrollView style={s.scroll} contentContainerStyle={s.content}>
        <TouchableOpacity style={s.backBtn} onPress={() => router.back()}>
          <Ionicons name="arrow-back" size={22} color="#60a5fa" />
          <Text style={s.backTxt}>Back</Text>
        </TouchableOpacity>

        {/* Type badge and title */}
        <View style={s.headerBadgeRow}>
          <View style={[s.typeBadge, { backgroundColor: config.color + '22' }]}>
            <Ionicons name={config.icon as any} size={12} color={config.color} />
            <Text style={[s.typeTxt, { color: config.color }]}>{config.label}</Text>
          </View>
          {question?.difficulty && (
            <View style={[s.diffBadge, question.difficulty === 'hard' ? s.diffH : s.diffM]}>
              <Text style={s.diffTxt}>{question.difficulty}</Text>
            </View>
          )}
        </View>

        <Text style={s.qTitle}>{question?.title || paramTitle}</Text>

        {/* Scenario with TTS */}
        <View style={s.scenarioCard}>
          <View style={s.scenarioHeader}>
            <Text style={s.scenarioLabel}>Scenario</Text>
            <TouchableOpacity onPress={() => toggleTTS(scenarioText + '. ' + questionText)} style={s.ttsBtn}>
              <Ionicons name={isTTSPlaying ? 'stop' : 'volume-high'} size={18} color="#60a5fa" />
            </TouchableOpacity>
          </View>
          <Text style={s.scenarioTxt}>{scenarioText}</Text>
        </View>

        {/* Question */}
        <Text style={s.questionLabel}>{questionText}</Text>

        {/* Options */}
        {options.map((opt: any, i: number) => {
          const isSelected = selectedAnswer === opt.label;
          return (
            <TouchableOpacity
              key={i}
              style={[s.optionCard, isSelected && s.optionSelected]}
              onPress={() => setSelectedAnswer(opt.label)}
              activeOpacity={0.7}
            >
              <View style={[s.optBadge, isSelected && s.optBadgeSelected]}>
                <Text style={[s.optLetter, isSelected && s.optLetterSelected]}>{opt.label}</Text>
              </View>
              <Text style={[s.optText, isSelected && s.optTextSelected]}>{opt.text}</Text>
              {isSelected && <Ionicons name="checkmark-circle" size={20} color="#60a5fa" />}
            </TouchableOpacity>
          );
        })}

        {/* Submit */}
        <TouchableOpacity
          style={[s.submitBtn, !selectedAnswer && s.submitDisabled]}
          onPress={handleSubmit}
          disabled={!selectedAnswer}
        >
          <Ionicons name="checkmark-circle" size={18} color={selectedAnswer ? '#000' : '#64748b'} />
          <Text style={[s.submitTxt, !selectedAnswer && s.submitTxtDisabled]}>Submit Answer</Text>
        </TouchableOpacity>

        <View style={{ height: 80 }} />
      </ScrollView>

      {/* Bot 9165 */}
      <DetectiveBotBubble onPress={() => setChatVisible(true)} hintCount={hintCount} />
      <ChatOverlay
        visible={chatVisible}
        onClose={() => setChatVisible(false)}
        questionId={question?.question_id || questionId!}
        userCurrentResponse={selectedAnswer ? `Selected answer: ${selectedAnswer}` : ''}
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

  backBtn: { flexDirection: 'row', alignItems: 'center', gap: 6, marginBottom: 16 },
  backTxt: { color: '#60a5fa', fontSize: 15, fontWeight: '600' },

  headerBadgeRow: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 8 },
  typeBadge: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 10, paddingVertical: 4, borderRadius: 12, gap: 4 },
  typeTxt: { fontSize: 11, fontWeight: '700' },
  diffBadge: { paddingHorizontal: 8, paddingVertical: 2, borderRadius: 6 },
  diffH: { backgroundColor: '#7f1d1d' },
  diffM: { backgroundColor: '#1e3a5f' },
  diffTxt: { fontSize: 11, color: '#fff', fontWeight: '600' },

  qTitle: { fontSize: 20, fontWeight: '800', color: '#f1f5f9', marginBottom: 12 },

  scenarioCard: { backgroundColor: '#1e293b', borderRadius: 12, padding: 14, marginBottom: 12, borderWidth: 1, borderColor: '#334155' },
  scenarioHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 },
  scenarioLabel: { fontSize: 12, fontWeight: '700', color: '#94a3b8', textTransform: 'uppercase' },
  ttsBtn: { padding: 6 },
  scenarioTxt: { fontSize: 14, color: '#cbd5e1', lineHeight: 22 },

  questionLabel: { fontSize: 16, fontWeight: '700', color: '#f1f5f9', marginBottom: 12 },

  optionCard: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#1e293b', borderRadius: 10, padding: 12, marginBottom: 8, borderWidth: 1, borderColor: '#334155', gap: 10 },
  optionSelected: { borderColor: '#2563eb', backgroundColor: '#172554' },
  optBadge: { width: 30, height: 30, borderRadius: 15, backgroundColor: '#334155', alignItems: 'center', justifyContent: 'center' },
  optBadgeSelected: { backgroundColor: '#2563eb' },
  optLetter: { fontSize: 14, fontWeight: '700', color: '#94a3b8' },
  optLetterSelected: { color: '#fff' },
  optText: { flex: 1, fontSize: 13, color: '#cbd5e1', lineHeight: 19 },
  optTextSelected: { color: '#f1f5f9' },

  submitBtn: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8, backgroundColor: '#fbbf24', paddingVertical: 12, borderRadius: 24, marginTop: 16 },
  submitDisabled: { backgroundColor: '#334155' },
  submitTxt: { fontSize: 15, fontWeight: '700', color: '#000' },
  submitTxtDisabled: { color: '#64748b' },

  // Results
  resultBanner: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 10, padding: 16, borderRadius: 12, marginBottom: 16 },
  resultBannerTxt: { fontSize: 20, fontWeight: '800', color: '#fff' },
  ioResultBadge: { paddingHorizontal: 12, paddingVertical: 4, borderRadius: 10 },
  ioResultVal: { fontSize: 18, fontWeight: '800' },

  scenarioRecap: { fontSize: 13, color: '#94a3b8', lineHeight: 20, marginBottom: 6 },
  questionRecap: { fontSize: 14, fontWeight: '600', color: '#e2e8f0', marginBottom: 14 },

  sectionHead: { fontSize: 15, fontWeight: '700', color: '#e2e8f0', marginBottom: 10 },

  optResult: { backgroundColor: '#1e293b', borderRadius: 10, padding: 12, marginBottom: 8, borderWidth: 1, borderColor: '#334155' },
  optResultTop: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  optResultLabel: { fontSize: 14, fontWeight: '800', color: '#94a3b8', width: 22 },
  optResultTxt: { flex: 1, fontSize: 13, color: '#cbd5e1', lineHeight: 19 },
  ioSmallBadge: { paddingHorizontal: 8, paddingVertical: 3, borderRadius: 8 },
  ioSmallVal: { fontSize: 13, fontWeight: '800' },
  correctTag: { fontSize: 11, fontWeight: '700', color: '#22c55e', marginTop: 4 },
  selectedTag: { fontSize: 11, fontWeight: '700', color: '#ef4444', marginTop: 4 },

  explanationCard: { backgroundColor: 'rgba(251,191,36,0.08)', borderRadius: 12, padding: 14, marginTop: 12, marginBottom: 16 },
  explanationTitle: { fontSize: 14, fontWeight: '700', color: '#fbbf24', marginTop: 4, marginBottom: 6 },
  explanationTxt: { fontSize: 13, color: '#fde68a', lineHeight: 20 },
  refTxt: { fontSize: 11, color: '#d97706', marginTop: 8, fontStyle: 'italic' },

  resultActions: { flexDirection: 'row', gap: 12, marginTop: 8 },
  retryBtn: { flex: 1, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', backgroundColor: '#fbbf24', paddingHorizontal: 16, paddingVertical: 12, borderRadius: 24, gap: 8 },
  retryTxt: { fontSize: 15, fontWeight: '700', color: '#000' },
  nextBtn: { flex: 1, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', backgroundColor: '#2563eb', paddingHorizontal: 16, paddingVertical: 12, borderRadius: 24, gap: 8 },
  nextTxt: { fontSize: 15, fontWeight: '700', color: '#fff' },
});
