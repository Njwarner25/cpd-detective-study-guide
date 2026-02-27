import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet, ActivityIndicator, Platform } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useAuth } from '../../contexts/AuthContext';
import { useRouter } from 'expo-router';
import { questionService } from '../../services/api';

// Section config for each exam type
const EXAM_SECTIONS = [
  { type: 'ranking', catId: 'cat_ranking', title: 'Ranking', icon: 'swap-vertical', color: '#60a5fa', desc: 'Rank actions in correct priority order', tag: 'Rank 6 items', route: '/ranking-question', paramKey: 'questionId' },
  { type: 'most_appropriate', catId: 'cat_most_appropriate', title: 'Most Appropriate', icon: 'checkmark-circle', color: '#22c55e', desc: 'Select the BEST action for the scenario', tag: '4 options', route: '/exam-question', paramKey: 'questionId' },
  { type: 'least_appropriate', catId: 'cat_least_appropriate', title: 'Least Appropriate', icon: 'alert-circle', color: '#f87171', desc: 'Select the WORST action for the scenario', tag: '4 options', route: '/exam-question', paramKey: 'questionId' },
  { type: 'legal_trap', catId: 'cat_legal_trap', title: 'Legal Trap', icon: 'warning', color: '#fbbf24', desc: 'Tricky legal and constitutional questions', tag: 'High stakes', route: '/exam-question', paramKey: 'questionId' },
  { type: 'digital_evidence', catId: 'cat_digital_evidence', title: 'Digital Evidence', icon: 'phone-portrait', color: '#a78bfa', desc: 'Digital evidence handling scenarios', tag: '4 options', route: '/exam-question', paramKey: 'questionId' },
  { type: 'mini_scenario', catId: 'cat_mini_scenario', title: 'Mini Scenarios', icon: 'document-text', color: '#fb923c', desc: 'Short written scenarios with AI grading', tag: '10 min', route: '/mini-scenario', paramKey: 'scenarioId' },
];

