import { router } from 'expo-router'
import { Button, Text, View } from 'react-native'

const SignIn = () => {
  return (
    <View>
      <Text>Sign In</Text>
      <Button title='Sign Up' onPress={() => router.push('/(auth)/sign-up')}></Button>
    </View>
  )
}

export default SignIn