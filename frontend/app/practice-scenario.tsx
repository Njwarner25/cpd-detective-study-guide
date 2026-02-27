import React, { useEffect, useState, useRef, useCallback } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  TextInput,
  ScrollView,
  ActivityIndicator,
  Alert,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useAuth } from '../contexts/AuthContext';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { questionService, scenarioService } from '../services/api';
import DetectiveBotBubble from '../components/DetectiveBotBubble';
import ChatOverlay from '../components/ChatOverlay';

const DEFAULT_TIME = 15 * 60; // 15 minutes for standard scenarios
const COMPLEX_TIME = 20 * 60; // 20 minutes for complex scenarios

// Cross-platform alert helper
const showAlert = (title: string, message: string, buttons?: any[]) => {
  if (Platform.OS === 'web') {
    if (buttons && buttons.length > 1) {
      const confirmBtn = buttons.find((b: any) => b.style !== 'cancel');
      const result = window.confirm(title + '\n\n' + message);
      if (result && confirmBtn && confirmBtn.onPress) confirmBtn.onPress();
    } else if (buttons && buttons.length === 1 && buttons[0].onPress) {
      window.alert(title + '\n\n' + message);
      buttons[0].onPress();
    } else {
      window.alert(title + '\n\n' + message);
    }
  } else {
    Alert.alert(title, message, buttons);
  }
};

// D.E.T.E.C.T.I.V.E.S. Framework data
const DETECTIVES_FRAMEWORK = [
  { letter: 'D', title: 'Document the Scene', desc: 'Secure, photograph, and preserve all evidence at the scene' },
  { letter: 'E', title: 'Establish Perimeter', desc: 'Set inner/outer perimeter with uniformed personnel' },
  { letter: 'T', title: 'Talk to Witnesses', desc: 'Separate, identify, and interview all witnesses individually' },
  { letter: 'E', title: 'Evidence Collection', desc: 'Tag, log, and maintain chain of custody for all evidence' },
  { letter: 'C', title: 'Communicate & Coordinate', desc: 'Notify ASA, request forensics, issue flash messages' },
  { letter: 'T', title: 'Technology & Surveillance', desc: 'Obtain security footage, LEADS/CLEAR checks, digital evidence' },
  { letter: 'I', title: 'Interrogation & Interviews', desc: 'Miranda rights, recorded interrogation, detailed statements' },
  { letter: 'V', title: 'Verify & Validate', desc: 'Cross-reference statements, confirm IDs, check alibis' },
  { letter: 'E', title: 'Examine Forensics', desc: 'Ballistics, DNA, gunshot residue, trace evidence analysis' },
  { letter: 'S', title: 'Summarize & Report', desc: 'Complete case report, felony 101, PCAD documentation' },
];

