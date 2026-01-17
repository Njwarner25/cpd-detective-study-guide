import React, { useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet, Alert, Image, ActivityIndicator } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useAuth } from '../../contexts/AuthContext';
import { useRouter } from 'expo-router';
import { statsService } from '../../services/api';

export default function Profile() {
  const { user, logout, isGuest, sessionToken } = useAuth();
  const router = useRouter();
  const [resetting, setResetting] = useState(false);

  const handleLogout = () => {
    Alert.alert(
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
    Alert.alert(
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
              Alert.alert('Success', result.message);
            } catch (error) {
              console.error('Reset failed:', error);
              Alert.alert('Error', 'Failed to reset scores. Please try again.');
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
                <Ionicons name={isGuest ? "person-outline" : "person"} size={48} color={isGuest ? "#f59e0b" : "#64748b"} />
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

        {isGuest && (
          <View style={styles.upgradeSection}>
            <View style={styles.upgradeCard}>
              <View style={styles.upgradeIcon}>
                <Ionicons name="star" size={32} color="#f59e0b" />
              </View>
              <View style={styles.upgradeContent}>
                <Text style={styles.upgradeTitle}>Upgrade Your Account</Text>
                <Text style={styles.upgradeText}>
                  Create a free account to save your progress, sync across devices, and track your study history.
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
            
            <TouchableOpacity style={styles.menuItem} onPress={() => router.push('/leaderboard')}>
              <View style={[styles.menuIconContainer, { backgroundColor: '#1e3a5f' }]}>
                <Ionicons name="trophy" size={20} color="#fbbf24" />
              </View>
              <Text style={styles.menuText}>Leaderboard</Text>
              <Ionicons name="chevron-forward" size={20} color="#64748b" />
            </TouchableOpacity>
            
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
              <View style={styles.menuIconContainer}>
                <Ionicons name="settings-outline" size={20} color="#fff" />
              </View>
              <Text style={styles.menuText}>Manage Questions</Text>
              <Ionicons name="chevron-forward" size={20} color="#64748b" />
            </TouchableOpacity>
          </View>
        )}

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

        <View style={styles.section}>
          <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
            <Ionicons name="log-out-outline" size={20} color="#ef4444" />
            <Text style={styles.logoutText}>Logout</Text>
          </TouchableOpacity>
        </View>

        <Text style={styles.version}>Version 1.0.0</Text>
        <Text style={styles.credits}>Created by Nathaniel Warner</Text>
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
  },
  credits: {
    textAlign: 'center',
    color: '#64748b',
    fontSize: 12,
    paddingBottom: 24,
    fontStyle: 'italic',
  },
});
