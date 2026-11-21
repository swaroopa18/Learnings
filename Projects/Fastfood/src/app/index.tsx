import cn from 'clsx';
import React from "react";
import { FlatList, Image, Pressable, Text, TouchableOpacity, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { offers } from "../../constants";
import "./global.css";

export default function App() {
  return (
    <SafeAreaView className='flex-1 bg-white'>
      <View className='flex-between flex-row w-full my-5 px-5'>
        <View className='flex-start'>
          <Text className='small-bold text-primary'>DELIVER TO</Text>
          <TouchableOpacity className='flex-row flex-center gap-x-1 mt-0.5'>
            <Text className='paragraph-bold text-dark-100'>Hyderabad</Text>
            <Image
              source={{
                uri: "https://cdn-icons-png.flaticon.com/512/2985/2985150.png",
              }}
              className="w-6 h-6"
              resizeMode="contain"
            />
          </TouchableOpacity>
        </View>

        <Text>Cart</Text>
      </View>
      <FlatList data={offers} keyExtractor={(item) => item.id.toString()} renderItem={({ item, index }) => {
        const isEven = index % 2 == 0
        return (<View className="p-2">
          <Pressable className={cn("offer-card", isEven ? 'flex-row-reverse' : 'flex-row')}
            style={{ backgroundColor: item.color }}>
            {({ pressed }) => (<React.Fragment>
              <View className="h-full w-1/2">
                <Image source={{ uri: item.image }} className="size-full" resizeMode="contain" />
              </View>
              <View>
                <Text className="h1-bold">
                  {item.title}
                </Text>
              </View>
            </React.Fragment>)}
          </Pressable>
        </View>)
      }} contentContainerClassName='pb-28 px-5' />
    </SafeAreaView>
  );
}