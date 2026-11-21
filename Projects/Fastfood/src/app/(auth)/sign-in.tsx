import CustomButton from '@/components/CustomButton'
import CustomInput from '@/components/CustomInput'
import { Link, router } from 'expo-router'
import { useState } from 'react'
import { Alert, Text, View } from 'react-native'

const SignIn = () => {
  const [isSubmitting, setisSubmitting] = useState(false)
  const [form, setform] = useState({ email: '', password: '' })

  const submit = () => {
    if (!form.email || !form.password){
      Alert.alert('Please enter valid details')
      return;
    }

    setisSubmitting(true)

    try {
      //appwrite signin function
      Alert.alert('Signed in successfully')
      router.replace('/')
    } catch (error: any) {
      Alert.alert('Error', error)
    } finally {
      setisSubmitting(false)
    }
  }

  return (
    <View>
      <CustomInput label='Email' value={form.email} onChangeText={(text) => setform(prev => ({ ...prev, email: text }))} />
      <CustomInput label='Password' secureTextEntry={true} onChangeText={(text) => setform(prev => ({ ...prev, password: text }))} />
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