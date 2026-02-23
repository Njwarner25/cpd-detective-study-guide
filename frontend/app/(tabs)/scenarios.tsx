import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet, ActivityIndicator, Platform } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useAuth } from '../../contexts/AuthContext';
import { useRouter } from 'expo-router';
import { questionService } from '../../services/api';

export default function Scenarios() {
  const { sessionToken, hasPaid, isGuest } = useAuth();
  const router = useRouter();
  const [scenarios, setScenarios] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showGrading, setShowGrading] = useState(false);

  useEffect(() => { loadScenarios(); }, []);

  const loadScenarios = async () => {
    try {
      const data = await questionService.getScenarios(sessionToken || undefined);
      setScenarios(data || []);
    } catch (e) { console.error(e); }
    finally { setLoading(false); }
  };

  const startScenario = (scenario: any) => {
    if (!hasPaid && !isGuest) { router.push('/upgrade'); return; }
    router.push({ pathname: '/practice-scenario', params: { scenarioId: scenario._id || scenario.id, title: scenario.title }});
  };

  const isPremium = hasPaid;

  return (
    <SafeAreaView style={s.safe}>
      <ScrollView style={s.scroll} contentContainerStyle={s.content}>

        {/* Header */}
        <View style={s.header}>
          <View style={s.premBadge}><Ionicons name="star" size={14} color="#fbbf24" /><Text style={s.premTxt}>PREMIUM</Text></View>
          <Text style={s.title}>Detective Scenarios</Text>
          <Text style={s.subtitle}>Timed written scenarios graded using the I/O Solutions methodology</Text>
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
                The CPD Detective Part 2 written assessment is developed and scored by I/O Solutions (IOS), a national leader in public safety promotional testing. Your written responses are evaluated by trained assessors who score your answers against a checklist of Mandatory Courses of Action â essentially an answer key of the behavioral actions you should demonstrate as the responding detective.
              </Text>

              <Text style={s.gradingSectionHead}>Differentially Weighted Point System</Text>
              <Text style={s.gradingText}>
                Unlike a standard pass/fail test, I/O Solutions uses differentially weighted scoring. Not every correct action is worth the same number of points â critical investigative steps earn more than routine ones, and harmful actions can cost you points:
              </Text>
              <View style={s.pointRow}><View style={[s.pointBadge,{backgroundColor:'#166534'}]}><Text style={s.pointVal}>+2</Text></View><Text style={s.pointLabel}>Most effective â actions critical to the investigation (e.g., securing scene, requesting ET, ensuring victim safety, interviewing witnesses individually)</Text></View>
              <View style={s.pointRow}><View style={[s.pointBadge,{backgroundColor:'#854d0e'}]}><Text style={s.pointVal}>+1</Text></View><Text style={s.pointLabel}>Effective but lower priority â appropriate actions that support the investigation (e.g., canvassing area, checking POD cameras, background checks)</Text></View>
              <View style={s.pointRow}><View style={[s.pointBadge,{backgroundColor:'#64748b'}]}><Text style={s.pointVal}> 0</Text></View><Text style={s.pointLabel}>Ineffective â unnecessary, premature, or does not advance the case</Text></View>
              <View style={s.pointRow}><View style={[s.pointBadge,{backgroundColor:'#991b1b'}]}><Text style={s.pointVal}>-1</Text></View><Text style={s.pointLabel}>Counterproductive â could compromise the investigation or violate procedure</Text></View>
              <View style={s.pointRow}><View style={[s.pointBadge,{backgroundColor:'#7f1d1d'}]}><Text style={s.pointVal}>-2</Text></View><Text style={s.pointLabel}>Harmful â directly damages the case, endangers safety, or violates legal requirements</Text></View>

              <Text style={s.gradingSectionHead}>Assessor Checklist â What They Look For</Text>
              <Text style={s.gradingText}>
                Assessors are trained to evaluate your behavioral actions â what you would actually do as the responding detective, not theoretical knowledge. Your written response is compared line-by-line against the Mandatory Courses of Action checklist. Points are awarded for each required action you include and deducted for harmful ones.
              </Text>

              <Text style={s.gradingSectionHead}>Format Matters</Text>
              <Text style={s.gradingBullet}>{'\u2022'} When the question asks for a list of actions, write a numbered or bulleted list â narrative paragraphs may not be scored</Text>
              <Text style={s.gradingBullet}>{'\u2022'} When told to select a specific number of answers, selecting more than that number results in an automatic zero for that question â even if all your selections are correct</Text>
              <Text style={s.gradingBullet}>{'\u2022'} Selecting fewer than the specified number earns partial credit for correct selections</Text>
              <Text style={s.gradingBullet}>{'\u2022'} When a question asks you to explain your reasoning, you must provide a rationale or you will not receive full credit</Text>

              <Text style={s.gradingSectionHead}>How Our AI Grading Works</Text>
              <Text style={s.gradingText}>
                Our AI grading system mirrors the I/O Solutions methodology. After you submit your written response, the AI evaluates it against the same type of Mandatory Courses of Action checklist that real assessors use. You receive a point breakdown showing which +2 and +1 actions you hit, which you missed, and any actions that would have cost you points â so you know exactly where to improve.
              </Text>

              <View style={s.tipBox}>
                <Ionicons name="bulb-outline" size={16} color="#fbbf24" />
                <Text style={s.tipText}>Key mindset: "What would I actually do as the responding Detective?" Your score depends on demonstrating the right behavioral actions in the right priority order â not on how much you know.</Text>
              </View>
            </View>
          )}
        </TouchableOpacity>

        {/* ===== Scenario List ===== */}
        {loading ? (
          <ActivityIndicator size="large" color="#60a5fa" style={{marginTop:40}} />
        ) : !isPremium ? (
          <View style={s.lockOverlay}>
            <Ionicons name="lock-closed" size={48} color="#fbbf24" />
            <Text style={s.lockTitle}>Premium Content</Text>
            <Text style={s.lockDesc}>Unlock {scenarios.length} timed detective scenarios with AI grading, curveball events, and text-to-speech narration.</Text>
            <TouchableOpacity style={s.unlockBtn} onPress={() => router.push('/upgrade')}>
              <Ionicons name="star" size={16} color="#000" />
              <Text style={s.unlockTxt}>Unlock Premium â $25.00</Text>
            </TouchableOpacity>
            {scenarios.slice(0,3).map((sc: any, i: number) => (
              <View key={i} style={s.lockCard}>
                <View style={s.cardRow}>
                  <View style={[s.numBadge,s.lockNum]}><Text style={s.numTxt}>{i+1}</Text></View>
                  <View style={{flex:1}}>
                    <Text style={s.lockCardTitle}>{sc.title}</Text>
                    <Text style={s.lockCardDesc}>{sc.is_complex ? '20 min' : '15 min'} {'\u2022'} {sc.difficulty || 'Standard'}</Text>
                  </View>
                  <Ionicons name="lock-closed" size={16} color="#64748b" />
                </View>
              </View>
            ))}
            <Text style={s.moreText}>+ {Math.max(0,scenarios.length-3)} more scenarios...</Text>
          </View>
        ) : (
          <View>
            <Text style={s.sectionLabel}>{scenarios.length} Scenarios Available</Text>
            {scenarios.map((sc: any, i: number) => (
              <TouchableOpacity key={sc._id||i} style={s.card} onPress={() => startScenario(sc)} activeOpacity={0.7}>
                <View style={s.cardRow}>
                  <View style={s.numBadge}><Text style={s.numTxt}>{i+1}</Text></View>
                  <View style={{flex:1}}>
                    <Text style={s.cardTitle}>{sc.title}</Text>
                    <View style={s.tagRow}>
                      <View style={s.tag}><Ionicons name="time-outline" size={12} color="#94a3b8" /><Text style={s.tagTxt}>{sc.is_complex ? '20 min' : '15 min'}</Text></View>
                      <View style={s.tag}><Ionicons name="volume-high-outline" size={12} color="#94a3b8" /><Text style={s.tagTxt}>Audio</Text></View>
                      {sc.difficulty && <View style={[s.diffBadge,sc.difficulty==='Hard'?s.diffH:s.diffM]}><Text style={s.diffTxt}>{sc.difficulty}</Text></View>}
                    </View>
                  </View>
                  <Ionicons name="chevron-forward" size={20} color="#64748b" />
                </View>
              </TouchableOpacity>
            ))}
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
  gradingCard:{backgroundColor:'#1e293b',borderRadius:12,padding:14,marginBottom:16,borderWidth:1,borderColor:'#334155'},
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
  sectionLabel:{fontSize:14,fontWeight:'700',color:'#94a3b8',marginBottom:10},
  card:{backgroundColor:'#1e293b',borderRadius:12,padding:14,marginBottom:8},
  cardRow:{flexDirection:'row',alignItems:'center',gap:10},
  numBadge:{width:32,height:32,borderRadius:16,backgroundColor:'#1e3a5f',alignItems:'center',justifyContent:'center'},
  numTxt:{fontSize:14,fontWeight:'800',color:'#60a5fa'},
  cardTitle:{fontSize:14,fontWeight:'600',color:'#f1f5f9',marginBottom:4},
  tagRow:{flexDirection:'row',alignItems:'center',gap:6},
  tag:{flexDirection:'row',alignItems:'center',gap:3},
  tagTxt:{fontSize:11,color:'#94a3b8'},
  diffBadge:{paddingHorizontal:8,paddingVertical:2,borderRadius:6},
  diffH:{backgroundColor:'#7f1d1d'},
  diffM:{backgroundColor:'#1e3a5f'},
  diffTxt:{fontSize:11,color:'#fff',fontWeight:'600'},
  lockOverlay:{alignItems:'center',padding:20,marginTop:10},
  lockTitle:{fontSize:20,fontWeight:'800',color:'#fbbf24',marginTop:10,marginBottom:6},
  lockDesc:{fontSize:13,color:'#94a3b8',textAlign:'center',marginBottom:16,lineHeight:20},
  unlockBtn:{flexDirection:'row',alignItems:'center',backgroundColor:'#fbbf24',paddingHorizontal:24,paddingVertical:12,borderRadius:30,gap:8,marginBottom:20},
  unlockTxt:{fontSize:16,fontWeight:'800',color:'#000'},
  lockCard:{backgroundColor:'#1e293b',borderRadius:12,padding:14,marginBottom:8,opacity:0.5,width:'100%'},
  lockNum:{backgroundColor:'#334155'},
  lockCardTitle:{fontSize:14,fontWeight:'600',color:'#94a3b8',marginBottom:2},
  lockCardDesc:{fontSize:12,color:'#64748b'},
  moreText:{fontSize:13,color:'#64748b',marginTop:4},
});
