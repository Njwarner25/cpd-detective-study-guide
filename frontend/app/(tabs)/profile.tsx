import React, { useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet, Alert, Image, ActivityIndicator, Share, Platform } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useAuth } from '../../contexts/AuthContext';
import { useRouter } from 'expo-router';
import { statsService } from '../../services/api';

// Cross-platform alert helper
const showAlert = (title, message, buttons) => {
  if (Platform.OS === 'web') {
    if (buttons && buttons.length > 1) {
      const confirmBtn = buttons.find(b => b.style !== 'cancel');
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

export default function Profile() {
  const { user, logout, isGuest, sessionToken, hasPaid } = useAuth();
  const router = useRouter();
  const [resetting, setResetting] = useState(false);

  const handleShare = async () => {
    try {
      const appUrl = 'https://www.detectiveexamstudyguide.com';
      await Share.share({
        message: 'Check out the CPD Detective Exam Study Guide app! It has 160+ practice questions, scenarios, and flashcards to help you prepare for the Chicago Police Department Detective Test.' + '\n\n' + 'Try it here: ' + appUrl + '\n\n' + 'Coming soon to App Store & Google Play!',
        title: 'CPD Detective Exam Study Guide',
        url: appUrl,
      });
    } catch (error) {
      console.error('Error sharing:', error);
    }
  };

  const handleLogout = () => {
    showAlert(
      'Logout',
      'Are you sure you want to logout?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Logout',
          style: 'destructive',
          onPress: async () => {
            await logout();
            router.replace('/(auth)/welcome');
          },
        },
      ]
    );
  };

  const handleUpgradeAccount = () => {
    router.push('/(auth)/login');
  };

  const handleResetScores = () => {
    showAlert(
      'Reset All Scores',
      'Are you sure you want to reset all your scenario scores? This action cannot be undone.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Reset',
          style: 'destructive',
          onPress: async () => {
            setResetting(true);
            try {
              const result = await statsService.resetScores(sessionToken || undefined);
              showAlert('Success', result.message);
            } catch (error) {
              console.error('Reset failed:', error);
              showAlert('Error', 'Failed to reset scores. Please try again.');
            } finally {
              setResetting(false);
            }
          },
        },
      ]
    );
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <ScrollView style={styles.scrollView}>
        <View style={styles.header}>
          <View style={styles.avatarContainer}>
            {user?.picture ? (
              <Image source={{ uri: user.picture }} style={styles.avatar} />
            ) : (
              <View style={[styles.avatarPlaceholder, isGuest && styles.guestAvatar]}>
                <Ionicons
                  name={isGuest ? 'person-outline' : 'person'}
                  size={48}
                  color={isGuest ? '#f59e0b' : '#64748b'}
                />
              </View>
            )}
          </View>
          <Text style={styles.name}>{user?.name || 'Guest User'}</Text>
          <Text style={styles.email}>{user?.email}</Text>
          {isGuest ? (
            <View style={styles.guestBadge}>
              <Ionicons name="time-outline" size={14} color="#f59e0b" />
              <Text style={styles.guestBadgeText}>Guest Account</Text>
            </View>
          ) : user?.role === 'admin' ? (
            <View style={styles.adminBadge}>
              <Text style={styles.adminBadgeText}>Admin</Text>
            </View>
          ) : (
            <View style={styles.registeredBadge}>
              <Ionicons name="checkmark-circle" size={14} color="#10b981" />
              <Text style={styles.registeredBadgeText}>Registered</Text>
            </View>
          )}
        </View>

        {/* Premium Upgrade Section - for registered users who haven't paid */}
        {!isGuest && user?.role !== 'admin' && !hasPaid && (
          <View style={styles.premiumUpgradeSection}>
            <TouchableOpacity
              style={styles.premiumUpgradeCard}
              onPress={() => router.push('/upgrade')}
            >
              <View style={styles.premiumUpgradeIconContainer}>
                <Ionicons name="star" size={32} color="#f59e0b" />
              </View>
              <View style={styles.premiumUpgradeContent}>
                <Text style={styles.premiumUpgradeTitle}>Upgrade to Premium</Text>
                <Text style={styles.premiumUpgradeSubtitle}>
                  Unlock all 20 practice scenarios with AI-powered grading
                </Text>
              </View>
              <View style={styles.premiumUpgradePrice}>
                <Text style={styles.premiumUpgradePriceText}>$25</Text>
                <Text style={styles.premiumUpgradePriceNote}>one-time</Text>
              </View>
            </TouchableOpacity>
          </View>
        )}

        {/* Premium Active Badge - for users who have paid */}
        {!isGuest && user?.role !== 'admin' && hasPaid && (
          <View style={styles.premiumActiveSection}>
            <View style={styles.premiumActiveCard}>
              <Ionicons name="star" size={24} color="#f59e0b" />
              <View style={styles.premiumActiveContent}>
                <Text style={styles.premiumActiveTitle}>Premium Active</Text>
                <Text style={styles.premiumActiveSubtitle}>You have full access to all content</Text>
              </View>
              <Ionicons name="checkmark-circle" size={24} color="#10b981" />
            </View>
          </View>
        )}

        {isGuest && (
          <View style={styles.upgradeSection}>
            <View style={styles.upgradeCard}>
              <View style={styles.upgradeIcon}>
                <Ionicons name="star" size={32} color="#f59e0b" />
              </View>
              <View style={styles.upgradeContent}>
                <Text style={styles.upgradeTitle}>Upgrade Your Account</Text>
                <Text style={styles.upgradeText}>
                  Create a free account to save your progress, sync across devices, and
                  track your study history.
                </Text>
              </View>
              <TouchableOpacity style={styles.upgradeButton} onPress={handleUpgradeAccount}>
                <Text style={styles.upgradeButtonText}>Create Account</Text>
              </TouchableOpacity>
            </View>
          </View>
        )}

        {isGuest && (
          <View style={styles.limitationsSection}>
            <Text style={styles.sectionTitle}>Guest Limitations</Text>
            <View style={styles.limitationItem}>
              <Ionicons name="close-circle" size={18} color="#ef4444" />
              <Text style={styles.limitationText}>Progress not saved after logout</Text>
            </View>
            <View style={styles.limitationItem}>
              <Ionicons name="close-circle" size={18} color="#ef4444" />
              <Text style={styles.limitationText}>No cross-device sync</Text>
            </View>
            <View style={styles.limitationItem}>
              <Ionicons name="close-circle" size={18} color="#ef4444" />
              <Text style={styles.limitationText}>Shared progress with other guests</Text>
            </View>
          </View>
        )}

        {!isGuest && (
          <View style={styles.benefitsSection}>
            <Text style={styles.sectionTitle}>Account Benefits</Text>
            <View style={styles.benefitItem}>
              <Ionicons name="checkmark-circle" size={18} color="#10b981" />
              <Text style={styles.benefitText}>Personal progress tracking</Text>
            </View>
            <View style={styles.benefitItem}>
              <Ionicons name="checkmark-circle" size={18} color="#10b981" />
              <Text style={styles.benefitText}>Sync across all devices</Text>
            </View>
            <View style={styles.benefitItem}>
              <Ionicons name="checkmark-circle" size={18} color="#10b981" />
              <Text style={styles.benefitText}>Bookmarks saved to your account</Text>
            </View>
            <View style={styles.benefitItem}>
              <Ionicons name="checkmark-circle" size={18} color="#10b981" />
              <Text style={styles.benefitText}>Study history preserved</Text>
            </View>
          </View>
        )}

        {!isGuest && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Account</Text>
            <TouchableOpacity style={styles.menuItem} onPress={() => router.push('/bookmarks')}>
              <View style={[styles.menuIconContainer, { backgroundColor: '#78350f' }]}>
                <Ionicons name="bookmark" size={20} color="#f59e0b" />
              </View>
              <Text style={styles.menuText}>My Bookmarks</Text>
              <Ionicons name="chevron-forward" size={20} color="#64748b" />
            </TouchableOpacity>
            <TouchableOpacity style={styles.menuItem} onPress={handleResetScores} disabled={resetting}>
              <View style={[styles.menuIconContainer, { backgroundColor: '#7f1d1d' }]}>
                {resetting ? (
                  <ActivityIndicator size="small" color="#ef4444" />
                ) : (
                  <Ionicons name="refresh" size={20} color="#ef4444" />
                )}
              </View>
              <Text style={styles.menuText}>Reset All Scores</Text>
              <Ionicons name="chevron-forward" size={20} color="#64748b" />
            </TouchableOpacity>
            <TouchableOpacity style={styles.menuItem}>
              <View style={styles.menuIconContainer}>
                <Ionicons name="person-outline" size={20} color="#fff" />
              </View>
              <Text style={styles.menuText}>Edit Profile</Text>
              <Ionicons name="chevron-forward" size={20} color="#64748b" />
            </TouchableOpacity>
            <TouchableOpacity style={styles.menuItem}>
              <View style={styles.menuIconContainer}>
                <Ionicons name="lock-closed-outline" size={20} color="#fff" />
              </View>
              <Text style={styles.menuText}>Change Password</Text>
              <Ionicons name="chevron-forward" size={20} color="#64748b" />
            </TouchableOpacity>
          </View>
        )}

        {user?.role === 'admin' && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Admin</Text>
            <TouchableOpacity
              style={styles.menuItem}
              onPress={() => router.push('/admin')}
            >
              <View style={[styles.menuIconContainer, { backgroundColor: '#7c2d12' }]}>
                <Ionicons name="analytics" size={20} color="#f97316" />
              </View>
              <Text style={styles.menuText}>Analytics Dashboard</Text>
              <Ionicons name="chevron-forward" size={20} color="#64748b" />
            </TouchableOpacity>
          </View>
        )}

        {/* Install App Section */}
        <View style={styles.installSection}>
          <TouchableOpacity
            style={styles.installCard}
            onPress={() => router.push('/install')}
          >
            <View style={styles.installIconContainer}>
              <Ionicons name="download-outline" size={28} color="#3b82f6" />
            </View>
            <View style={styles.installContent}>
              <Text style={styles.installTitle}>Install App on Your Device</Text>
              <Text style={styles.installSubtitle}>
                Add to home screen for quick access
              </Text>
            </View>
            <Ionicons name="chevron-forward" size={24} color="#3b82f6" />
          </TouchableOpacity>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Support</Text>
          <TouchableOpacity style={styles.menuItem} onPress={() => router.push('/updates')}>
            <View style={[styles.menuIconContainer, { backgroundColor: '#1e3a8a' }]}>
              <Ionicons name="sparkles" size={20} color="#60a5fa" />
            </View>
            <Text style={styles.menuText}>What's New</Text>
            <View style={styles.newBadge}>
              <Text style={styles.newBadgeText}>NEW</Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color="#64748b" />
          </TouchableOpacity>
          <TouchableOpacity style={styles.menuItem}>
            <View style={styles.menuIconContainer}>
              <Ionicons name="help-circle-outline" size={20} color="#fff" />
            </View>
            <Text style={styles.menuText}>Help Center</Text>
            <Ionicons name="chevron-forward" size={20} color="#64748b" />
          </TouchableOpacity>
          <TouchableOpacity style={styles.menuItem}>
            <View style={styles.menuIconContainer}>
              <Ionicons name="information-circle-outline" size={20} color="#fff" />
            </View>
            <Text style={styles.menuText}>About</Text>
            <Ionicons name="chevron-forward" size={20} color="#64748b" />
          </TouchableOpacity>
        </View>

        {/* Share with Friend Section */}
        <View style={styles.shareSection}>
          <View style={styles.shareCard}>
            <View style={styles.shareIconContainer}>
              <Ionicons name="share-social" size={28} color="#10b981" />
            </View>
            <Text style={styles.shareTitle}>Share with a Friend</Text>
            <Text style={styles.shareText}>
              Know someone preparing for the detective test? Share this app with them!
            </Text>
            <View style={styles.comingSoonBadge}>
              <Ionicons name="storefront-outline" size={14} color="#94a3b8" />
              <Text style={styles.comingSoonText}>Not yet on app stores - Coming soon!</Text>
            </View>
            <TouchableOpacity style={styles.shareButton} onPress={handleShare}>
              <Ionicons name="share-outline" size={20} color="#fff" />
              <Text style={styles.shareButtonText}>Share App</Text>
            </TouchableOpacity>
          </View>
        </View>

        {/* Support/Donate Section */}
        <View style={styles.supportSection}>
          <TouchableOpacity
            style={styles.supportCard}
            onPress={() => router.push('/support')}
          >
            <View style={styles.supportIconContainer}>
              <Ionicons name="heart" size={28} color="#ef4444" />
            </View>
            <View style={styles.supportContent}>
              <Text style={styles.supportTitle}>Support the App</Text>
              <Text style={styles.supportSubtitle}>
                Optional donations to help keep it free
              </Text>
            </View>
            <Ionicons name="chevron-forward" size={24} color="#ef4444" />
          </TouchableOpacity>
        </View>

        <View style={styles.section}>
          <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
            <Ionicons name="log-out-outline" size={20} color="#ef4444" />
            <Text style={styles.logoutText}>Logout</Text>
          </TouchableOpacity>
        </View>

        <Text style={styles.version}>Version 1.5.0</Text>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0c0c0c',
  },
  scrollView: {
    flex: 1,
  },
  header: {
    padding: 24,
    alignItems: 'center',
    paddingTop: 20,
  },
  avatarContainer: {
    marginBottom: 16,
  },
  avatar: {
    width: 96,
    height: 96,
    borderRadius: 48,
  },
  avatarPlaceholder: {
    width: 96,
    height: 96,
    borderRadius: 48,
    backgroundColor: '#1e293b',
    justifyContent: 'center',
    alignItems: 'center',
  },
  guestAvatar: {
    borderWidth: 2,
    borderColor: '#f59e0b',
    borderStyle: 'dashed',
  },
  name: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 4,
  },
  email: {
    fontSize: 16,
    color: '#94a3b8',
  },
  guestBadge: {
    backgroundColor: '#78350f',
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
    marginTop: 8,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  guestBadgeText: {
    color: '#fcd34d',
    fontSize: 12,
    fontWeight: '600',
  },
  adminBadge: {
    backgroundColor: '#7c3aed',
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
    marginTop: 8,
  },
  adminBadgeText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
  },
  registeredBadge: {
    backgroundColor: '#064e3b',
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
    marginTop: 8,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  registeredBadgeText: {
    color: '#10b981',
    fontSize: 12,
    fontWeight: '600',
  },
  // Premium upgrade styles
  premiumUpgradeSection: {
    paddingHorizontal: 24,
    marginBottom: 16,
  },
  premiumUpgradeCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 16,
    borderWidth: 2,
    borderColor: '#f59e0b',
  },
  premiumUpgradeIconContainer: {
    width: 56,
    height: 56,
    borderRadius: 14,
    backgroundColor: '#78350f',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  premiumUpgradeContent: {
    flex: 1,
  },
  premiumUpgradeTitle: {
    fontSize: 17,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 4,
  },
  premiumUpgradeSubtitle: {
    fontSize: 13,
    color: '#94a3b8',
    lineHeight: 18,
  },
  premiumUpgradePrice: {
    alignItems: 'center',
    marginLeft: 8,
  },
  premiumUpgradePriceText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#10b981',
  },
  premiumUpgradePriceNote: {
    fontSize: 11,
    color: '#64748b',
  },
  // Premium active styles
  premiumActiveSection: {
    paddingHorizontal: 24,
    marginBottom: 16,
  },
  premiumActiveCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#064e3b',
    borderRadius: 16,
    padding: 16,
    gap: 12,
    borderWidth: 1,
    borderColor: 'rgba(16, 185, 129, 0.3)',
  },
  premiumActiveContent: {
    flex: 1,
  },
  premiumActiveTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#10b981',
    marginBottom: 2,
  },
  premiumActiveSubtitle: {
    fontSize: 13,
    color: '#6ee7b7',
  },
  upgradeSection: {
    paddingHorizontal: 24,
    marginBottom: 16,
  },
  upgradeCard: {
    backgroundColor: '#1e3a5f',
    borderRadius: 16,
    padding: 20,
    borderWidth: 1,
    borderColor: '#f59e0b',
  },
  upgradeIcon: {
    alignItems: 'center',
    marginBottom: 12,
  },
  upgradeContent: {
    marginBottom: 16,
  },
  upgradeTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
    textAlign: 'center',
    marginBottom: 8,
  },
  upgradeText: {
    fontSize: 14,
    color: '#94a3b8',
    textAlign: 'center',
    lineHeight: 20,
  },
  upgradeButton: {
    backgroundColor: '#f59e0b',
    padding: 14,
    borderRadius: 10,
    alignItems: 'center',
  },
  upgradeButtonText: {
    color: '#000',
    fontSize: 16,
    fontWeight: '600',
  },
  limitationsSection: {
    paddingHorizontal: 24,
    marginBottom: 16,
  },
  limitationItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    paddingVertical: 8,
  },
  limitationText: {
    color: '#94a3b8',
    fontSize: 14,
  },
  benefitsSection: {
    paddingHorizontal: 24,
    marginBottom: 16,
  },
  benefitItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    paddingVertical: 8,
  },
  benefitText: {
    color: '#94a3b8',
    fontSize: 14,
  },
  section: {
    padding: 24,
    paddingTop: 8,
    gap: 8,
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#64748b',
    textTransform: 'uppercase',
    letterSpacing: 0.5,
    marginBottom: 8,
  },
  menuItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1e293b',
    padding: 16,
    borderRadius: 12,
    gap: 12,
  },
  menuIconContainer: {
    width: 36,
    height: 36,
    borderRadius: 8,
    backgroundColor: '#334155',
    justifyContent: 'center',
    alignItems: 'center',
  },
  menuText: {
    flex: 1,
    fontSize: 16,
    color: '#fff',
  },
  logoutButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#1e293b',
    padding: 16,
    borderRadius: 12,
    gap: 8,
    borderWidth: 1,
    borderColor: '#7f1d1d',
  },
  logoutText: {
    color: '#ef4444',
    fontSize: 16,
    fontWeight: '600',
  },
  version: {
    textAlign: 'center',
    color: '#64748b',
    fontSize: 12,
    paddingTop: 24,
    paddingBottom: 24,
  },
  newBadge: {
    backgroundColor: '#2563eb',
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 6,
    marginLeft: 'auto',
    marginRight: 8,
  },
  newBadgeText: {
    color: '#fff',
    fontSize: 10,
    fontWeight: 'bold',
  },
  shareSection: {
    paddingHorizontal: 24,
    paddingBottom: 16,
  },
  shareCard: {
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 20,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#10b981',
  },
  shareIconContainer: {
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: '#064e3b',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
  },
  shareTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 8,
  },
  shareText: {
    fontSize: 14,
    color: '#94a3b8',
    textAlign: 'center',
    lineHeight: 20,
    marginBottom: 12,
  },
  comingSoonBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    backgroundColor: '#334155',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
    marginBottom: 16,
  },
  comingSoonText: {
    color: '#94a3b8',
    fontSize: 12,
    fontStyle: 'italic',
  },
  shareButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    backgroundColor: '#10b981',
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 10,
  },
  shareButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  supportSection: {
    paddingHorizontal: 24,
    paddingBottom: 16,
  },
  supportCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 16,
    borderWidth: 2,
    borderColor: '#ef4444',
  },
  supportIconContainer: {
    width: 48,
    height: 48,
    borderRadius: 12,
    backgroundColor: '#450a0a',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  supportContent: {
    flex: 1,
  },
  supportTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 4,
  },
  supportSubtitle: {
    fontSize: 13,
    color: '#94a3b8',
  },
  installSection: {
    paddingHorizontal: 24,
    paddingBottom: 16,
  },
  installCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1e3a8a',
    borderRadius: 16,
    padding: 16,
    borderWidth: 2,
    borderColor: '#3b82f6',
  },
  installIconContainer: {
    width: 48,
    height: 48,
    borderRadius: 12,
    backgroundColor: '#1e293b',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  installContent: {
    flex: 1,
  },
  installTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 4,
  },
  installSubtitle: {
    fontSize: 13,
    color: '#93c5fd',
  },
});
