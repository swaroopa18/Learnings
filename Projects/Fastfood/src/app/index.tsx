import { FlatList, Image, Pressable, Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { offers } from "../../constants";
import "./global.css";

export default function App() {
  return (
    <SafeAreaView>
      <FlatList data={offers} keyExtractor={(item) => item.id.toString()} renderItem={({ item }) =>
      (<View className="p-2">
        <Pressable className="offer-card">
          <Text className="text-lg font-bold">{item.title}</Text>
          <Image source={{ uri: item.image }} className="w-full h-40 rounded-lg mt-3" />
        </Pressable>
      </View>)
      } />
    </SafeAreaView>
  );
}