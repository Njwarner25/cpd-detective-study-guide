import { Stack } from 'expo-router';
import { AuthProvider } from '../contexts/AuthContext';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import VersionCheck from '../components/VersionCheck';
import { Platform } from 'react-native';

export default function RootLayout() {
  // Skip version check on web for now - Railway deployment issue
  if (Platform.OS === 'web') {
    return (
      <SafeAreaProvider>
        <AuthProvider>
          <Stack screenOptions={{ headerShown: false }}>
            <Stack.Screen name="index" />
            <Stack.Screen name="(auth)" />
            <Stack.Screen name="(tabs)" />
          </Stack>
        </AuthProvider>
      </SafeAreaProvider>
    );
  }
  
  return (
    <SafeAreaProvider>
      <VersionCheck>
        <AuthProvider>
          <Stack screenOptions={{ headerShown: false }}>
            <Stack.Screen name="index" />
            <Stack.Screen name="(auth)" />
            <Stack.Screen name="(tabs)" />
          </Stack>
        </AuthProvider>
      </VersionCheck>
    </SafeAreaProvider>
  );
}