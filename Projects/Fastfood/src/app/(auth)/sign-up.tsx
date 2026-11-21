import CustomButton from '@/components/CustomButton'
import CustomInput from '@/components/CustomInput'
import { Link, router } from 'expo-router'
import { useState } from 'react'
import { Alert, Text, View } from 'react-native'

const SignUp = () => {
  const [isSubmitting, setisSubmitting] = useState(false)
  const [form, setform] = useState({ name: '', email: '', password: '' })

  const submit = () => {
    console.log("---submit")
    if (!form.email || !form.password || !form.password) {
      Alert.alert('Please enter valid details')
      return;
    }

    setisSubmitting(true)

    try {
      //appwrite signup function
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
      <CustomInput label='Name' value={form.name} onChangeText={(text) => setform(prev => ({ ...prev, name: text }))} />
      <CustomInput label='Email' value={form.email} onChangeText={(text) => setform(prev => ({ ...prev, email: text }))} />
      <CustomInput label='Password' secureTextEntry={true} onChangeText={(text) => setform(prev => ({ ...prev, password: text }))} />

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