import { Redirect, Slot } from 'expo-router'
import useAuthStore from '../../../store/auth.store'

export default function _layout() {
  const { isAuthenticated } = useAuthStore()
  console.log("----isAuthenticated", isAuthenticated)
  if (!isAuthenticated) {
    return <Redirect href='/sign-in' />
  }
  return (
    <Slot />
  )
}