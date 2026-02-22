// frontend/app/payment-success.tsx
// Shown after successful Stripe checkout redirect
import React, { useEffect, useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ActivityIndicator } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import { useAuth } from '../contexts/AuthContext';

export default function PaymentSuccess() {
  const router = useRouter();
  const { refreshPaymentStatus } = useAuth();
  const [verifying, setVerifying] = useState(true);
  const [verified, setVerified] = useState(false);

  useEffect(() => { verifyPayment(); }, []);

  const verifyPayment = async () => {
    setVerifying(true);
    try {
      await new Promise(resolve => setTimeout(resolve, 2000));
      const paid = await refreshPaymentStatus();
      setVerified(paid);
      if (!paid) {
        await new Promise(resolve => setTimeout(resolve, 3000));
        const retryPaid = await refreshPaymentStatus();
        setVerified(retryPaid);
      }
    } catch (error) {
      console.error('Verification error:', error);
    } finally { setVerifying(false); }
  };

  return (
    <SafeAreaView style={s.container}>
      <View style={s.content}>
        {verifying ? (
          <>
            <ActivityIndicator size="large" color="#10b981" />
            <Text style={s.verifyingText}>Verifying your payment...</Text>
            <Text style={s.verifyingSubtext}>This may take a moment</Text>
          </>
        ) : verified ? (
          <>
            <View style={s.iconContainer}>
              <Ionicons name="checkmark-circle" size={100} color="#10b981" />
            </View>
            <Text style={s.title}>Payment Successful!</Text>
            <Text style={s.subtitle}>You now have full access to all premium scenarios. Time to study!</Text>
            <TouchableOpacity style={s.button} onPress={() => router.replace('/(tabs)/home')}>
              <Ionicons name="rocket" size={20} color="#fff" />
              <Text style={s.buttonText}>Start Studying</Text>
            </TouchableOpacity>
          </>
        ) : (
          <>
            <View style={s.iconContainer}>
              <Ionicons name="time" size={100} color="#f59e0b" />
            </View>
            <Text style={s.title}>Processing Payment</Text>
            <Text style={s.subtitle}>Your payment is being processed. This usually takes just a few seconds.</Text>
            <TouchableOpacity style={s.button} onPress={verifyPayment}>
              <Ionicons name="refresh" size={20} color="#fff" />
              <Text style={s.buttonText}>Check Again</Text>
            </TouchableOpacity>
            <TouchableOpacity style={s.secondaryButton} onPress={() => router.replace('/(tabs)/home')}>
              <Text style={s.secondaryButtonText}>Go Home</Text>
            </TouchableOpacity>
          </>
        )}
      </View>
    </SafeAreaView>
  );
}

const s = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0c0c0c' },
  content: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 24 },
  iconContainer: { marginBottom: 24 },
  title: { fontSize: 28, fontWeight: 'bold', color: '#fff', textAlign: 'center', marginBottom: 12 },
  subtitle: { fontSize: 16, color: '#94a3b8', textAlign: 'center', lineHeight: 24, marginBottom: 32, maxWidth: 320 },
  verifyingText: { fontSize: 18, color: '#fff', marginTop: 20 },
  verifyingSubtext: { fontSize: 14, color: '#64748b', marginTop: 8 },
  button: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8, backgroundColor: '#10b981', paddingHorizontal: 32, paddingVertical: 16, borderRadius: 12, marginBottom: 12 },
  buttonText: { color: '#fff', fontSize: 16, fontWeight: '600' },
  secondaryButton: { padding: 12 },
  secondaryButtonText: { color: '#60a5fa', fontSize: 14, fontWeight: '500' },
});
