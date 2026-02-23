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
  const [scenarios, setScenarios] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => { loadScenarios(); }, [sessionToken]);

  const loadScenarios = async () => {
    try {
      setLoading(true);
      const data = await questionService.getQuestions('scenario', 'cat_detective_part2', sessionToken || undefined);
      setScenarios(data || []);
    } catch (error) { console.error('Failed to load scenarios:', error); }
    finally { setLoading(false); }
  };

  const handleStartScenario = (id) => router.push({ pathname: '/practice-scenario', params: { scenarioId: id } });
  const handleUpgrade = () => router.push('/upgrade');
  const isAdmin = user?.role === 'admin';
  const canAccess = hasPaid || isAdmin;

  if (loading) {
    return (<SafeAreaView style={st.container}><View style={st.loadingBox}><ActivityIndicator size="large" color="#10b981" /><Text style={st.loadTxt}>Loading scenarios...</Text></View></SafeAreaView>);
  }

  return (
    <SafeAreaView style={st.container}>
      <ScrollView style={st.scroll} contentContainerStyle={st.scrollInner} showsVerticalScrollIndicator={false}>
        <View style={st.header}>
          <View style={st.badge}><Ionicons name="star" size={14} color="#fff" /><Text style={st.badgeTxt}>PREMIUM</Text></View>
          <Text style={st.title}>Detective Part 2 Scenarios</Text>
          <Text style={st.subtitle}>20-minute timed scenarios with AI grading{String.fromCharCode(10)}Based on I/O Solutions methodology</Text>
        </View>

        <View style={st.infoCard}>
          <View style={st.infoRow}>
            <View style={st.infoItem}><Ionicons name="time" size={20} color="#f59e0b" /><Text style={st.infoLbl}>20 min</Text><Text style={st.infoSub}>Per scenario</Text></View>
            <View style={st.divider} />
            <View style={st.infoItem}><Ionicons name="document-text" size={20} color="#3b82f6" /><Text style={st.infoLbl}>{scenarios.length}</Text><Text style={st.infoSub}>Scenarios</Text></View>
            <View style={st.divider} />
            <View style={st.infoItem}><Ionicons name="sparkles" size={20} color="#10b981" /><Text style={st.infoLbl}>AI</Text><Text style={st.infoSub}>Graded</Text></View>
            <View style={st.divider} />
            <View style={st.infoItem}><Ionicons name="volume-high" size={20} color="#8b5cf6" /><Text style={st.infoLbl}>Audio</Text><Text style={st.infoSub}>Read aloud</Text></View>
          </View>
        </View>

        {!canAccess && (
          <View style={st.lockBox}>
            <Ionicons name="lock-closed" size={48} color="#f59e0b" />
            <Text style={st.lockTitle}>Premium Content</Text>
            <Text style={st.lockDesc}>Unlock all {scenarios.length} detective scenarios with timed practice, curveball complications, and AI-powered grading using the I/O Solutions scoring matrix.</Text>
            <View style={st.features}>
              {['20-minute timed written responses','Scenarios read aloud to you','Mid-scenario curveball twists','AI grading on mandatory actions','Detailed feedback & scoring'].map((t,i)=>(
                <View key={i} style={st.featRow}><Ionicons name="checkmark-circle" size={18} color="#10b981" /><Text style={st.featTxt}>{t}</Text></View>
              ))}
            </View>
            <TouchableOpacity style={st.unlockBtn} onPress={handleUpgrade}>
              <Ionicons name="lock-open" size={20} color="#fff" /><Text style={st.unlockTxt}>Unlock Premium - $25.00</Text>
            </TouchableOpacity>
            <Text style={st.subTxt}>One-time payment. Lifetime access.</Text>
          </View>
        )}

        {canAccess && (<>
          <Text style={st.secTitle}>All Scenarios</Text>
          {scenarios.map((s, i) => (
            <TouchableOpacity key={s.question_id||i} style={st.card} onPress={()=>handleStartScenario(s.question_id)} activeOpacity={0.7}>
              <View style={st.cardRow}>
                <View style={st.num}><Text style={st.numTxt}>{i+1}</Text></View>
                <View style={st.cardBody}>
                  <Text style={st.cardTitle}>{s.title}</Text>
                  <Text style={st.cardDesc} numberOfLines={2}>{s.description||s.content||''}</Text>
                  <View style={st.meta}>
                    <View style={st.tag}><Ionicons name="time-outline" size={12} color="#94a3b8" /><Text style={st.tagTxt}>20 min</Text></View>
                    {s.difficulty&&<View style={[st.diffBadge,s.difficulty==='Hard'?st.diffH:st.diffM]}><Text style={st.diffTxt}>{s.difficulty}</Text></View>}
                    <View style={st.tag}><Ionicons name="volume-high-outline" size={12} color="#8b5cf6" /><Text style={[st.tagTxt,{color:'#8b5cf6'}]}>Audio</Text></View>
                    {s.is_complex&&<View style={st.tag}><Ionicons name="flash" size={12} color="#f59e0b" /><Text style={[st.tagTxt,{color:'#f59e0b'}]}>Curveball</Text></View>}
                  </View>
                </View>
                <Ionicons name="chevron-forward" size={20} color="#64748b" />
              </View>
            </TouchableOpacity>
          ))}
        </>)}

        {!canAccess && (<>
          <Text style={st.secTitle}>Scenario Preview</Text>
          {scenarios.map((s, i) => (
            <View key={s.question_id||i} style={st.lockCard}>
              <View style={st.cardRow}>
                <View style={[st.num,st.lockNum]}><Ionicons name="lock-closed" size={14} color="#64748b" /></View>
                <View style={st.cardBody}>
                  <Text style={st.lockCardTitle}>{s.title}</Text>
                  <Text style={st.lockCardDesc} numberOfLines={1}>{(s.description||s.content||'').substring(0,80)}...</Text>
                </View>
              </View>
            </View>
          ))}
          <TouchableOpacity style={[st.unlockBtn,{marginTop:16}]} onPress={handleUpgrade}><Ionicons name="lock-open" size={20} color="#fff" /><Text style={st.unlockTxt}>Unlock All Scenarios</Text></TouchableOpacity>
        </>)}
        <View style={{height:40}} />
      </ScrollView>
    </SafeAreaView>
  );
}

