import React from 'react';
import { View, Text, ScrollView, StyleSheet, TouchableOpacity, Linking, Image } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';

export default function Support() {
  const router = useRouter();

  const handleOpenVenmo = () => {
    Linking.openURL('https://venmo.com/Jakari-Jones-8');
  };

  const handleOpenCashApp = () => {
    Linking.openURL('https://cash.app/$jorel1000');
  };

  const handleOpenZelle = () => {
    // Zelle doesn't have direct links, show instructions
    Linking.openURL('https://www.zellepay.com/');
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
          <Ionicons name="arrow-back" size={24} color="#fff" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Support the App</Text>
        <View style={styles.placeholder} />
      </View>

      <ScrollView style={styles.scrollView} showsVerticalScrollIndicator={false}>
        {/* Heart Icon */}
        <View style={styles.heroSection}>
          <View style={styles.heartContainer}>
            <Ionicons name="heart" size={64} color="#ef4444" />
          </View>
          <Text style={styles.heroTitle}>Support Our Mission</Text>
        </View>

        {/* Mission Statement */}
        <View style={styles.missionCard}>
          <View style={styles.missionHeader}>
            <Ionicons name="shield-checkmark" size={24} color="#3b82f6" />
            <Text style={styles.missionTitle}>Our Goal</Text>
          </View>
          <Text style={styles.missionText}>
            This app was created to help aspiring CPD detectives prepare for their exam 
            <Text style={styles.boldText}> without breaking the bank</Text>. 
            Other study materials can cost hundreds of dollars — we believe quality preparation 
            should be accessible to everyone.
          </Text>
        </View>

        {/* Optional Notice */}
        <View style={styles.optionalNotice}>
          <Ionicons name="information-circle" size={20} color="#fbbf24" />
          <Text style={styles.optionalText}>
            Donations are <Text style={styles.boldYellow}>100% optional</Text>. 
            The app is free and will always remain free. Your success is our reward!
          </Text>
        </View>

        {/* Donation Options */}
        <View style={styles.donationSection}>
          <Text style={styles.sectionTitle}>Ways to Support</Text>
          
          {/* Venmo */}
          <TouchableOpacity style={styles.donationCard} onPress={handleOpenVenmo}>
            <View style={[styles.donationIcon, { backgroundColor: '#008CFF' }]}>
              <Text style={styles.donationIconText}>V</Text>
            </View>
            <View style={styles.donationInfo}>
              <Text style={styles.donationName}>Venmo</Text>
              <Text style={styles.donationHandle}>@Jakari-Jones-8</Text>
            </View>
            <Ionicons name="open-outline" size={24} color="#64748b" />
          </TouchableOpacity>

          {/* Cash App */}
          <TouchableOpacity style={styles.donationCard} onPress={handleOpenCashApp}>
            <View style={[styles.donationIcon, { backgroundColor: '#00D632' }]}>
              <Text style={styles.donationIconText}>$</Text>
            </View>
            <View style={styles.donationInfo}>
              <Text style={styles.donationName}>Cash App</Text>
              <Text style={styles.donationHandle}>$jorel1000</Text>
            </View>
            <Ionicons name="open-outline" size={24} color="#64748b" />
          </TouchableOpacity>

          {/* Zelle */}
          <View style={styles.donationCard}>
            <View style={[styles.donationIcon, { backgroundColor: '#6D1ED4' }]}>
              <Text style={styles.donationIconText}>Z</Text>
            </View>
            <View style={styles.donationInfo}>
              <Text style={styles.donationName}>Zelle</Text>
              <Text style={styles.donationHandle}>Search "Jakari Jones" in your bank app</Text>
            </View>
          </View>
        </View>

        {/* Thank You Message */}
        <View style={styles.thankYouCard}>
          <Text style={styles.thankYouEmoji}>🙏</Text>
          <Text style={styles.thankYouTitle}>Thank You!</Text>
          <Text style={styles.thankYouText}>
            Whether you donate or not, thank you for using the app and trusting us with your exam preparation. 
            Good luck on your detective test!
          </Text>
        </View>

        {/* What Donations Help With */}
        <View style={styles.helpSection}>
          <Text style={styles.helpTitle}>What Donations Help With</Text>
          <View style={styles.helpItem}>
            <Ionicons name="server-outline" size={20} color="#10b981" />
            <Text style={styles.helpText}>Server costs to keep the app running</Text>
          </View>
          <View style={styles.helpItem}>
            <Ionicons name="book-outline" size={20} color="#10b981" />
            <Text style={styles.helpText}>Adding more practice questions & scenarios</Text>
          </View>
          <View style={styles.helpItem}>
            <Ionicons name="code-slash-outline" size={20} color="#10b981" />
            <Text style={styles.helpText}>Continuous app improvements</Text>
          </View>
          <View style={styles.helpItem}>
            <Ionicons name="people-outline" size={20} color="#10b981" />
            <Text style={styles.helpText}>Keeping the app free for everyone</Text>
          </View>
        </View>

        <View style={styles.bottomPadding} />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0c0c0c',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#1e293b',
  },
  backButton: {
    padding: 8,
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#fff',
  },
  placeholder: {
    width: 40,
  },
  scrollView: {
    flex: 1,
  },
  heroSection: {
    alignItems: 'center',
    paddingTop: 32,
    paddingBottom: 24,
  },
  heartContainer: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: '#1e293b',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
  },
  heroTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    textAlign: 'center',
  },
  missionCard: {
    backgroundColor: '#1e293b',
    marginHorizontal: 24,
    padding: 20,
    borderRadius: 16,
    marginBottom: 16,
  },
  missionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    marginBottom: 12,
  },
  missionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
  },
  missionText: {
    fontSize: 15,
    color: '#94a3b8',
    lineHeight: 24,
  },
  boldText: {
    fontWeight: 'bold',
    color: '#fff',
  },
  optionalNotice: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 10,
    backgroundColor: '#78350f',
    marginHorizontal: 24,
    padding: 16,
    borderRadius: 12,
    marginBottom: 24,
  },
  optionalText: {
    flex: 1,
    fontSize: 14,
    color: '#fcd34d',
    lineHeight: 20,
  },
  boldYellow: {
    fontWeight: 'bold',
    color: '#fbbf24',
  },
  donationSection: {
    paddingHorizontal: 24,
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 16,
  },
  donationCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1e293b',
    padding: 16,
    borderRadius: 12,
    marginBottom: 12,
  },
  donationIcon: {
    width: 48,
    height: 48,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },
  donationIconText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  donationInfo: {
    flex: 1,
  },
  donationName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#fff',
    marginBottom: 2,
  },
  donationHandle: {
    fontSize: 14,
    color: '#64748b',
  },
  thankYouCard: {
    backgroundColor: '#14532d',
    marginHorizontal: 24,
    padding: 24,
    borderRadius: 16,
    alignItems: 'center',
    marginBottom: 24,
    borderWidth: 1,
    borderColor: '#22c55e',
  },
  thankYouEmoji: {
    fontSize: 40,
    marginBottom: 12,
  },
  thankYouTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#22c55e',
    marginBottom: 8,
  },
  thankYouText: {
    fontSize: 14,
    color: '#86efac',
    textAlign: 'center',
    lineHeight: 20,
  },
  helpSection: {
    backgroundColor: '#1e293b',
    marginHorizontal: 24,
    padding: 20,
    borderRadius: 16,
    marginBottom: 24,
  },
  helpTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 16,
  },
  helpItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    marginBottom: 12,
  },
  helpText: {
    fontSize: 14,
    color: '#94a3b8',
    flex: 1,
  },
  bottomPadding: {
    height: 40,
  },
});
