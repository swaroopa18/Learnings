import { useFonts } from 'expo-font';
import { SplashScreen, Stack } from "expo-router";
import { useEffect } from "react";

import './global.css';

export default function RootLayout() {
  const [isLoaded, error] = useFonts({
    "TWKLausanne-Light": require("../../assets/fonts/TWKLausanne-Light.ttf"),
    "TWKLausanne-Regular": require("../../assets/fonts/TWKLausanne-Regular.ttf"),
    "TWKLausanne-Semibold": require("../../assets/fonts/TWKLausanne-Semibold.ttf"),
    "TWKLausanne-Bold": require("../../assets/fonts/TWKLausanne-Bold.ttf"),
    "TWKLausanne-Extrabold": require("../../assets/fonts/TWKLausanne-Extrabold.ttf"),
  });

  useEffect(() => {
    if (error) throw error;
    if (isLoaded) SplashScreen.hideAsync()
  }, [])
  return <Stack
    screenOptions={{
      headerShown: false,
    }}
  />;
}
