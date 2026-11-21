import { Slot } from 'expo-router';
import { Text, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function AuthLayout() {
  return <SafeAreaView>
    <View><Text>Auth view</Text></View>

    <Slot />
  </SafeAreaView>;
}
