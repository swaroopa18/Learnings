import cn from 'clsx';
import { Redirect, Tabs } from 'expo-router';
import { Image, Text, View } from 'react-native';
import useAuthStore from '../../../store/auth.store';

const TabBarIcon = ({ focused, icon, title }: TabBarIconProps) => {
  return (
    <View className='tab-icon'>
      <Image
        source={icon}
        className='size-7'
        resizeMode='contain'
        tintColor={focused ? '#413DFF' : '#808080'}
      />
      <Text className={cn('text-sm font-bold', focused ? 'text-primary' : 'text-grey-500')}>
        {title}
      </Text>
    </View>
  );
};
export default function _layout() {
  const { isAuthenticated } = useAuthStore()
  if (!isAuthenticated) {
    return <Redirect href='/sign-in' />
  }
  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarShowLabel: false,
        tabBarItemStyle: {
          width: '100%',
          height: '100%',
          justifyContent: 'center',
          alignItems: 'center',
        },
        tabBarIconStyle: {
          width: '100%',
          height: '100%',
        },
        tabBarStyle: {
          borderRadius: 50,
          marginHorizontal: 20,
          height: 80,
          position: 'absolute',
          bottom: 40,
          backgroundColor: 'white',
          shadowColor: '#1a1a1a',
          shadowOffset: { width: 0, height: 2 },
          shadowOpacity: 0.1,
          shadowRadius: 4,
          elevation: 5,
          paddingBottom: 0,
          paddingTop: 0,
        },
      }}>
      <Tabs.Screen
        name='index'
        options={{
          title: 'Home',
          tabBarIcon: ({ focused }) => <TabBarIcon title='Home'
            icon={{
              uri: 'https://img.icons8.com/ios-filled/100/home.png',
            }} focused={focused} />,
        }} >
      </Tabs.Screen>
      <Tabs.Screen
        name='search'
        options={{
          title: 'Search',
          tabBarIcon: ({ focused }) => <TabBarIcon title='Search'
            icon={{
              uri: 'https://img.icons8.com/ios-filled/100/search.png',
            }} focused={focused} />,
        }} >
      </Tabs.Screen>
      <Tabs.Screen
        name='cart'
        options={{
          title: 'Cart',
          tabBarIcon: ({ focused }) => <TabBarIcon title='Cart'
            icon={{
              uri: 'https://img.icons8.com/ios-filled/100/shopping-cart.png',
            }} focused={focused} />,
        }} >
      </Tabs.Screen>
      <Tabs.Screen
        name='profile'
        options={{
          title: 'Profile',
          tabBarIcon: ({ focused }) => <TabBarIcon title='Profile'
            icon={{
              uri: 'https://img.icons8.com/ios-filled/100/user.png',
            }} focused={focused} />,
        }} >
      </Tabs.Screen>
    </Tabs>
  )
}