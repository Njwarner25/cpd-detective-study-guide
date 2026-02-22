import React, { useEffect } from 'react';
import { View, ActivityIndicator, StyleSheet } from 'react-native';
import { useAuth } from '../contexts/AuthContext';
import { useRouter } from 'expo-router';

export default function Index() {
  const { user, loading, hasPaid, checkingPayment } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading) {
      if (user) {
        if (hasPaid || user.role === 'admin') {
          router.replace('/(tabs)/home');
        } else {
          router.replace('/upgrade');
        }
      } else {
        router.replace('/(auth)/welcome');
      }
    }
  }, [user, loading, hasPaid]);

  return (
    <View style={styles.container}>
      <ActivityIndicator size="large" color="#2563eb" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0c0c0c',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
