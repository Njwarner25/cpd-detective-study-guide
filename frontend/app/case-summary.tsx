import React, { useEffect, useState, useRef } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  ActivityIndicator,
  Image,
  Platform,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useAuth } from '../contexts/AuthContext';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { questionService, ttsService } from '../services/api';
import DetectiveBotBubble from '../components/DetectiveBotBubble';
import ChatOverlay from '../components/ChatOverlay';

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

type Phase = 'reading' | 'upload' | 'submitting' | 'result';

export default function CaseSummary() {
  const { sessionToken } = useAuth();
  const router = useRouter();
  const { scenarioId, title: paramTitle } = useLocalSearchParams<{ scenarioId: string; title: string }>();

  const [scenario, setScenario] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [phase, setPhase] = useState<Phase>('reading');
  const [result, setResult] = useState<any>(null);
  const [imageData, setImageData] = useState<string | null>(null);
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [isTTSPlaying, setIsTTSPlaying] = useState(false);
  const [chatVisible, setChatVisible] = useState(false);
  const [hintCount, setHintCount] = useState(0);
  const [allScenarios, setAllScenarios] = useState<any[]>([]);
  const ttsRef = useRef<any>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  useEffect(() => { loadScenario(); loadAllScenarios(); return () => stopTTS(); }, [scenarioId]);

  const loadScenario = async () => {
    try {
      const data = await questionService.getQuestion(scenarioId!, sessionToken || undefined);
      setScenario(data);
    } catch (e) { console.error('Failed to load case summary scenario:', e); }
    finally { setLoading(false); }
  };

  const loadAllScenarios = async () => {
    if (allScenarios.length > 0) return;
    try {
      const data = await questionService.getQuestions('case_summary', 'cat_case_summary', sessionToken || undefined);
      setAllScenarios(data || []);
    } catch (e) { console.error('Failed to load case summary list:', e); }
  };

  const getNextScenario = () => {
    if (allScenarios.length === 0) return null;
    const idx = allScenarios.findIndex((q: any) => q.question_id === scenarioId);
    if (idx === -1 || idx >= allScenarios.length - 1) return null;
    return allScenarios[idx + 1];
  };

  const goToNext = () => {
    const next = getNextScenario();
    if (!next) return;
    stopTTS();
    setImageData(null);
    setImageFile(null);
    setResult(null);
    setPhase('reading');
    setHintCount(0);
    router.replace({
      pathname: '/case-summary',
      params: { scenarioId: next.question_id, title: next.title },
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

  // Handle file upload (photo/screenshot of handwritten answer)
  const handleFileSelect = (event: any) => {
    const file = event.target?.files?.[0];
    if (!file) return;
    setImageFile(file);
    const reader = new FileReader();
    reader.onload = (e) => {
      setImageData(e.target?.result as string);
    };
    reader.readAsDataURL(file);
  };

  const handleUploadPress = () => {
    if (Platform.OS === 'web') {
      fileInputRef.current?.click();
    } else {
      // Mobile: use expo-image-picker
      pickImageMobile();
    }
  };

  const pickImageMobile = async () => {
    try {
      const ImagePicker = require('expo-image-picker');
      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: false,
        quality: 0.8,
        base64: true,
      });
      if (!result.canceled && result.assets[0]) {
        const asset = result.assets[0];
        setImageData(asset.uri);
      }
    } catch (e) {
      console.error('Image picker error:', e);
      showAlert('Error', 'Could not access photo library');
    }
  };

  const handleSubmit = async () => {
    if (!imageData) {
      showAlert('No Image', 'Please upload a photo of your handwritten response first.');
      return;
    }
    setPhase('submitting');
    try {
      const API_URL = process.env.EXPO_PUBLIC_BACKEND_URL || '';
      const res = await fetch(`${API_URL}/api/case-summary/grade`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${sessionToken}`,
        },
        body: JSON.stringify({
          question_id: scenarioId,
          image_data: imageData,
        }),
      });
      if (!res.ok) throw new Error('Grade request failed');
      const data = await res.json();
      setResult(data);
      setPhase('result');
    } catch (e) {
      console.error('Failed to submit case summary:', e);
      showAlert('Error', 'Failed to grade your response. Please try again.');
      setPhase('upload');
    }
  };

  if (loading) {
    return (
      <SafeAreaView style={s.safe}>
        <View style={s.centered}>
          <ActivityIndicator size="large" color="#60a5fa" />
          <Text style={s.loadingTxt}>Loading case...</Text>
        </View>
      </SafeAreaView>
    );
  }

  const scenarioText = scenario?.content || scenario?.description || '';
  const title = scenario?.title || paramTitle || 'Case Summary';

  // ======== RESULT PHASE ========
  if (phase === 'result' && result) {
    return (
      <SafeAreaView style={s.safe}>
        <ScrollView style={s.scroll} contentContainerStyle={s.content}>
          <TouchableOpacity style={s.backBtn} onPress={() => router.back()}>
            <Ionicons name="arrow-back" size={22} color="#60a5fa" />
            <Text style={s.backTxt}>Back</Text>
          </TouchableOpacity>

          {/* Score banner */}
          <View style={[s.scoreBanner, { backgroundColor: (result.score || 0) >= 70 ? '#166534' : (result.score || 0) >= 50 ? '#854d0e' : '#7f1d1d' }]}>
            <Ionicons name={(result.score || 0) >= 70 ? 'checkmark-circle' : 'alert-circle'} size={28} color="#fff" />
            <Text style={s.scoreVal}>{result.score || 0}/100</Text>
            <Text style={s.scoreLabel}>{(result.score || 0) >= 70 ? 'Strong Response' : (result.score || 0) >= 50 ? 'Needs Improvement' : 'Below Standard'}</Text>
          </View>

          {/* AI Feedback */}
          <View style={s.feedbackCard}>
            <Ionicons name="bulb-outline" size={18} color="#fbbf24" />
            <Text style={s.feedbackTitle}>AI Assessment</Text>
            <Text style={s.feedbackTxt}>{result.feedback || 'No feedback available'}</Text>
          </View>

          {/* Key facts hit/missed */}
          {result.key_facts_hit && result.key_facts_hit.length > 0 && (
            <View style={s.factSection}>
              <Text style={s.factSectionTitle}>Key Facts You Included</Text>
              {result.key_facts_hit.map((fact: string, i: number) => (
                <View key={i} style={s.factRow}>
                  <Ionicons name="checkmark-circle" size={16} color="#22c55e" />
                  <Text style={s.factTxt}>{fact}</Text>
                </View>
              ))}
            </View>
          )}
          {result.key_facts_missed && result.key_facts_missed.length > 0 && (
            <View style={s.factSection}>
              <Text style={[s.factSectionTitle, { color: '#f87171' }]}>Key Facts You Missed</Text>
              {result.key_facts_missed.map((fact: string, i: number) => (
                <View key={i} style={s.factRow}>
                  <Ionicons name="close-circle" size={16} color="#f87171" />
                  <Text style={s.factTxt}>{fact}</Text>
                </View>
              ))}
            </View>
          )}

          {/* Model answer */}
          {result.model_answer && (
            <View style={s.modelCard}>
              <Text style={s.modelTitle}>Model Summary</Text>
              <Text style={s.modelTxt}>{result.model_answer}</Text>
            </View>
          )}

          {/* Navigation */}
          <View style={s.resultActions}>
            <TouchableOpacity style={s.retryBtn} onPress={() => { setImageData(null); setImageFile(null); setResult(null); setPhase('reading'); }}>
              <Ionicons name="refresh" size={18} color="#000" />
              <Text style={s.retryTxt}>Try Again</Text>
            </TouchableOpacity>
            {getNextScenario() && (
              <TouchableOpacity style={s.nextBtn} onPress={goToNext}>
                <Text style={s.nextTxt}>Next Case</Text>
                <Ionicons name="arrow-forward" size={18} color="#fff" />
              </TouchableOpacity>
            )}
          </View>
          <View style={{ height: 80 }} />
        </ScrollView>
      </SafeAreaView>
    );
  }

  // ======== SUBMITTING ========
  if (phase === 'submitting') {
    return (
      <SafeAreaView style={s.safe}>
        <View style={s.centered}>
          <ActivityIndicator size="large" color="#60a5fa" />
          <Text style={s.loadingTxt}>Bot 9165 is reading your response...</Text>
          <Text style={[s.loadingTxt, { fontSize: 13, marginTop: 4 }]}>AI grading may take a moment</Text>
        </View>
      </SafeAreaView>
    );
  }

  // ======== READING + UPLOAD PHASES ========
  return (
    <SafeAreaView style={s.safe}>
      <ScrollView style={s.scroll} contentContainerStyle={s.content}>
        <TouchableOpacity style={s.backBtn} onPress={() => router.back()}>
          <Ionicons name="arrow-back" size={22} color="#60a5fa" />
          <Text style={s.backTxt}>Back</Text>
        </TouchableOpacity>

        {/* Header */}
        <View style={s.headerBadgeRow}>
          <View style={[s.typeBadge, { backgroundColor: '#06b6d422' }]}>
            <Ionicons name="document-text" size={12} color="#06b6d4" />
            <Text style={[s.typeTxt, { color: '#06b6d4' }]}>CASE SUMMARY</Text>
          </View>
        </View>
        <Text style={s.qTitle}>{title}</Text>

        {/* Instructions */}
        <View style={s.instrCard}>
          <Ionicons name="information-circle" size={18} color="#60a5fa" />
          <Text style={s.instrTitle}>How This Works</Text>
          <Text style={s.instrTxt}>1. Read the case reports below carefully</Text>
          <Text style={s.instrTxt}>2. On paper, write a concise factual summary as if presenting to your supervisor</Text>
          <Text style={s.instrTxt}>3. Take a clear photo or screenshot of your handwritten response</Text>
          <Text style={s.instrTxt}>4. Upload it below for AI grading</Text>
        </View>

        {/* Scenario content with TTS */}
        <View style={s.scenarioCard}>
          <View style={s.scenarioHeader}>
            <Text style={s.scenarioLabel}>Case Report</Text>
            <TouchableOpacity onPress={() => toggleTTS(scenarioText)} style={s.ttsBtn}>
              <Ionicons name={isTTSPlaying ? 'stop' : 'volume-high'} size={18} color="#60a5fa" />
            </TouchableOpacity>
          </View>
          <Text style={s.scenarioTxt}>{scenarioText}</Text>
        </View>

        {/* Ready to answer / Upload section */}
        {phase === 'reading' && (
          <TouchableOpacity style={s.readyBtn} onPress={() => setPhase('upload')}>
            <Ionicons name="create" size={18} color="#000" />
            <Text style={s.readyBtnTxt}>I've Written My Answer — Upload Photo</Text>
          </TouchableOpacity>
        )}

        {phase === 'upload' && (
          <View style={s.uploadSection}>
            <Text style={s.uploadTitle}>Upload Your Handwritten Response</Text>
            <Text style={s.uploadDesc}>Take a clear, well-lit photo of your written summary. Make sure all text is legible.</Text>

            {/* Hidden file input for web */}
            {Platform.OS === 'web' && (
              <input
                ref={fileInputRef as any}
                type="file"
                accept="image/*"
                capture="environment"
                onChange={handleFileSelect}
                style={{ display: 'none' }}
              />
            )}

            <TouchableOpacity style={s.uploadBtn} onPress={handleUploadPress}>
              <Ionicons name="camera" size={24} color="#60a5fa" />
              <Text style={s.uploadBtnTxt}>{imageData ? 'Change Photo' : 'Take Photo or Choose Image'}</Text>
            </TouchableOpacity>

            {imageData && (
              <View style={s.previewWrap}>
                <Image source={{ uri: imageData }} style={s.previewImg} resizeMode="contain" />
                <TouchableOpacity style={s.removeBtn} onPress={() => { setImageData(null); setImageFile(null); }}>
                  <Ionicons name="close-circle" size={24} color="#f87171" />
                </TouchableOpacity>
              </View>
            )}

            <TouchableOpacity
              style={[s.submitBtn, !imageData && s.submitDisabled]}
              onPress={handleSubmit}
              disabled={!imageData}
            >
              <Ionicons name="cloud-upload" size={18} color={imageData ? '#000' : '#64748b'} />
              <Text style={[s.submitTxt, !imageData && s.submitTxtDisabled]}>Submit for Grading</Text>
            </TouchableOpacity>
          </View>
        )}

        <View style={{ height: 100 }} />
      </ScrollView>

      {/* Detective Bot */}
      {scenario && (
        <>
          <DetectiveBotBubble onPress={() => setChatVisible(true)} hintCount={hintCount} />
          <ChatOverlay
            visible={chatVisible}
            onClose={() => setChatVisible(false)}
            questionId={scenarioId!}
            userCurrentResponse="[User is writing a handwritten case summary]"
            onHintReceived={(count) => setHintCount(count)}
          />
        </>
      )}
    </SafeAreaView>
  );
}

const s = StyleSheet.create({
  safe: { flex: 1, backgroundColor: '#0a0f1a' },
  scroll: { flex: 1 },
  content: { padding: 20 },
  centered: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  loadingTxt: { color: '#94a3b8', marginTop: 12, fontSize: 15 },
  backBtn: { flexDirection: 'row', alignItems: 'center', gap: 6, marginBottom: 16 },
  backTxt: { color: '#60a5fa', fontSize: 16 },
  headerBadgeRow: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 8 },
  typeBadge: { flexDirection: 'row', alignItems: 'center', gap: 4, paddingHorizontal: 10, paddingVertical: 4, borderRadius: 12 },
  typeTxt: { fontSize: 11, fontWeight: '700', letterSpacing: 0.5 },
  qTitle: { color: '#f1f5f9', fontSize: 20, fontWeight: '700', marginBottom: 16 },
  instrCard: { backgroundColor: '#1e293b', borderRadius: 12, padding: 16, marginBottom: 16, borderLeftWidth: 3, borderLeftColor: '#60a5fa' },
  instrTitle: { color: '#f1f5f9', fontSize: 15, fontWeight: '700', marginBottom: 8, marginLeft: 4 },
  instrTxt: { color: '#cbd5e1', fontSize: 14, lineHeight: 22, marginLeft: 4 },
  scenarioCard: { backgroundColor: '#1e293b', borderRadius: 12, padding: 16, marginBottom: 16 },
  scenarioHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 },
  scenarioLabel: { color: '#60a5fa', fontSize: 13, fontWeight: '700', letterSpacing: 0.5, textTransform: 'uppercase' },
  ttsBtn: { padding: 6 },
  scenarioTxt: { color: '#e2e8f0', fontSize: 15, lineHeight: 24 },
  readyBtn: { backgroundColor: '#60a5fa', borderRadius: 12, padding: 16, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8, marginTop: 8 },
  readyBtnTxt: { color: '#000', fontSize: 16, fontWeight: '700' },
  uploadSection: { backgroundColor: '#1e293b', borderRadius: 12, padding: 16, marginTop: 8 },
  uploadTitle: { color: '#f1f5f9', fontSize: 17, fontWeight: '700', marginBottom: 6 },
  uploadDesc: { color: '#94a3b8', fontSize: 14, lineHeight: 20, marginBottom: 16 },
  uploadBtn: { backgroundColor: '#0f172a', borderWidth: 2, borderColor: '#334155', borderStyle: 'dashed', borderRadius: 12, padding: 24, alignItems: 'center', justifyContent: 'center', gap: 8, marginBottom: 16 },
  uploadBtnTxt: { color: '#60a5fa', fontSize: 15, fontWeight: '600' },
  previewWrap: { position: 'relative', marginBottom: 16, borderRadius: 12, overflow: 'hidden' },
  previewImg: { width: '100%', height: 300, borderRadius: 12, backgroundColor: '#0f172a' },
  removeBtn: { position: 'absolute', top: 8, right: 8 },
  submitBtn: { backgroundColor: '#60a5fa', borderRadius: 12, padding: 16, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8 },
  submitDisabled: { backgroundColor: '#334155' },
  submitTxt: { color: '#000', fontSize: 16, fontWeight: '700' },
  submitTxtDisabled: { color: '#64748b' },
  scoreBanner: { borderRadius: 16, padding: 20, alignItems: 'center', marginBottom: 16, gap: 6 },
  scoreVal: { color: '#fff', fontSize: 36, fontWeight: '800' },
  scoreLabel: { color: '#ffffffcc', fontSize: 15, fontWeight: '600' },
  feedbackCard: { backgroundColor: '#1e293b', borderRadius: 12, padding: 16, marginBottom: 16, borderLeftWidth: 3, borderLeftColor: '#fbbf24' },
  feedbackTitle: { color: '#fbbf24', fontSize: 15, fontWeight: '700', marginBottom: 8, marginLeft: 4 },
  feedbackTxt: { color: '#e2e8f0', fontSize: 14, lineHeight: 22 },
  factSection: { backgroundColor: '#1e293b', borderRadius: 12, padding: 16, marginBottom: 12 },
  factSectionTitle: { color: '#22c55e', fontSize: 14, fontWeight: '700', marginBottom: 10 },
  factRow: { flexDirection: 'row', alignItems: 'flex-start', gap: 8, marginBottom: 6 },
  factTxt: { color: '#e2e8f0', fontSize: 14, lineHeight: 20, flex: 1 },
  modelCard: { backgroundColor: '#0f172a', borderRadius: 12, padding: 16, marginBottom: 16, borderWidth: 1, borderColor: '#334155' },
  modelTitle: { color: '#60a5fa', fontSize: 14, fontWeight: '700', marginBottom: 8 },
  modelTxt: { color: '#cbd5e1', fontSize: 14, lineHeight: 22 },
  resultActions: { flexDirection: 'row', gap: 12, marginTop: 8 },
  retryBtn: { flex: 1, backgroundColor: '#fbbf24', borderRadius: 12, padding: 14, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 6 },
  retryTxt: { color: '#000', fontSize: 15, fontWeight: '700' },
  nextBtn: { flex: 1, backgroundColor: '#60a5fa', borderRadius: 12, padding: 14, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 6 },
  nextTxt: { color: '#fff', fontSize: 15, fontWeight: '700' },
});
