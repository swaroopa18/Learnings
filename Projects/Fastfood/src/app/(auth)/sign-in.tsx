import CustomButton from '@/components/CustomButton'
import CustomInput from '@/components/CustomInput'
import { View } from 'react-native'

const SignIn = () => {
  return (
    <View>
      <CustomInput label='email' />
      <CustomButton />
    </View>
  )
}

export default SignIn