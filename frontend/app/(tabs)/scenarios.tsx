import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet, ActivityIndicator, LayoutAnimation, Platform, UIManager } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useAuth } from '../../contexts/AuthContext';
import { useRouter } from 'expo-router';
import { questionService } from '../../services/api';

// Enable LayoutAnimation on Android
if (Platform.OS === 'android' && UIManager.setLayoutAnimationEnabledExperimental) {
  UIManager.setLayoutAnimationEnabledExperimental(true);
}

// Section config for each exam type
const EXAM_SECTIONS = [
  { type: 'ranking', catId: 'cat_g03_06_firearm_discharge', title: '2026 General Orders Study Guide', icon: 'book', color: '#22d3ee', desc: 'NEW — 50 ranking questions covering G03-02, G03-02-01, G03-02-03, G03-02-08, G04-02, S03-14 & G03-06. Rank 6 actions in priority order.', tag: 'Rank 6 items', route: '/ranking-question', paramKey: 'questionId' },
  { type: 'ranking', catId: 'cat_ranking', title: 'Ranking Questions', icon: 'swap-vertical', color: '#60a5fa', desc: 'Rank actions in correct priority order using I/O differential weighting.', tag: 'Rank 6 items', route: '/ranking-question', paramKey: 'questionId' },
  { type: 'most_appropriate', catId: 'cat_most_appropriate', title: 'Most Appropriate', icon: 'checkmark-circle', color: '#22c55e', desc: 'Select the BEST action for each detective scenario.', tag: '4 options', route: '/exam-question', paramKey: 'questionId' },
  { type: 'least_appropriate', catId: 'cat_least_appropriate', title: 'Least Appropriate', icon: 'alert-circle', color: '#f87171', desc: 'Select the WORST action for each detective scenario.', tag: '4 options', route: '/exam-question', paramKey: 'questionId' },
  { type: 'legal_trap', catId: 'cat_legal_trap', title: 'Legal Trap', icon: 'warning', color: '#fbbf24', desc: 'Tricky legal and constitutional questions where the obvious answer is wrong.', tag: 'High stakes', route: '/exam-question', paramKey: 'questionId' },
  { type: 'digital_evidence', catId: 'cat_digital_evidence', title: 'Digital Evidence', icon: 'phone-portrait', color: '#a78bfa', desc: 'Modern digital evidence handling and technology scenarios.', tag: '4 options', route: '/exam-question', paramKey: 'questionId' },
  { type: 'mini_scenario', catId: 'cat_mini_scenario', title: 'Mini Scenarios', icon: 'document-text', color: '#fb923c', desc: 'Short written scenarios with AI grading. Practice hitting all R.E.A.C.T.I.O.N. steps without the pressure of a full 20-minute exam.', tag: '10 min', route: '/mini-scenario', paramKey: 'scenarioId' },
];

