import React, { useEffect, useRef } from 'react';
import {
  TouchableOpacity,
  Image,
  View,
  Text,
  StyleSheet,
  Animated,
} from 'react-native';

interface DetectiveBotBubbleProps {
  onPress: () => void;
  hintCount?: number;
}

export default function DetectiveBotBubble({ onPress, hintCount = 0 }: DetectiveBotBubbleProps) {
  const scale = useRef(new Animated.Value(0)).current;
  const pulse = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    // Entrance animation
    Animated.spring(scale, {
      toValue: 1,
      damping: 12,
      stiffness: 100,
      useNativeDriver: true,
    }).start();

    // Subtle pulse animation
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulse, {
          toValue: 1.06,
          duration: 1500,
          useNativeDriver: true,
        }),
        Animated.timing(pulse, {
          toValue: 1.0,
          duration: 1500,
          useNativeDriver: true,
        }),
      ])
    ).start();
  }, []);

  const animatedScale = Animated.multiply(scale, pulse);

  return (
    <Animated.View
      style={[
        styles.bubble,
        { transform: [{ scale: animatedScale }] },
      ]}
    >
      <TouchableOpacity onPress={onPress} activeOpacity={0.8} style={styles.touchable}>
        <Image
          source={require('../assets/images/detective-bot.png')}
          style={styles.avatar}
        />
        {hintCount > 0 && (
          <View style={styles.badge}>
            <Text style={styles.badgeText}>{hintCount > 9 ? '9+' : hintCount}</Text>
          </View>
        )}
      </TouchableOpacity>
      <View style={styles.tooltip}>
        <Text style={styles.tooltipText}>Click me if you need help!</Text>
      </View>
    </Animated.View>
  );
}

const styles = StyleSheet.create({
  bubble: {
    position: 'absolute',
    bottom: 100,
    right: 20,
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: '#1e293b',
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#3b82f6',
    shadowColor: '#3b82f6',
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.5,
    shadowRadius: 10,
    elevation: 8,
    zIndex: 50,
  },
  touchable: {
    width: 60,
    height: 60,
    borderRadius: 30,
    justifyContent: 'center',
    alignItems: 'center',
  },
  avatar: {
    width: 50,
    height: 50,
    borderRadius: 25,
  },
  badge: {
    position: 'absolute',
    top: -4,
    right: -4,
    backgroundColor: '#ef4444',
    borderRadius: 10,
    minWidth: 20,
    height: 20,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 4,
  },
  badgeText: {
    color: '#fff',
    fontSize: 11,
    fontWeight: 'bold',
  },
  tooltip: {
    position: 'absolute',
    right: 68,
    top: 12,
    backgroundColor: '#3b82f6',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
    whiteSpace: 'nowrap',
  },
  tooltipText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
  },
});
