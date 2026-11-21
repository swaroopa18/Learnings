import CustomButton from '@/components/CustomButton'
import CustomInput from '@/components/CustomInput'
import { Link, router } from 'expo-router'
import { useState } from 'react'
import { Alert, Text, View } from 'react-native'
import { createUser } from '../../../lib/appwrite'

const SignUp = () => {
  const [isSubmitting, setisSubmitting] = useState(false)
  const [form, setform] = useState({ name: '', email: '', password: '' })

  const submit = async () => {
    const { email, password, name } = form
    if (!name || !email || !password) {
      Alert.alert('Error', 'Please enter valid details')
      return;
    }

    setisSubmitting(true)

    try {
      await createUser({ email, password, name })
      Alert.alert('Success', 'Account created successfully')
      router.replace('/(tabs)')
    } catch (error: any) {
      console.error('Sign up error:', error);
      Alert.alert('Error', error?.message || 'Failed to create account')
    } finally {
      setisSubmitting(false)
    }
  }

  return (
    <View>
      <CustomInput label='Name' value={form.name} onChangeText={(text) => setform(prev => ({ ...prev, name: text }))} />
      <CustomInput label='Email' value={form.email} onChangeText={(text) => setform(prev => ({ ...prev, email: text }))} />
      <CustomInput label='Password' value={form.password} secureTextEntry={true} onChangeText={(text) => setform(prev => ({ ...prev, password: text }))} />

      <CustomButton title='Sign Up' isLoading={isSubmitting} onPress={submit} />

      <View className='flex flex-row justify-center mt-5 gap-2'>
        <Text className='base-regular'>
          Already have an account?
        </Text>
        <Link href='/(auth)/sign-in' className='text-primary' style={{ color: 'red', fontWeight: 'bold' }}> Sign In</Link>
      </View>
    </View>
  )
}

export default SignUp;