export default function Scenarios() {
  const { sessionToken, hasPaid, isGuest } = useAuth();
  const router = useRouter();
  const [scenarios, setScenarios] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showGrading, setShowGrading] = useState(false);
  const [showFramework, setShowFramework] = useState(false);

  // Exam sections state
  const [examData, setExamData] = useState<Record<string, any[]>>({});
  const [examLoading, setExamLoading] = useState<Record<string, boolean>>({});

  useEffect(() => {
    loadScenarios();
    EXAM_SECTIONS.forEach(sec => loadExamSection(sec.type, sec.catId));
  }, [sessionToken]);

  const loadScenarios = async () => {
    if (!sessionToken) return;
    try {
      const data = await questionService.getQuestions('scenario', 'cat_detective_part2', sessionToken || undefined);
      setScenarios(data || []);
    } catch (e) { console.error(e); }
    finally { setLoading(false); }
  };

  const loadExamSection = async (type: string, catId: string) => {
    if (!sessionToken) return;
    setExamLoading(prev => ({ ...prev, [type]: true }));
    try {
      const data = await questionService.getQuestions(type, catId, sessionToken || undefined);
      setExamData(prev => ({ ...prev, [type]: data || [] }));
    } catch (e) { console.error(e); }
    finally { setExamLoading(prev => ({ ...prev, [type]: false })); }
  };

  const startScenario = (scenario: any, index: number) => {
    if (index === 0) {
      router.push({ pathname: '/practice-scenario', params: { scenarioId: scenario.question_id, title: scenario.title } });
      return;
    }
    if (!hasPaid) { router.push('/upgrade'); return; }
    router.push({ pathname: '/practice-scenario', params: { scenarioId: scenario.question_id, title: scenario.title } });
  };

  const startExamQuestion = (question: any, section: typeof EXAM_SECTIONS[0]) => {
    if (!hasPaid) { router.push('/upgrade'); return; }
    const params: any = { title: question.title, questionType: section.type };
    params[section.paramKey] = question.question_id;
    router.push({ pathname: section.route as any, params });
  };

  const isPremium = hasPaid;

  return (
    <SafeAreaView style={s.safe}>
      <ScrollView style={s.scroll} contentContainerStyle={s.content}>

        {/* Header */}
        <View style={s.header}>
          <View style={s.premBadge}><Ionicons name="star" size={14} color="#fbbf24" /><Text style={s.premTxt}>PREMIUM</Text></View>
          <Text style={s.title}>Part 2 {'\u2014'} Detective Exam</Text>
          <Text style={s.subtitle}>I/O Solutions mixed-method exam simulation with AI grading</Text>
        </View>

        {/* ===== HOW YOU'RE GRADED ===== */}
        <TouchableOpacity style={s.gradingCard} onPress={() => setShowGrading(!showGrading)} activeOpacity={0.8}>
          <View style={s.gradingHeader}>
            <Ionicons name="school-outline" size={20} color="#60a5fa" />
            <Text style={s.gradingTitle}>How You're Graded</Text>
            <Ionicons name={showGrading ? 'chevron-up' : 'chevron-down'} size={18} color="#94a3b8" />
          </View>

          {showGrading && (
            <View style={s.gradingBody}>

              <Text style={s.gradingSectionHead}>I/O Solutions Scoring Method</Text>
              <Text style={s.gradingText}>
                The CPD Detective Part 2 written assessment is developed and scored by I/O Solutions (IOS), a national leader in public safety promotional testing. Your written responses are evaluated by trained assessors who score your answers against a checklist of Mandatory Courses of Action {'\u2014'} essentially an answer key of the behavioral actions you should demonstrate as the responding detective.
              </Text>

              <Text style={s.gradingSectionHead}>Differentially Weighted Point System</Text>
              <Text style={s.gradingText}>
                Unlike a standard pass/fail test, I/O Solutions uses differentially weighted scoring. Not every correct action is worth the same number of points {'\u2014'} critical investigative steps earn more than routine ones, and harmful actions can cost you points:
              </Text>
              <View style={s.pointRow}><View style={[s.pointBadge,{backgroundColor:'#166534'}]}><Text style={s.pointVal}>+2</Text></View><Text style={s.pointLabel}>Most effective {'\u2014'} actions critical to the investigation (e.g., securing scene, requesting ET, ensuring victim safety, interviewing witnesses individually)</Text></View>
              <View style={s.pointRow}><View style={[s.pointBadge,{backgroundColor:'#854d0e'}]}><Text style={s.pointVal}>+1</Text></View><Text style={s.pointLabel}>Effective but lower priority {'\u2014'} appropriate actions that support the investigation (e.g., canvassing area, checking POD cameras, background checks)</Text></View>
              <View style={s.pointRow}><View style={[s.pointBadge,{backgroundColor:'#64748b'}]}><Text style={s.pointVal}> 0</Text></View><Text style={s.pointLabel}>Ineffective {'\u2014'} unnecessary, premature, or does not advance the case</Text></View>
              <View style={s.pointRow}><View style={[s.pointBadge,{backgroundColor:'#991b1b'}]}><Text style={s.pointVal}>-1</Text></View><Text style={s.pointLabel}>Counterproductive {'\u2014'} could compromise the investigation or violate procedure</Text></View>
              <View style={s.pointRow}><View style={[s.pointBadge,{backgroundColor:'#7f1d1d'}]}><Text style={s.pointVal}>-2</Text></View><Text style={s.pointLabel}>Harmful {'\u2014'} directly damages the case, endangers safety, or violates legal requirements</Text></View>

              <Text style={s.gradingSectionHead}>How Our AI Grading Works</Text>
              <Text style={s.gradingText}>
                Our AI grading system mirrors the I/O Solutions methodology. After you submit your response, the AI evaluates it against the same type of Mandatory Courses of Action checklist that real assessors use. You receive a point breakdown so you know exactly where to improve.
              </Text>

              <View style={s.tipBox}>
                <Ionicons name="bulb-outline" size={16} color="#fbbf24" />
                <Text style={s.tipText}>Key mindset: "What would I actually do as the responding Detective?" Your score depends on demonstrating the right behavioral actions in the right priority order.</Text>
              </View>
            </View>
          )}
        </TouchableOpacity>

        {/* ===== R.E.A.C.T.I.O.N. Framework ===== */}
        <TouchableOpacity style={s.fwCard} onPress={() => setShowFramework(!showFramework)} activeOpacity={0.8}>
          <View style={s.gradingHeader}>
            <Ionicons name="shield-checkmark-outline" size={20} color="#60a5fa" />
            <Text style={s.gradingTitle}>R.E.A.C.T.I.O.N. Framework</Text>
            <Ionicons name={showFramework ? 'chevron-up' : 'chevron-down'} size={18} color="#94a3b8" />
          </View>

          {showFramework && (
            <View style={s.gradingBody}>
              <Text style={s.gradingText}>Use this acronym to organize your response and hit every major scoring area:</Text>
              {[
                ['R','Respond & Render Aid','Arrive safely, ensure safety, provide medical aid'],
                ['E','Establish the Scene','Secure perimeters, control entry/exit, crime scene tape'],
                ['A','Arrest/Detain & Advise','Locate suspects, Miranda if custodial, detain & advise rights'],
                ['C','Collect/Identify Witnesses','Separate witnesses, conduct interviews, written statements'],
                ['T','Take Notes & Document','Photos, video/BWC, sketches, notes, crime scene logs'],
                ['I','Inventory & Process Evidence','Collect, package, chain of custody, request ET/forensic services'],
                ['O','Obtain Legal/Consult','Search warrants, Felony Review, ASA consultation'],
                ['N','Next Steps & Notification','Case reports, notify supervisors, follow-up, court prep'],
              ].map(([letter, title, desc], i) => (
                <View key={i} style={s.fwItem}>
                  <View style={s.fwBadge}><Text style={s.fwLetter}>{letter}</Text></View>
                  <View style={{flex:1}}>
                    <Text style={s.fwTitle}>{title}</Text>
                    <Text style={s.fwDesc}>{desc}</Text>
                  </View>
                </View>
              ))}
            </View>
          )}
        </TouchableOpacity>

        {/* ===== SECTION: Full Written Scenarios (20 min) ===== */}
        <View style={s.sectionHeader}>
          <Ionicons name="create-outline" size={18} color="#60a5fa" />
          <Text style={s.sectionTitle}>Written Scenarios</Text>
        </View>
        <Text style={s.sectionDesc}>Full 20-minute timed scenarios with AI grading, audio narration, and Bot 9165 hints.</Text>

        {loading ? (
          <ActivityIndicator size="large" color="#60a5fa" style={{marginTop:20}} />
        ) : (
          <View>
            <Text style={s.sectionLabel}>{scenarios.length} Scenarios Available</Text>
            {scenarios.map((sc: any, i: number) => {
              const isFreeTrial = i === 0;
              const isLocked = !isPremium && !isFreeTrial;
              return (
                <TouchableOpacity
                  key={sc._id||i}
                  style={[s.card, isLocked && s.lockedCard]}
                  onPress={() => isLocked ? router.push('/upgrade') : startScenario(sc, i)}
                  activeOpacity={isLocked ? 0.5 : 0.7}
                >
                  <View style={s.cardRow}>
                    <View style={[s.numBadge, isLocked && s.lockNum]}>
                      <Text style={s.numTxt}>{i+1}</Text>
                    </View>
                    <View style={{flex:1}}>
                      <View style={{flexDirection:'row',alignItems:'center',gap:6,marginBottom:4}}>
                        <Text style={[s.cardTitle, isLocked && {color:'#94a3b8'}, {marginBottom:0}]}>{sc.title}</Text>
                        {isFreeTrial && !isPremium && (
                          <View style={s.freeTrialBadge}>
                            <Text style={s.freeTrialTxt}>FREE TRIAL</Text>
                          </View>
                        )}
                      </View>
                      <View style={s.tagRow}>
                        <View style={s.tag}><Ionicons name="time-outline" size={12} color="#94a3b8" /><Text style={s.tagTxt}>20 min</Text></View>
                        <View style={s.tag}><Ionicons name="volume-high-outline" size={12} color="#94a3b8" /><Text style={s.tagTxt}>Audio</Text></View>
                        <View style={s.tag}><Ionicons name="chatbubble-ellipses-outline" size={12} color="#94a3b8" /><Text style={s.tagTxt}>Bot 9165</Text></View>
                        {sc.difficulty && <View style={[s.diffBadge,sc.difficulty==='Hard'?s.diffH:s.diffM]}><Text style={s.diffTxt}>{sc.difficulty}</Text></View>}
                      </View>
                    </View>
                    {isLocked ? (
                      <Ionicons name="lock-closed" size={16} color="#64748b" />
                    ) : (
                      <Ionicons name="chevron-forward" size={20} color="#64748b" />
                    )}
                  </View>
                </TouchableOpacity>
              );
            })}
          </View>
        )}

        {/* ===== EXAM SECTIONS ===== */}
        {EXAM_SECTIONS.map((section) => {
          const questions = examData[section.type] || [];
          const isLoading = examLoading[section.type];
          const isMini = section.type === 'mini_scenario';

          return (
            <View key={section.type}>
              <View style={s.divider} />
              <View style={s.sectionHeader}>
                <Ionicons name={section.icon as any} size={18} color={section.color} />
                <Text style={s.sectionTitle}>{section.title}</Text>
              </View>
              <Text style={s.sectionDesc}>
                {section.desc}
                {isMini ? '. These shorter scenarios help you practice hitting all R.E.A.C.T.I.O.N. steps without the pressure of a full 20-minute exam.' : ''}
              </Text>

              {isLoading ? (
                <ActivityIndicator size="small" color="#60a5fa" style={{marginTop:12, marginBottom:12}} />
              ) : questions.length > 0 ? (
                <View>
                  <Text style={s.sectionLabel}>{questions.length} Questions Available</Text>
                  {questions.map((q: any, i: number) => {
                    const isLocked = !isPremium;
                    return (
                      <TouchableOpacity
                        key={q._id || q.question_id || i}
                        style={[s.card, isLocked && s.lockedCard]}
                        onPress={() => isLocked ? router.push('/upgrade') : startExamQuestion(q, section)}
                        activeOpacity={isLocked ? 0.5 : 0.7}
                      >
                        <View style={s.cardRow}>
                          <View style={[s.numBadge, isLocked && s.lockNum, {backgroundColor: section.color + '22'}]}>
                            <Ionicons name={section.icon as any} size={14} color={section.color} />
                          </View>
                          <View style={{flex:1}}>
                            <Text style={[s.cardTitle, isLocked && {color:'#94a3b8'}, {marginBottom:0}]}>{q.title}</Text>
                            <View style={s.tagRow}>
                              <View style={s.tag}><Text style={s.tagTxt}>{section.tag}</Text></View>
                              {isMini && <View style={s.tag}><Ionicons name="volume-high-outline" size={12} color="#94a3b8" /><Text style={s.tagTxt}>Audio</Text></View>}
                              {isMini && <View style={s.tag}><Ionicons name="chatbubble-ellipses-outline" size={12} color="#94a3b8" /><Text style={s.tagTxt}>Bot 9165</Text></View>}
                              {!isMini && <View style={s.tag}><Ionicons name="chatbubble-ellipses-outline" size={12} color="#94a3b8" /><Text style={s.tagTxt}>Bot 9165</Text></View>}
                              {q.difficulty && <View style={[s.diffBadge,q.difficulty==='hard'?s.diffH:s.diffM]}><Text style={s.diffTxt}>{q.difficulty}</Text></View>}
                            </View>
                          </View>
                          {isLocked ? (
                            <Ionicons name="lock-closed" size={16} color="#64748b" />
                          ) : (
                            <Ionicons name="chevron-forward" size={20} color="#64748b" />
                          )}
                        </View>
                      </TouchableOpacity>
                    );
                  })}
                </View>
              ) : (
                <Text style={s.emptyTxt}>Coming soon</Text>
              )}
            </View>
          );
        })}

        {/* Bottom unlock */}
        {!isPremium && (
          <View style={{marginTop: 16}}>
            <TouchableOpacity style={s.unlockBtn} onPress={() => router.push('/upgrade')}>
              <Ionicons name="star" size={16} color="#000" />
              <Text style={s.unlockTxt}>Unlock All Sections {'\u2014'} $25.00</Text>
            </TouchableOpacity>
          </View>
        )}

      </ScrollView>
    </SafeAreaView>
  );
}

