import { Stack } from 'expo-router';
import { AuthProvider } from '../contexts/AuthContext';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import VersionCheck from '../components/VersionCheck';

export default function RootLayout() {
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