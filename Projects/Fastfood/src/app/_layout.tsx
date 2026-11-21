import { useFonts } from 'expo-font';
import { SplashScreen, Stack } from "expo-router";
import { useEffect } from "react";

import useAuthStore from '../../store/auth.store';
import './global.css';

export const unstable_settings = {
  anchor: '(tabs)',
};

export default function RootLayout() {
  const { fetchAuthenticatedUsers, isLoading } = useAuthStore();
  const [isFontsLoaded, error] = useFonts({
    "TWKLausanne-Light": require("../../assets/fonts/TWKLausanne-Light.ttf"),
    "TWKLausanne-Regular": require("../../assets/fonts/TWKLausanne-Regular.ttf"),
    "TWKLausanne-Semibold": require("../../assets/fonts/TWKLausanne-Semibold.ttf"),
    "TWKLausanne-Bold": require("../../assets/fonts/TWKLausanne-Bold.ttf"),
    "TWKLausanne-Extrabold": require("../../assets/fonts/TWKLausanne-Extrabold.ttf"),
  });

  useEffect(() => {
    if (error) throw error;
    if (isFontsLoaded) SplashScreen.hideAsync();
  }, [error, isFontsLoaded]);

  useEffect(() => {
    fetchAuthenticatedUsers();
  }, []);

  if (!isFontsLoaded || isLoading) return null;

  return (
    <Stack screenOptions={{ headerShown: false }}/>
  );
}