const s = StyleSheet.create({
  safe:{flex:1,backgroundColor:'#0f172a'},
  scroll:{flex:1},
  content:{padding:16,paddingBottom:100},
  header:{marginBottom:16,alignItems:'center'},
  premBadge:{flexDirection:'row',alignItems:'center',backgroundColor:'rgba(251,191,36,0.15)',paddingHorizontal:12,paddingVertical:4,borderRadius:20,marginBottom:8},
  premTxt:{color:'#fbbf24',fontSize:12,fontWeight:'700',marginLeft:4},
  title:{fontSize:24,fontWeight:'800',color:'#f1f5f9',marginBottom:4},
  subtitle:{fontSize:13,color:'#94a3b8',textAlign:'center'},
  gradingCard:{backgroundColor:'#1e293b',borderRadius:12,padding:14,marginBottom:10,borderWidth:1,borderColor:'#334155'},
  fwCard:{backgroundColor:'#1e293b',borderRadius:12,padding:14,marginBottom:16,borderWidth:1,borderColor:'#1e3a5f'},
  gradingHeader:{flexDirection:'row',alignItems:'center',gap:8},
  gradingTitle:{flex:1,fontSize:15,fontWeight:'700',color:'#e2e8f0'},
  gradingBody:{marginTop:12},
  gradingSectionHead:{fontSize:14,fontWeight:'700',color:'#60a5fa',marginTop:14,marginBottom:4},
  gradingText:{fontSize:13,color:'#cbd5e1',lineHeight:20,marginBottom:6},
  gradingBullet:{fontSize:13,color:'#cbd5e1',lineHeight:22,paddingLeft:8},
  pointRow:{flexDirection:'row',alignItems:'flex-start',marginBottom:8,gap:8},
  pointBadge:{width:32,height:24,borderRadius:6,alignItems:'center',justifyContent:'center'},
  pointVal:{fontSize:13,fontWeight:'800',color:'#fff'},
  pointLabel:{flex:1,fontSize:12,color:'#94a3b8',lineHeight:18},
  tipBox:{flexDirection:'row',backgroundColor:'rgba(251,191,36,0.1)',borderRadius:8,padding:10,marginTop:14,gap:8,alignItems:'flex-start'},
  tipText:{flex:1,fontSize:12,color:'#fbbf24',lineHeight:18},
  fwItem:{flexDirection:'row',alignItems:'flex-start',marginBottom:8,gap:10},
  fwBadge:{width:28,height:28,borderRadius:14,backgroundColor:'#1e3a5f',alignItems:'center',justifyContent:'center'},
  fwLetter:{fontSize:14,fontWeight:'800',color:'#60a5fa'},
  fwTitle:{fontSize:13,fontWeight:'700',color:'#e2e8f0'},
  fwDesc:{fontSize:11,color:'#94a3b8',lineHeight:16},

  // Section headers
  sectionHeader:{flexDirection:'row',alignItems:'center',gap:8,marginBottom:4,marginTop:4},
  sectionTitle:{fontSize:18,fontWeight:'800',color:'#f1f5f9'},
  sectionDesc:{fontSize:12,color:'#94a3b8',lineHeight:18,marginBottom:10},
  sectionLabel:{fontSize:13,fontWeight:'700',color:'#64748b',marginBottom:8},

  // Cards
  card:{backgroundColor:'#1e293b',borderRadius:12,padding:14,marginBottom:8},
  cardRow:{flexDirection:'row',alignItems:'center',gap:10},
  numBadge:{width:32,height:32,borderRadius:16,backgroundColor:'#1e3a5f',alignItems:'center',justifyContent:'center'},
  numTxt:{fontSize:14,fontWeight:'800',color:'#60a5fa'},
  cardTitle:{fontSize:14,fontWeight:'600',color:'#f1f5f9',marginBottom:4},
  tagRow:{flexDirection:'row',alignItems:'center',gap:6,flexWrap:'wrap'},
  tag:{flexDirection:'row',alignItems:'center',gap:3},
  tagTxt:{fontSize:11,color:'#94a3b8'},
  diffBadge:{paddingHorizontal:8,paddingVertical:2,borderRadius:6},
  diffH:{backgroundColor:'#7f1d1d'},
  diffM:{backgroundColor:'#1e3a5f'},
  diffTxt:{fontSize:11,color:'#fff',fontWeight:'600'},
  unlockBtn:{flexDirection:'row',alignItems:'center',justifyContent:'center',backgroundColor:'#fbbf24',paddingHorizontal:24,paddingVertical:12,borderRadius:30,gap:8,marginTop:4,marginBottom:20},
  unlockTxt:{fontSize:16,fontWeight:'800',color:'#000'},
  lockedCard:{opacity:0.5},
  lockNum:{backgroundColor:'#334155'},
  freeTrialBadge:{backgroundColor:'#166534',paddingHorizontal:8,paddingVertical:2,borderRadius:6},
  freeTrialTxt:{fontSize:10,fontWeight:'800',color:'#4ade80'},
  divider:{height:1,backgroundColor:'#334155',marginVertical:20},
  emptyTxt:{fontSize:13,color:'#64748b',textAlign:'center',marginTop:8,marginBottom:8},
});