export default function PracticeScenario() {
  const { sessionToken } = useAuth();
  const router = useRouter();
  const params = useLocalSearchParams();
  const [scenario, setScenario] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [response, setResponse] = useState('');
  const [wrenchResponse, setWrenchResponse] = useState('');
  const [timeRemaining, setTimeRemaining] = useState(DEFAULT_TIME);
  const [totalTime, setTotalTime] = useState(DEFAULT_TIME);
  const [isStarted, setIsStarted] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [wrenchResult, setWrenchResult] = useState<any>(null);
  const [showStudyTip, setShowStudyTip] = useState(false);
  const [isTTSPlaying, setIsTTSPlaying] = useState(false);
  const [phase, setPhase] = useState<'start' | 'respond' | 'wrench' | 'result'>('start');
  const [chatVisible, setChatVisible] = useState(false);
  const [hintCount, setHintCount] = useState(0);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const startTimeRef = useRef<number>(0);
  const ttsRef = useRef<any>(null);

  // Check if scenario has a wrench
  const hasWrench = scenario?.answer && (() => {
    try {
      const parsed = typeof scenario.answer === 'string' ? JSON.parse(scenario.answer) : scenario.answer;
      return !!parsed?.wrench;
    } catch { return false; }
  })();

  const getWrenchData = useCallback(() => {
    if (!scenario?.answer) return null;
    try {
      const parsed = typeof scenario.answer === 'string' ? JSON.parse(scenario.answer) : scenario.answer;
      return parsed?.wrench || null;
    } catch { return null; }
  }, [scenario]);

  const getModelAnswer = useCallback(() => {
    if (!scenario?.answer) return '';
    try {
      const parsed = typeof scenario.answer === 'string' ? JSON.parse(scenario.answer) : scenario.answer;
      if (parsed?.modelAnswer && Array.isArray(parsed.modelAnswer)) {
        const sections = [
          { header: 'D - Document the Scene', keywords: ['photograph', 'crime scene tech', 'supervisor', 'scene status', 'weapons on scene', 'case report', 'felony 101', 'PCAD', 'document scene', 'document owner', 'document all civilian', 'document all statements', 'record all evidence'] },
          { header: 'E - Establish Perimeter', keywords: ['perimeter', 'canine', 'uniformed'] },
          { header: 'T - Talk to Witnesses', keywords: ['witness', 'interview', 'canvass', 'fire department', 'statement from', 'command post'] },
          { header: 'E - Evidence Collection', keywords: ['preserve', 'physical evidence', 'shell casing', 'jewelry inventory', 'chain of custody', "owner's weapon", 'stolen'] },
          { header: 'C - Communicate & Coordinate', keywords: ['asa', 'flash message', 'medical examiner', 'notify'] },
          { header: 'T - Technology & Surveillance', keywords: ['security camera', 'footage', 'leads', 'clear system', 'surveillance', 'pawn shop', 'fencing'] },
          { header: 'I - Interrogation & Interviews', keywords: ['miranda', 'electronically recorded', 'interrogation', 'apprehending officer', "suspect's statement", 'inconsistencies'] },
          { header: 'V - Verify & Validate', keywords: ['photo lineup', 'show-up', 'background check', 'consent to search', 'footwear', 'clothing'] },
          { header: 'E - Examine Forensics', keywords: ['forensic services', 'ballistics', 'gunshot residue', 'dna', 'trace evidence'] },
          { header: 'S - Summarize & Report', keywords: ['arrest report', 'trr', 'tactical response', 'chain of custody maintained', 'tagged', 'file arrest'] },
        ];
        const buckets: Record<string, string[]> = {};
        const used = new Set<number>();
        sections.forEach(sec => { buckets[sec.header] = []; });
        parsed.modelAnswer.forEach((action: string, idx: number) => {
          const lower = action.toLowerCase();
          for (const sec of sections) {
            if (sec.keywords.some((kw: string) => lower.includes(kw))) {
              buckets[sec.header].push(action);
              used.add(idx);
              return;
            }
          }
        });
        parsed.modelAnswer.forEach((action: string, idx: number) => {
          if (!used.has(idx)) buckets['S - Summarize & Report'].push(action);
        });
        let output = '';
        sections.forEach(sec => {
          if (buckets[sec.header] && buckets[sec.header].length > 0) {
            output += '**' + sec.header + '**\n';
            buckets[sec.header].forEach((item: string) => { output += '• ' + item + '\n'; });
            output += '\n';
          }
        });
        return output.trim();
      }
      return typeof scenario.answer === 'string' ? scenario.answer : JSON.stringify(scenario.answer);
    } catch {
      return scenario.answer;
    }
  }, [scenario]);

  useEffect(() => {
    loadScenario();
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
      stopTTS();
    };
  }, []);

  useEffect(() => {
    if (isStarted && phase !== 'result' && timeRemaining > 0) {
      timerRef.current = setInterval(() => {
        setTimeRemaining((prev) => {
          if (prev <= 1) {
            handleTimeUp();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [isStarted, phase]);

  const loadScenario = async () => {
    try {
      const scenarioId = params.scenarioId as string;
      const data = await questionService.getQuestion(scenarioId, sessionToken || undefined);
      setScenario(data);
      // Use time_limit from data, or default based on complexity
      const scenarioTime = data.time_limit || (data.is_complex ? COMPLEX_TIME : DEFAULT_TIME);
      setTimeRemaining(scenarioTime);
      setTotalTime(scenarioTime);
    } catch (error) {
      console.error('Failed to load scenario:', error);
      showAlert('Error', 'Failed to load scenario');
    } finally {
      setLoading(false);
    }
  };

  // ── TTS (Web Speech API for web, can extend for native) ──
  const toggleTTS = (text: string) => {
    if (Platform.OS === 'web' && 'speechSynthesis' in window) {
      if (isTTSPlaying) {
        stopTTS();
      } else {
        stopTTS();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.9;
        utterance.onend = () => setIsTTSPlaying(false);
        utterance.onerror = () => setIsTTSPlaying(false);
        ttsRef.current = utterance;
        window.speechSynthesis.speak(utterance);
        setIsTTSPlaying(true);
      }
    } else {
      showAlert('TTS Not Available', 'Text-to-speech is only available on web browsers.');
    }
  };

  const stopTTS = () => {
    if (Platform.OS === 'web' && 'speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    setIsTTSPlaying(false);
  };

  const handleStart = () => {
    setIsStarted(true);
    setPhase('respond');
    startTimeRef.current = Date.now();
    // Auto-read scenario aloud when starting
    if (scenario) {
      const text = scenario.description || scenario.content;
      if (text && Platform.OS === 'web' && 'speechSynthesis' in window) {
        stopTTS();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.9;
        utterance.onend = () => setIsTTSPlaying(false);
        utterance.onerror = () => setIsTTSPlaying(false);
        ttsRef.current = utterance;
        window.speechSynthesis.speak(utterance);
        setIsTTSPlaying(true);
      }
    }
  };

  const handleTimeUp = () => {
    if (timerRef.current) clearInterval(timerRef.current);
    if (phase === 'respond') {
      handleSubmit(true);
    } else if (phase === 'wrench') {
      handleWrenchSubmit(true);
    }
  };

  const handleSubmit = async (timeUp: boolean = false) => {
    if (submitting) return;

    if (!timeUp && response.trim().length < 50) {
      showAlert(
        'Response Too Short',
        'Please provide a more detailed response (at least 50 characters).'
      );
      return;
    }

    setSubmitting(true);
    stopTTS();
    if (timerRef.current) clearInterval(timerRef.current);

    const timeTaken = Math.round((Date.now() - startTimeRef.current) / 1000);

    try {
      const resultData = await scenarioService.submitResponse(
        scenario.question_id,
        response || 'No response provided - time expired',
        timeTaken,
        sessionToken || undefined
      );
      setResult(resultData);

      // If wrench exists, go to wrench phase; otherwise go to results
      if (hasWrench) {
        setPhase('wrench');
        // Reset timer for wrench phase (5 minutes)
        setTimeRemaining(5 * 60);
        startTimeRef.current = Date.now();
      } else {
        setPhase('result');
        setIsSubmitted(true);
      }
    } catch (error) {
      console.error('Failed to submit response:', error);
      showAlert('Error', 'Failed to submit response. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleWrenchSubmit = async (timeUp: boolean = false) => {
    if (submitting) return;

    if (!timeUp && wrenchResponse.trim().length < 30) {
      showAlert(
        'Response Too Short',
        'Please provide a more detailed response (at least 30 characters).'
      );
      return;
    }

    setSubmitting(true);
    stopTTS();
    if (timerRef.current) clearInterval(timerRef.current);

    const timeTaken = Math.round((Date.now() - startTimeRef.current) / 1000);

    try {
      // Submit wrench response with a special prefix so backend knows it's the curveball
      const wrenchData = await scenarioService.submitResponse(
        scenario.question_id,
        `[CURVEBALL RESPONSE] ${wrenchResponse || 'No response provided - time expired'}`,
        timeTaken,
        sessionToken || undefined
      );
      setWrenchResult(wrenchData);
      setPhase('result');
      setIsSubmitted(true);
    } catch (error) {
      console.error('Failed to submit wrench response:', error);
      showAlert('Error', 'Failed to submit response. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  // Render structured AI feedback with headers and bullet points
  const renderStructuredFeedback = (feedback: string) => {
    if (!feedback) return <Text style={styles.feedbackText}>No feedback available</Text>;
    
    const lines = feedback.split('\n');
    const elements: React.ReactNode[] = [];
    
    lines.forEach((line, i) => {
      const trimmed = line.trim();
      if (!trimmed) return;
      
      // H2 headers: ## Section Title
      if (trimmed.startsWith('## ')) {
        elements.push(
          <Text key={`h2-${i}`} style={styles.fbSectionHeader}>{trimmed.replace('## ', '')}</Text>
        );
      }
      // Bold headers: **D - Document the Scene**
      else if (trimmed.startsWith('**') && trimmed.endsWith('**')) {
        const content = trimmed.replace(/\*\*/g, '');
        // Color the letter for D.E.T.E.C.T.I.V.E.S. framework items
        const letterMatch = content.match(/^([A-Z]) - (.+)/);
        if (letterMatch) {
          elements.push(
            <View key={`bold-${i}`} style={styles.fbFrameworkItem}>
              <View style={styles.fbLetterBadge}>
                <Text style={styles.fbLetterText}>{letterMatch[1]}</Text>
              </View>
              <Text style={styles.fbFrameworkTitle}>{letterMatch[2]}</Text>
            </View>
          );
        } else {
          elements.push(
            <Text key={`bold-${i}`} style={styles.fbBoldText}>{content}</Text>
          );
        }
      }
      // Bullet points: • item
      else if (trimmed.startsWith('•') || trimmed.startsWith('-')) {
        const bulletContent = trimmed.replace(/^[•-]\s*/, '');
        elements.push(
          <View key={`bullet-${i}`} style={styles.fbBulletRow}>
            <Text style={styles.fbBullet}>•</Text>
            <Text style={styles.fbBulletText}>{bulletContent}</Text>
          </View>
        );
      }
      // Regular text
      else {
        elements.push(
          <Text key={`text-${i}`} style={styles.feedbackText}>{trimmed}</Text>
        );
      }
    });
    
    return <View style={styles.fbContainer}>{elements}</View>;
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getTimerColor = () => {
    if (timeRemaining <= 60) return '#ef4444';
    if (timeRemaining <= 180) return '#f59e0b';
    return '#10b981';
  };

  // Compute combined score if wrench exists
  const getCombinedScore = () => {
    if (!result) return null;
    const mainGrade = result.grade ?? 0;
    if (wrenchResult?.grade != null) {
      return Math.round(mainGrade * 0.6 + wrenchResult.grade * 0.4);
    }
    return Math.round(mainGrade);
  };

  // ── Loading ──
  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#2563eb" />
        </View>
      </SafeAreaView>
    );
  }

  // ── No scenario ──
  if (!scenario) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.header}>
          <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
            <Ionicons name="arrow-back" size={24} color="#fff" />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Scenario</Text>
          <View style={styles.backButton} />
        </View>
        <View style={styles.emptyContainer}>
          <Ionicons name="alert-circle-outline" size={64} color="#64748b" />
          <Text style={styles.emptyText}>Scenario not found</Text>
        </View>
      </SafeAreaView>
    );
  }

  // ── Result screen ──
  if (phase === 'result' && isSubmitted && result) {
    const combinedScore = getCombinedScore();
    const wrenchData = getWrenchData();
    const modelAnswer = getModelAnswer();

    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.header}>
          <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
            <Ionicons name="arrow-back" size={24} color="#fff" />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Results</Text>
          <View style={styles.backButton} />
        </View>
        <ScrollView style={styles.scrollView} contentContainerStyle={styles.scrollContent}>
          <View style={styles.resultCard}>
            {/* Combined Score */}
            <View style={styles.scoreContainer}>
              <Text style={styles.scoreLabel}>
                {hasWrench ? 'Combined Score (60% Main + 40% Curveball)' : 'Your Score'}
              </Text>
              <Text
                style={[
                  styles.scoreValue,
                  {
                    color:
                      (combinedScore ?? 0) >= 70
                        ? '#10b981'
                        : (combinedScore ?? 0) >= 50
                          ? '#f59e0b'
                          : '#ef4444',
                  },
                ]}
              >
                {combinedScore !== null ? `${combinedScore}%` : 'Pending'}
              </Text>
            </View>

            {/* Individual scores if wrench */}
            {hasWrench && wrenchResult && (
              <View style={styles.scoreBreakdown}>
                <View style={styles.scoreBreakdownItem}>
                  <Text style={styles.scoreBreakdownLabel}>Main Response</Text>
                  <Text style={styles.scoreBreakdownValue}>{Math.round(result.grade ?? 0)}%</Text>
                </View>
                <View style={styles.scoreBreakdownItem}>
                  <Text style={[styles.scoreBreakdownLabel, { color: '#F97316' }]}>Curveball</Text>
                  <Text style={[styles.scoreBreakdownValue, { color: '#F97316' }]}>
                    {Math.round(wrenchResult.grade ?? 0)}%
                  </Text>
                </View>
              </View>
            )}

            <View style={styles.divider} />

            {/* Main AI Feedback */}
            <Text style={styles.feedbackLabel}>D.E.T.E.C.T.I.V.E.S. Assessment:</Text>
            {renderStructuredFeedback(result.feedback)}

            {/* Wrench AI Feedback */}
            {wrenchResult && (
              <>
                <View style={styles.divider} />
                <Text style={[styles.feedbackLabel, { color: '#F97316' }]}>Curveball Assessment:</Text>
                {renderStructuredFeedback(wrenchResult.feedback)}
              </>
            )}

            <View style={styles.divider} />

            {/* Model Answer */}
            <Text style={styles.feedbackLabel}>Model Answer:</Text>
            {renderStructuredFeedback(typeof modelAnswer === 'string' ? modelAnswer : JSON.stringify(modelAnswer))}

            {/* Wrench Model Answer */}
            {wrenchData?.wrenchModelAnswer && (
              <>
                <View style={styles.divider} />
                <Text style={[styles.feedbackLabel, { color: '#F97316' }]}>Curveball Model Answer:</Text>
                {renderStructuredFeedback(typeof modelAnswer === 'string' ? modelAnswer : JSON.stringify(modelAnswer))}
              </>
            )}
          </View>

          <TouchableOpacity style={styles.doneButton} onPress={() => router.back()}>
            <Text style={styles.doneButtonText}>Back to Scenarios</Text>
          </TouchableOpacity>
        </ScrollView>
      </SafeAreaView>
    );
  }

  // ── Wrench/Curveball phase ──
  if (phase === 'wrench') {
    const wrenchData = getWrenchData();
    return (
      <SafeAreaView style={styles.container}>
        <KeyboardAvoidingView
          behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
          style={styles.keyboardView}
        >
          <View style={styles.header}>
            <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
              <Ionicons name="close" size={24} color="#fff" />
            </TouchableOpacity>
            <View style={[styles.timerBadge, { backgroundColor: getTimerColor() }]}>
              <Ionicons name="time" size={18} color="#fff" />
              <Text style={styles.timerText}>{formatTime(timeRemaining)}</Text>
            </View>
            <View style={styles.backButton} />
          </View>
          <ScrollView
            style={styles.scrollView}
            contentContainerStyle={styles.practiceContent}
          >
            {/* Curveball badge */}
            <View style={styles.wrenchBadgeRow}>
              <View style={styles.wrenchBadge}>
                <Ionicons name="warning" size={16} color="#fff" />
                <Text style={styles.wrenchBadgeText}>CURVEBALL</Text>
              </View>
              {/* TTS button for wrench */}
              <TouchableOpacity
                style={styles.ttsButton}
                onPress={() => toggleTTS(wrenchData?.wrenchText || '')}
              >
                <Ionicons name={isTTSPlaying ? 'stop' : 'volume-high'} size={20} color="#F97316" />
              </TouchableOpacity>
            </View>

            <View style={styles.wrenchBox}>
              <Text style={styles.scenarioLabel}>NEW DEVELOPMENT</Text>
              <Text style={styles.scenarioContent}>{wrenchData?.wrenchText}</Text>
            </View>

            {/* Show main response score */}
            {result && (
              <View style={styles.mainScorePreview}>
                <Ionicons name="checkmark-circle" size={18} color="#10b981" />
                <Text style={styles.mainScoreText}>
                  Main response submitted — Score: {Math.round(result.grade ?? 0)}%
                </Text>
              </View>
            )}

            <View style={styles.responseSection}>
              <Text style={[styles.responseLabel, { color: '#F97316' }]}>YOUR CURVEBALL RESPONSE</Text>
              <TextInput
                style={[styles.responseInput, { borderColor: '#F97316' }]}
                multiline
                placeholder="How do you handle this new development? Be thorough..."
                placeholderTextColor="#64748b"
                value={wrenchResponse}
                onChangeText={setWrenchResponse}
                textAlignVertical="top"
              />
              <Text style={styles.charCount}>{wrenchResponse.length} characters</Text>
            </View>
          </ScrollView>
          <View style={styles.submitContainer}>
            <TouchableOpacity
              style={[styles.submitButton, { backgroundColor: '#F97316' }, submitting && styles.submitButtonDisabled]}
              onPress={() => handleWrenchSubmit(false)}
              disabled={submitting}
            >
              {submitting ? (
                <ActivityIndicator color="#fff" />
              ) : (
                <>
                  <Ionicons name="send" size={20} color="#fff" />
                  <Text style={styles.submitButtonText}>Submit Curveball Response</Text>
                </>
              )}
            </TouchableOpacity>
          </View>
        </KeyboardAvoidingView>
      </SafeAreaView>
    );
  }

  // ── Start screen ──
  if (phase === 'start' && !isStarted) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.header}>
          <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
            <Ionicons name="arrow-back" size={24} color="#fff" />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Scenario Practice</Text>
          <View style={styles.backButton} />
        </View>
        <ScrollView style={styles.scrollView} contentContainerStyle={styles.scrollContent}>
          <View style={styles.startCard}>
            <View style={styles.scenarioHeader}>
              <View
                style={[
                  styles.badge,
                  styles[`badge${scenario.difficulty}` as keyof typeof styles] || styles.badgehard,
                ]}
              >
                <Text style={styles.badgeText}>{scenario.difficulty}</Text>
              </View>
              <Text style={styles.categoryBadge}>{scenario.category_name}</Text>
              {hasWrench && (
                <View style={styles.wrenchBadgeSmall}>
                  <Text style={styles.wrenchBadgeSmallText}>CURVEBALL</Text>
                </View>
              )}
            </View>
            <Text style={styles.scenarioTitle}>{scenario.title}</Text>
            <View style={styles.infoBox}>
              <Ionicons name="information-circle" size={24} color="#60a5fa" />
              <View style={styles.infoContent}>
                <Text style={styles.infoTitle}>Instructions</Text>
                <Text style={styles.infoText}>
                  {'\u2022'} You will have {Math.floor(totalTime / 60)} minutes to respond{'\n'}
                  {'\u2022'} The scenario will be read aloud when you start{'\n'}
                  {'\u2022'} Read along and provide a detailed, professional response{'\n'}
                  {'\u2022'} Graded using I/O Solutions methodology (mandatory actions, GO/ILCS citations)
                  {scenario.is_complex ? `\n\u2022 This is a complex scenario (20 min) with multi-part elements` : ''}
                  {hasWrench ? `\n\u2022 This scenario includes a curveball complication` : ''}
                </Text>
              </View>
            </View>
            <View style={styles.timerPreview}>
              <Ionicons name="time" size={32} color="#f59e0b" />
              <Text style={styles.timerPreviewText}>{formatTime(totalTime)}</Text>
            </View>

            {/* D.E.T.E.C.T.I.V.E.S. Framework */}
            {scenario.study_tip && (
              <View style={styles.studyTipContainer}>
                <TouchableOpacity
                  style={styles.studyTipHeader}
                  onPress={() => setShowStudyTip(!showStudyTip)}
                >
                  <View style={styles.studyTipHeaderLeft}>
                    <Ionicons name="bulb" size={20} color="#f59e0b" />
                    <Text style={styles.studyTipHeaderText}>D.E.T.E.C.T.I.V.E.S. Framework</Text>
                  </View>
                  <Ionicons
                    name={showStudyTip ? 'chevron-up' : 'chevron-down'}
                    size={20}
                    color="#64748b"
                  />
                </TouchableOpacity>
                {showStudyTip && (
                  <View style={styles.studyTipContent}>
                    {DETECTIVES_FRAMEWORK.map((item, index) => (
                      <View key={index} style={styles.frameworkItem}>
                        <Text style={styles.frameworkLetter}>{item.letter}</Text>
                        <View style={styles.frameworkText}>
                          <Text style={styles.frameworkTitle}>{item.title}</Text>
                          <Text style={styles.frameworkDesc}>{item.desc}</Text>
                        </View>
                      </View>
                    ))}
                  </View>
                )}
              </View>
            )}

            <TouchableOpacity style={styles.startButton} onPress={handleStart}>
              <Ionicons name="play" size={24} color="#fff" />
              <Text style={styles.startButtonText}>Start Scenario</Text>
            </TouchableOpacity>
          </View>
        </ScrollView>
      </SafeAreaView>
    );
  }

  // ── Practice/Respond screen ──
  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.keyboardView}
      >
        <View style={styles.header}>
          <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
            <Ionicons name="close" size={24} color="#fff" />
          </TouchableOpacity>
          <View style={[styles.timerBadge, { backgroundColor: getTimerColor() }]}>
            <Ionicons name="time" size={18} color="#fff" />
            <Text style={styles.timerText}>{formatTime(timeRemaining)}</Text>
          </View>
          {/* TTS button in header */}
          <TouchableOpacity
            style={styles.ttsHeaderButton}
            onPress={() => toggleTTS(scenario.description || scenario.content)}
          >
            <Ionicons name={isTTSPlaying ? 'stop' : 'volume-high'} size={22} color="#60a5fa" />
          </TouchableOpacity>
        </View>

        {/* Phase indicator */}
        <View style={styles.phaseBar}>
          <View style={[styles.phaseStep, styles.phaseActive]}>
            <Text style={styles.phaseStepText}>1. Read & Respond</Text>
          </View>
          {hasWrench && (
            <View style={styles.phaseStep}>
              <Text style={styles.phaseStepTextInactive}>2. Curveball</Text>
            </View>
          )}
          <View style={styles.phaseStep}>
            <Text style={styles.phaseStepTextInactive}>{hasWrench ? '3' : '2'}. Results</Text>
          </View>
        </View>

        <ScrollView
          style={styles.scrollView}
          contentContainerStyle={styles.practiceContent}
        >
          <View style={styles.scenarioBox}>
            <Text style={styles.scenarioLabel}>SCENARIO</Text>
            <Text style={styles.scenarioContent}>{scenario.description || scenario.content}</Text>
            {scenario.reference && <Text style={styles.reference}>{scenario.reference}</Text>}
          </View>
          <View style={styles.responseSection}>
            <Text style={styles.responseLabel}>YOUR RESPONSE</Text>
            <TextInput
              style={styles.responseInput}
              multiline
              placeholder="Type your response here. Be thorough and professional in your approach..."
              placeholderTextColor="#64748b"
              value={response}
              onChangeText={setResponse}
              textAlignVertical="top"
            />
            <Text style={styles.charCount}>{response.length} characters</Text>
          </View>
        </ScrollView>
        <View style={styles.submitContainer}>
          <TouchableOpacity
            style={[styles.submitButton, submitting && styles.submitButtonDisabled]}
            onPress={() => handleSubmit(false)}
            disabled={submitting}
          >
            {submitting ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <>
                <Ionicons name="send" size={20} color="#fff" />
                <Text style={styles.submitButtonText}>Submit Response</Text>
              </>
            )}
          </TouchableOpacity>
        </View>

      </KeyboardAvoidingView>

      <DetectiveBotBubble onPress={() => setChatVisible(true)} hintCount={hintCount} />
      <ChatOverlay
        visible={chatVisible}
        onClose={() => setChatVisible(false)}
        questionId={scenario.question_id}
        userCurrentResponse={response}
        onHintReceived={(count) => setHintCount(count)}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0c0c0c',
  },
  keyboardView: {
    flex: 1,
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
    gap: 12,
  },
  emptyText: {
    fontSize: 18,
    color: '#94a3b8',
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
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
  },
  timerBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
  },
  timerText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  ttsHeaderButton: {
    padding: 8,
    width: 40,
    alignItems: 'center',
  },
  // Phase bar
  phaseBar: {
    flexDirection: 'row',
    paddingHorizontal: 16,
    paddingBottom: 8,
    gap: 8,
  },
  phaseStep: {
    flex: 1,
    paddingVertical: 6,
    borderRadius: 6,
    backgroundColor: '#1e293b',
    alignItems: 'center',
  },
  phaseActive: {
    backgroundColor: '#2563eb',
  },
  phaseStepText: {
    color: '#fff',
    fontSize: 11,
    fontWeight: '600',
  },
  phaseStepTextInactive: {
    color: '#64748b',
    fontSize: 11,
    fontWeight: '600',
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    padding: 16,
  },
  practiceContent: {
    padding: 16,
    paddingBottom: 100,
  },
  startCard: {
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 20,
    gap: 16,
  },
  scenarioHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    flexWrap: 'wrap',
  },
  badge: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 6,
  },
  badgeeasy: {
    backgroundColor: '#10b981',
  },
  badgemedium: {
    backgroundColor: '#f59e0b',
  },
  badgehard: {
    backgroundColor: '#ef4444',
  },
  badgeText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
    textTransform: 'capitalize',
  },
  categoryBadge: {
    fontSize: 12,
    color: '#64748b',
  },
  wrenchBadgeSmall: {
    backgroundColor: '#F97316',
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 4,
  },
  wrenchBadgeSmallText: {
    color: '#fff',
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 0.5,
  },
  scenarioTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#fff',
  },
  infoBox: {
    flexDirection: 'row',
    backgroundColor: '#1e3a5f',
    borderRadius: 12,
    padding: 16,
    gap: 12,
  },
  infoContent: {
    flex: 1,
  },
  infoTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#60a5fa',
    marginBottom: 8,
  },
  infoText: {
    fontSize: 14,
    color: '#94a3b8',
    lineHeight: 22,
  },
  timerPreview: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 12,
    paddingVertical: 16,
  },
  timerPreviewText: {
    fontSize: 48,
    fontWeight: 'bold',
    color: '#f59e0b',
  },
  startButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    backgroundColor: '#2563eb',
    padding: 16,
    borderRadius: 12,
  },
  startButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
  scenarioBox: {
    backgroundColor: '#1e293b',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
  },
  scenarioLabel: {
    fontSize: 12,
    fontWeight: '600',
    color: '#60a5fa',
    marginBottom: 12,
    letterSpacing: 1,
  },
  scenarioContent: {
    fontSize: 15,
    color: '#e2e8f0',
    lineHeight: 24,
  },
  reference: {
    fontSize: 12,
    color: '#94a3b8',
    fontStyle: 'italic',
    marginTop: 12,
  },
  responseSection: {
    flex: 1,
  },
  responseLabel: {
    fontSize: 12,
    fontWeight: '600',
    color: '#10b981',
    marginBottom: 12,
    letterSpacing: 1,
  },
  responseInput: {
    backgroundColor: '#1e293b',
    borderRadius: 12,
    padding: 16,
    fontSize: 15,
    color: '#fff',
    minHeight: 200,
    borderWidth: 1,
    borderColor: '#334155',
  },
  charCount: {
    fontSize: 12,
    color: '#64748b',
    textAlign: 'right',
    marginTop: 8,
  },
  submitContainer: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    padding: 16,
    backgroundColor: '#0c0c0c',
    borderTopWidth: 1,
    borderTopColor: '#1e293b',
  },
  submitButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    backgroundColor: '#10b981',
    padding: 16,
    borderRadius: 12,
  },
  submitButtonDisabled: {
    opacity: 0.7,
  },
  submitButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  resultCard: {
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 20,
    gap: 16,
  },
  scoreContainer: {
    alignItems: 'center',
    paddingVertical: 16,
  },
  scoreLabel: {
    fontSize: 14,
    color: '#94a3b8',
    marginBottom: 8,
    textAlign: 'center',
  },
  scoreValue: {
    fontSize: 64,
    fontWeight: 'bold',
  },
  scoreBreakdown: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 32,
  },
  scoreBreakdownItem: {
    alignItems: 'center',
  },
  scoreBreakdownLabel: {
    fontSize: 12,
    color: '#94a3b8',
    marginBottom: 4,
  },
  scoreBreakdownValue: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#10b981',
  },
  divider: {
    height: 1,
    backgroundColor: '#334155',
  },
  feedbackLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#60a5fa',
    marginBottom: 8,
  },
  feedbackText: {
    fontSize: 15,
    color: '#e2e8f0',
    lineHeight: 24,
  },
  // Structured feedback styles
  fbContainer: { gap: 4 },
  fbSectionHeader: { fontSize: 17, fontWeight: '700', color: '#60a5fa', marginTop: 12, marginBottom: 4 },
  fbFrameworkItem: { flexDirection: 'row', alignItems: 'center', marginTop: 10, marginBottom: 2 },
  fbLetterBadge: { width: 28, height: 28, borderRadius: 8, backgroundColor: '#10b981', alignItems: 'center', justifyContent: 'center', marginRight: 10 },
  fbLetterText: { color: '#fff', fontSize: 14, fontWeight: '800' },
  fbFrameworkTitle: { fontSize: 15, fontWeight: '700', color: '#f1f5f9' },
  fbBoldText: { fontSize: 15, fontWeight: '700', color: '#f1f5f9', marginTop: 8, marginBottom: 2 },
  fbBulletRow: { flexDirection: 'row', paddingLeft: 8, marginTop: 3 },
  fbBullet: { fontSize: 15, color: '#10b981', marginRight: 8, lineHeight: 22 },
  fbBulletText: { fontSize: 14, color: '#e2e8f0', lineHeight: 22, flex: 1 },
  modelAnswer: {
    fontSize: 14,
    color: '#94a3b8',
    lineHeight: 22,
  },
  doneButton: {
    backgroundColor: '#2563eb',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    marginTop: 16,
  },
  doneButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  // Wrench/Curveball styles
  wrenchBadgeRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 12,
  },
  wrenchBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    backgroundColor: '#F97316',
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 8,
  },
  wrenchBadgeText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '700',
    letterSpacing: 1,
  },
  wrenchBox: {
    backgroundColor: '#1e293b',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    borderWidth: 2,
    borderColor: '#F97316',
  },
  ttsButton: {
    padding: 8,
    borderRadius: 8,
    backgroundColor: '#1e293b',
    borderWidth: 1,
    borderColor: '#F97316',
  },
  mainScorePreview: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    backgroundColor: '#1e293b',
    padding: 12,
    borderRadius: 8,
    marginBottom: 16,
  },
  mainScoreText: {
    color: '#94a3b8',
    fontSize: 13,
  },
  // Study tip / Framework styles
  studyTipContainer: {
    backgroundColor: '#1e293b',
    borderRadius: 12,
    marginBottom: 0,
    borderWidth: 1,
    borderColor: '#334155',
    overflow: 'hidden',
  },
  studyTipHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 16,
  },
  studyTipHeaderLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
  },
  studyTipHeaderText: {
    color: '#f59e0b',
    fontSize: 15,
    fontWeight: '600',
  },
  studyTipContent: {
    padding: 16,
    paddingTop: 0,
    gap: 12,
  },
  frameworkItem: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 12,
  },
  frameworkLetter: {
    width: 28,
    height: 28,
    borderRadius: 6,
    backgroundColor: '#2563eb',
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
    textAlign: 'center',
    lineHeight: 28,
    overflow: 'hidden',
  },
  frameworkText: {
    flex: 1,
  },
  frameworkTitle: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
    marginBottom: 2,
  },
  frameworkDesc: {
    color: '#94a3b8',
    fontSize: 12,
    lineHeight: 16,
  },
});