export default function Scenarios() {
  const { sessionToken, hasPaid, isGuest } = useAuth();
  const router = useRouter();
  const [scenarios, setScenarios] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showGrading, setShowGrading] = useState(false);
  const [showFramework, setShowFramework] = useState(false);

  // Accordion state — which sections are expanded
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>({});
  const [writtenExpanded, setWrittenExpanded] = useState(false);

  // Exam sections state
  const [examData, setExamData] = useState<Record<string, any[]>>({});
  const [examLoading, setExamLoading] = useState<Record<string, boolean>>({});

  useEffect(() => {
    loadScenarios();
    EXAM_SECTIONS.forEach(sec => loadExamSection(sec.type || sec.catId, sec.type || undefined, sec.catId));
  }, [sessionToken]);

  const loadScenarios = async () => {
    if (!sessionToken) return;
    try {
      const data = await questionService.getQuestions('scenario', 'cat_detective_part2', sessionToken || undefined);
      setScenarios(data || []);
    } catch (e) { console.error(e); }
    finally { setLoading(false); }
  };

  const loadExamSection = async (key: string, type?: string, catId?: string) => {
    if (!sessionToken) return;
    setExamLoading(prev => ({ ...prev, [key]: true }));
    try {
      const data = await questionService.getQuestions(type, catId, sessionToken || undefined);
      setExamData(prev => ({ ...prev, [key]: data || [] }));
    } catch (e) { console.error(e); }
    finally { setExamLoading(prev => ({ ...prev, [key]: false })); }
  };

  const toggleSection = (key: string) => {
    LayoutAnimation.configureNext(LayoutAnimation.Presets.easeInEaseOut);
    setExpandedSections(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const toggleWritten = () => {
    LayoutAnimation.configureNext(LayoutAnimation.Presets.easeInEaseOut);
    setWrittenExpanded(prev => !prev);
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
    // For mixed-type sections, route based on the individual question's type
    const isMixed = (section as any).mixed === true;
    const route = isMixed && question.type === 'ranking' ? '/ranking-question' : section.route;
    const questionType = isMixed ? question.type : section.type;
    const paramKey = isMixed && question.type === 'ranking' ? 'questionId' : section.paramKey;
    const params: any = { title: question.title, questionType };
    params[paramKey] = question.question_id;
    if (isMixed) params.categoryId = section.catId;
    router.push({ pathname: route as any, params });
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

        {/* ===== UPDATE BANNER ===== */}
        <View style={s.updateBanner}>
          <View style={s.updateBadge}>
            <Ionicons name="sparkles" size={14} color="#fbbf24" />
            <Text style={s.updateBadgeTxt}>NEW UPDATE</Text>
          </View>
          <Text style={s.updateTitle}>2026 General Orders Study Guide</Text>
          <Text style={s.updateDesc}>
            50 brand-new ranking questions covering ALL general orders referenced in G03-06 {'\u2014'} including G03-02 (Use of Force), G03-02-01 (Force Options), G03-02-03 (Firearm Discharge), G03-02-08 (Force Review), G04-02 (Crime Scene), and S03-14 (Body Worn Cameras).
          </Text>
          <View style={s.updateFeatures}>
            <View style={s.updateFeatureRow}><Ionicons name="list" size={14} color="#22d3ee" /><Text style={s.updateFeatureTxt}>Rank 6 actions in correct priority order for each scenario</Text></View>
            <View style={s.updateFeatureRow}><Ionicons name="analytics" size={14} color="#22d3ee" /><Text style={s.updateFeatureTxt}>I/O Solutions differential scoring (+2 to -2)</Text></View>
            <View style={s.updateFeatureRow}><Ionicons name="chatbubble-ellipses" size={14} color="#22d3ee" /><Text style={s.updateFeatureTxt}>Bot 9165 AI tutor available on every question</Text></View>
            <View style={s.updateFeatureRow}><Ionicons name="volume-high" size={14} color="#22d3ee" /><Text style={s.updateFeatureTxt}>Voice readout for all scenarios</Text></View>
          </View>
        </View>

        {/* ===== HOW YOU'RE GRADED ===== */}
        <TouchableOpacity style={s.infoCard} onPress={() => setShowGrading(!showGrading)} activeOpacity={0.8}>
          <View style={s.infoHeader}>
            <Ionicons name="school-outline" size={20} color="#60a5fa" />
            <Text style={s.infoTitle}>How You're Graded</Text>
            <Ionicons name={showGrading ? 'chevron-up' : 'chevron-down'} size={18} color="#94a3b8" />
          </View>

          {showGrading && (
            <View style={s.infoBody}>
              <Text style={s.infoSectionHead}>I/O Solutions Scoring Method</Text>
              <Text style={s.infoText}>
                The CPD Detective Part 2 written assessment is developed and scored by I/O Solutions (IOS), a national leader in public safety promotional testing. Your written responses are evaluated by trained assessors who score your answers against a checklist of Mandatory Courses of Action {'\u2014'} essentially an answer key of the behavioral actions you should demonstrate as the responding detective.
              </Text>

              <Text style={s.infoSectionHead}>Differentially Weighted Point System</Text>
              <Text style={s.infoText}>
                Unlike a standard pass/fail test, I/O Solutions uses differentially weighted scoring. Not every correct action is worth the same number of points {'\u2014'} critical investigative steps earn more than routine ones, and harmful actions can cost you points:
              </Text>
              <View style={s.pointRow}><View style={[s.pointBadge,{backgroundColor:'#166534'}]}><Text style={s.pointVal}>+2</Text></View><Text style={s.pointLabel}>Most effective {'\u2014'} actions critical to the investigation</Text></View>
              <View style={s.pointRow}><View style={[s.pointBadge,{backgroundColor:'#854d0e'}]}><Text style={s.pointVal}>+1</Text></View><Text style={s.pointLabel}>Effective but lower priority {'\u2014'} appropriate supporting actions</Text></View>
              <View style={s.pointRow}><View style={[s.pointBadge,{backgroundColor:'#64748b'}]}><Text style={s.pointVal}> 0</Text></View><Text style={s.pointLabel}>Ineffective {'\u2014'} unnecessary or premature</Text></View>
              <View style={s.pointRow}><View style={[s.pointBadge,{backgroundColor:'#991b1b'}]}><Text style={s.pointVal}>-1</Text></View><Text style={s.pointLabel}>Counterproductive {'\u2014'} could compromise the investigation</Text></View>
              <View style={s.pointRow}><View style={[s.pointBadge,{backgroundColor:'#7f1d1d'}]}><Text style={s.pointVal}>-2</Text></View><Text style={s.pointLabel}>Harmful {'\u2014'} damages the case or violates legal requirements</Text></View>

              <Text style={s.infoSectionHead}>How Our AI Grading Works</Text>
              <Text style={s.infoText}>
                Our AI grading system mirrors the I/O Solutions methodology. After you submit your response, the AI evaluates it against the same type of Mandatory Courses of Action checklist that real assessors use.
              </Text>

              <View style={s.tipBox}>
                <Ionicons name="bulb-outline" size={16} color="#fbbf24" />
                <Text style={s.tipText}>Key mindset: "What would I actually do as the responding Detective?" Your score depends on demonstrating the right behavioral actions in the right priority order.</Text>
              </View>
            </View>
          )}
        </TouchableOpacity>

        {/* ===== R.E.A.C.T.I.O.N. Framework ===== */}
        <TouchableOpacity style={[s.infoCard, {borderColor:'#1e3a5f'}]} onPress={() => setShowFramework(!showFramework)} activeOpacity={0.8}>
          <View style={s.infoHeader}>
            <Ionicons name="shield-checkmark-outline" size={20} color="#60a5fa" />
            <Text style={s.infoTitle}>R.E.A.C.T.I.O.N. Framework</Text>
            <Ionicons name={showFramework ? 'chevron-up' : 'chevron-down'} size={18} color="#94a3b8" />
          </View>

          {showFramework && (
            <View style={s.infoBody}>
              <Text style={s.infoText}>Use this acronym to organize your response and hit every major scoring area:</Text>
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

        {/* ===== ACCORDION: Written Scenarios ===== */}
        <TouchableOpacity style={s.accordionHeader} onPress={toggleWritten} activeOpacity={0.7}>
          <View style={[s.accordionIcon, {backgroundColor: '#3b82f622'}]}>
            <Ionicons name="create-outline" size={20} color="#3b82f6" />
          </View>
          <View style={{flex:1}}>
            <Text style={s.accordionTitle}>Written Scenarios</Text>
            <Text style={s.accordionDesc}>Full 20-minute timed scenarios with AI grading</Text>
          </View>
          <View style={s.countBadge}>
            <Text style={s.countTxt}>{loading ? '...' : scenarios.length}</Text>
          </View>
          <Ionicons name={writtenExpanded ? 'chevron-up' : 'chevron-down'} size={20} color="#64748b" />
        </TouchableOpacity>

        {writtenExpanded && (
          <View style={s.accordionBody}>
            {loading ? (
              <ActivityIndicator size="small" color="#60a5fa" style={{marginVertical:16}} />
            ) : (
              scenarios.map((sc: any, i: number) => {
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
                          <Text style={[s.cardTitle, isLocked && {color:'#94a3b8'}, {marginBottom:0}]} numberOfLines={2}>{sc.title}</Text>
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
              })
            )}
          </View>
        )}

        {/* ===== ACCORDION: Exam Sections ===== */}
        {EXAM_SECTIONS.map((section) => {
          const sectionKey = section.type || section.catId;
          const questions = examData[sectionKey] || [];
          const isLoading = examLoading[sectionKey];
          const isExpanded = expandedSections[sectionKey] || false;
          const isMini = section.type === 'mini_scenario';
          const isMixed = (section as any).mixed === true;

          return (
            <View key={sectionKey}>
              <TouchableOpacity
                style={s.accordionHeader}
                onPress={() => toggleSection(sectionKey)}
                activeOpacity={0.7}
              >
                <View style={[s.accordionIcon, {backgroundColor: section.color + '22'}]}>
                  <Ionicons name={section.icon as any} size={20} color={section.color} />
                </View>
                <View style={{flex:1}}>
                  <Text style={s.accordionTitle}>{section.title}</Text>
                  <Text style={s.accordionDesc} numberOfLines={1}>{section.desc.split('.')[0]}</Text>
                </View>
                <View style={s.countBadge}>
                  <Text style={s.countTxt}>{isLoading ? '...' : questions.length}</Text>
                </View>
                <Ionicons name={isExpanded ? 'chevron-up' : 'chevron-down'} size={20} color="#64748b" />
              </TouchableOpacity>

              {isExpanded && (
                <View style={s.accordionBody}>
                  {isLoading ? (
                    <ActivityIndicator size="small" color="#60a5fa" style={{marginVertical:16}} />
                  ) : questions.length > 0 ? (
                    questions.map((q: any, i: number) => {
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
                              <Text style={[s.numTxt, {color: section.color}]}>{i+1}</Text>
                            </View>
                            <View style={{flex:1}}>
                              <Text style={[s.cardTitle, isLocked && {color:'#94a3b8'}]} numberOfLines={2}>{q.title}</Text>
                              <View style={s.tagRow}>
                                {isMixed ? (
                                  <View style={s.tag}><Text style={s.tagTxt}>{q.type === 'ranking' ? 'Ranking' : q.type === 'most_appropriate' ? 'Most Appropriate' : q.type === 'least_appropriate' ? 'Least Appropriate' : q.type}</Text></View>
                                ) : (
                                  <View style={s.tag}><Text style={s.tagTxt}>{section.tag}</Text></View>
                                )}
                                <View style={s.tag}><Ionicons name="chatbubble-ellipses-outline" size={12} color="#94a3b8" /><Text style={s.tagTxt}>Bot 9165</Text></View>
                                {isMini && <View style={s.tag}><Ionicons name="volume-high-outline" size={12} color="#94a3b8" /><Text style={s.tagTxt}>Audio</Text></View>}
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
                    })
                  ) : (
                    <Text style={s.emptyTxt}>Coming soon</Text>
                  )}
                </View>
              )}
            </View>
          );
        })}

        {/* Bottom unlock */}
        {!isPremium && (
          <View style={{marginTop: 20}}>
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

  // Info cards (grading, framework)
  infoCard:{backgroundColor:'#1e293b',borderRadius:12,padding:14,marginBottom:10,borderWidth:1,borderColor:'#334155'},
  infoHeader:{flexDirection:'row',alignItems:'center',gap:8},
  infoTitle:{flex:1,fontSize:15,fontWeight:'700',color:'#e2e8f0'},
  infoBody:{marginTop:12},
  infoSectionHead:{fontSize:14,fontWeight:'700',color:'#60a5fa',marginTop:14,marginBottom:4},
  infoText:{fontSize:13,color:'#cbd5e1',lineHeight:20,marginBottom:6},
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

  // Accordion
  accordionHeader:{flexDirection:'row',alignItems:'center',gap:12,backgroundColor:'#1e293b',borderRadius:12,padding:14,marginTop:10,borderWidth:1,borderColor:'#334155'},
  accordionIcon:{width:40,height:40,borderRadius:10,alignItems:'center',justifyContent:'center'},
  accordionTitle:{fontSize:16,fontWeight:'700',color:'#f1f5f9'},
  accordionDesc:{fontSize:12,color:'#94a3b8',marginTop:2},
  countBadge:{backgroundColor:'#334155',paddingHorizontal:10,paddingVertical:4,borderRadius:12,marginRight:4},
  countTxt:{fontSize:13,fontWeight:'700',color:'#e2e8f0'},
  accordionBody:{paddingTop:8,paddingLeft:4,paddingRight:4},

  // Cards
  card:{backgroundColor:'#1e293b',borderRadius:10,padding:12,marginBottom:6,borderWidth:1,borderColor:'#293548'},
  cardRow:{flexDirection:'row',alignItems:'center',gap:10},
  numBadge:{width:30,height:30,borderRadius:15,backgroundColor:'#1e3a5f',alignItems:'center',justifyContent:'center'},
  numTxt:{fontSize:13,fontWeight:'800',color:'#60a5fa'},
  cardTitle:{fontSize:13,fontWeight:'600',color:'#f1f5f9',marginBottom:4},
  tagRow:{flexDirection:'row',alignItems:'center',gap:6,flexWrap:'wrap'},
  tag:{flexDirection:'row',alignItems:'center',gap:3},
  tagTxt:{fontSize:11,color:'#94a3b8'},
  unlockBtn:{flexDirection:'row',alignItems:'center',justifyContent:'center',backgroundColor:'#fbbf24',paddingHorizontal:24,paddingVertical:12,borderRadius:30,gap:8,marginTop:4,marginBottom:20},
  unlockTxt:{fontSize:16,fontWeight:'800',color:'#000'},
  lockedCard:{opacity:0.5},
  lockNum:{backgroundColor:'#334155'},
  freeTrialBadge:{backgroundColor:'#166534',paddingHorizontal:8,paddingVertical:2,borderRadius:6},
  freeTrialTxt:{fontSize:10,fontWeight:'800',color:'#4ade80'},
  emptyTxt:{fontSize:13,color:'#64748b',textAlign:'center',marginTop:8,marginBottom:8},
  diffBadge:{paddingHorizontal:8,paddingVertical:2,borderRadius:6},
  diffH:{backgroundColor:'#7f1d1d'},
  diffM:{backgroundColor:'#1e3a5f'},
  diffTxt:{fontSize:11,color:'#fff',fontWeight:'600'},

  // Update banner
  updateBanner:{backgroundColor:'#0c2d48',borderRadius:14,padding:16,marginBottom:12,borderWidth:1,borderColor:'#22d3ee44'},
  updateBadge:{flexDirection:'row',alignItems:'center',gap:4,backgroundColor:'rgba(251,191,36,0.15)',paddingHorizontal:10,paddingVertical:3,borderRadius:12,alignSelf:'flex-start',marginBottom:8},
  updateBadgeTxt:{fontSize:11,fontWeight:'800',color:'#fbbf24'},
  updateTitle:{fontSize:17,fontWeight:'800',color:'#22d3ee',marginBottom:6},
  updateDesc:{fontSize:13,color:'#cbd5e1',lineHeight:20,marginBottom:10},
  updateFeatures:{gap:6},
  updateFeatureRow:{flexDirection:'row',alignItems:'center',gap:8},
  updateFeatureTxt:{fontSize:12,color:'#94a3b8',flex:1},
});
