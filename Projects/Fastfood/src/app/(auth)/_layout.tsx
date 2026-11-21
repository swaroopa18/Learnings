import { ImageBackground } from 'expo-image';
import { Slot } from 'expo-router';
import { cssInterop } from 'nativewind';
import { Dimensions, Image, KeyboardAvoidingView, Platform, ScrollView, View } from 'react-native';

cssInterop(ImageBackground, { className: 'style' });

export default function AuthLayout() {
    return (
        <KeyboardAvoidingView
            className="flex-1"
            style={{ flex: 1 }}
            behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        >
            <ScrollView
                className="h-full bg-white"
                contentContainerStyle={{ flexGrow: 1 }}
                keyboardShouldPersistTaps="handled"
            >
                <View
                    className="w-full relative"
                    style={{ height: Dimensions.get('screen').height / 2.25 }}
                >
                    <ImageBackground
                        source={{ uri: 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=1200&q=80' }}
                        style={{ width: '100%', height: '100%' }}
                        className="size-full"
                        contentFit="cover"
                    />
                    <View
                        className="self-center absolute -bottom-14 z-10 rounded-full border-4 border-white bg-white shadow-lg overflow-hidden items-center justify-center"
                        style={{
                            width: 120,
                            height: 120,
                            elevation: 8,
                        }}
                    >
                        <Image
                            source={{ uri: 'https://images.unsplash.com/photo-1632203171982-cc0df6e9ceb4?q=80&w=1428&auto=format&fit=crop' }}
                            className="size-full"
                            resizeMode="cover"
                        />
                    </View>
                </View>
                <View className="flex-1 pt-20 px-6">
                    <Slot />
                </View>
            </ScrollView>
        </KeyboardAvoidingView>
    );
}