const st = StyleSheet.create({
  container:{flex:1,backgroundColor:'#0c0c0c'},scroll:{flex:1},scrollInner:{padding:20,paddingBottom:40},
  loadingBox:{flex:1,justifyContent:'center',alignItems:'center'},loadTxt:{color:'#94a3b8',marginTop:12,fontSize:15},
  header:{alignItems:'center',marginBottom:20,paddingTop:8},
  badge:{flexDirection:'row',alignItems:'center',gap:5,backgroundColor:'#f59e0b',paddingHorizontal:14,paddingVertical:6,borderRadius:20,marginBottom:12},
  badgeTxt:{color:'#fff',fontSize:12,fontWeight:'700',letterSpacing:1},
  title:{fontSize:24,fontWeight:'bold',color:'#fff',textAlign:'center',marginBottom:6},
  subtitle:{fontSize:15,color:'#94a3b8',textAlign:'center',lineHeight:22},
  infoCard:{backgroundColor:'#1e293b',borderRadius:16,padding:16,marginBottom:20},
  infoRow:{flexDirection:'row',justifyContent:'space-around',alignItems:'center'},
  infoItem:{alignItems:'center',flex:1},divider:{width:1,height:40,backgroundColor:'#334155'},
  infoLbl:{color:'#fff',fontSize:16,fontWeight:'700',marginTop:6},infoSub:{color:'#64748b',fontSize:12,marginTop:2},
  lockBox:{backgroundColor:'#1e293b',borderRadius:16,padding:24,marginBottom:24,alignItems:'center',borderWidth:1,borderColor:'rgba(245,158,11,0.2)'},
  lockTitle:{fontSize:22,fontWeight:'bold',color:'#fff',marginTop:12,marginBottom:8},
  lockDesc:{fontSize:14,color:'#94a3b8',textAlign:'center',lineHeight:22,marginBottom:16},
  features:{width:'100%',marginBottom:20},featRow:{flexDirection:'row',alignItems:'center',gap:10,marginBottom:10},
  featTxt:{color:'#e2e8f0',fontSize:14,fontWeight:'500'},
  unlockBtn:{flexDirection:'row',alignItems:'center',justifyContent:'center',gap:8,backgroundColor:'#10b981',paddingVertical:16,paddingHorizontal:24,borderRadius:12,width:'100%'},
  unlockTxt:{color:'#fff',fontSize:17,fontWeight:'700'},subTxt:{color:'#64748b',fontSize:13,marginTop:8},
  secTitle:{fontSize:18,fontWeight:'bold',color:'#fff',marginBottom:14},
  card:{backgroundColor:'#1e293b',borderRadius:14,padding:16,marginBottom:12,borderWidth:1,borderColor:'#334155'},
  cardRow:{flexDirection:'row',alignItems:'center'},
  num:{width:36,height:36,borderRadius:10,backgroundColor:'#10b981',alignItems:'center',justifyContent:'center',marginRight:14},
  numTxt:{color:'#fff',fontSize:15,fontWeight:'700'},cardBody:{flex:1},
  cardTitle:{fontSize:15,fontWeight:'600',color:'#fff',marginBottom:4},
  cardDesc:{fontSize:13,color:'#94a3b8',lineHeight:18,marginBottom:8},
  meta:{flexDirection:'row',gap:8,flexWrap:'wrap'},tag:{flexDirection:'row',alignItems:'center',gap:4},
  tagTxt:{fontSize:11,color:'#94a3b8'},diffBadge:{paddingHorizontal:8,paddingVertical:2,borderRadius:6},
  diffH:{backgroundColor:'#7f1d1d'},diffM:{backgroundColor:'#1e3a5f'},diffTxt:{fontSize:11,color:'#fff',fontWeight:'600'},
  lockCard:{backgroundColor:'#1e293b',borderRadius:14,padding:14,marginBottom:8,opacity:0.5},
  lockNum:{backgroundColor:'#334155'},lockCardTitle:{fontSize:14,fontWeight:'600',color:'#94a3b8',marginBottom:2},
  lockCardDesc:{fontSize:12,color:'#64748b'},
});
