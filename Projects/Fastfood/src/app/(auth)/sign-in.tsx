import CustomButton from '@/components/CustomButton'
import CustomInput from '@/components/CustomInput'
import { Link, router } from 'expo-router'
import { useState } from 'react'
import { Alert, Text, View } from 'react-native'
import { signin } from '../../../lib/appwrite'

const SignIn = () => {
  const [isSubmitting, setisSubmitting] = useState(false)
  const [form, setform] = useState({ email: '', password: '' })

  const submit = async () => {
    if (!form.email || !form.password){
      Alert.alert('Error', 'Please enter valid details')
      return;
    }

    setisSubmitting(true)

    try {
      await signin({ email: form.email, password: form.password })
      Alert.alert('Success', 'Signed in successfully')
      router.replace('/(tabs)')
    } catch (error: any) {
      console.error('Sign in error:', error);
      Alert.alert('Error', error?.message || 'Failed to sign in')
    } finally {
      setisSubmitting(false)
    }
  }

  return (
    <View>
      <CustomInput label='Email' value={form.email} onChangeText={(text) => setform(prev => ({ ...prev, email: text }))} />
      <CustomInput label='Password' value={form.password}  secureTextEntry={true} onChangeText={(text) => setform(prev => ({ ...prev, password: text }))} />
      <CustomButton title='Sign In' isLoading={isSubmitting} onPress={submit} />

      <View className='flex flex-row justify-center mt-5 gap-2'>
        <Text className='base-regular'>
          Dont have an account?
        </Text>
        <Link href='/(auth)/sign-up' className='text-primary' style={{ color: 'red', fontWeight: 'bold' }}> Sign Up</Link>
      </View>
    </View>
  )
}

export default SignIn