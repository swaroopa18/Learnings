import cn from 'clsx';
import { useState } from 'react';
import { KeyboardTypeOptions, Text, TextInput, TouchableOpacity, View } from 'react-native';

interface CustomInputProps {
    placeholder?: string;
    value?: string;
    onChangeText?: (text: string) => void;
    onChange?: (e: any) => void;
    label: string;
    secureTextEntry?: boolean;
    keyboardType?: KeyboardTypeOptions;
    error?: string;
}

const CustomInput = ({
    placeholder,
    value = '',
    onChangeText,
    onChange,
    label,
    secureTextEntry = false,
    keyboardType = 'default',
    error,
}: CustomInputProps) => {
    const [isFocused, setIsFocused] = useState(false);
    const [showPassword, setShowPassword] = useState(false);

    return (
        <View className="w-full mb-4">
            <Text className="label">{label}</Text>
            <View className="relative w-full justify-center">
                <TextInput
                    autoCapitalize="none"
                    autoCorrect={false}
                    value={value}
                    onChangeText={onChangeText}
                    onChange={onChange}
                    secureTextEntry={secureTextEntry && !showPassword}
                    keyboardType={keyboardType}
                    onFocus={() => setIsFocused(true)}
                    onBlur={() => setIsFocused(false)}
                    placeholder={placeholder}
                    placeholderTextColor="#B3B3B3"
                    className={cn(
                        'input',
                        error
                            ? 'border-error'
                            : isFocused
                            ? 'border-primary'
                            : 'border-gray-300',
                        secureTextEntry && 'pr-14'
                    )}
                />
                {secureTextEntry && (
                    <TouchableOpacity
                        className="absolute right-4 py-2"
                        onPress={() => setShowPassword(!showPassword)}
                    >
                        <Text className="text-xs font-semibold text-primary">
                            {showPassword ? 'Hide' : 'Show'}
                        </Text>
                    </TouchableOpacity>
                )}
            </View>
            {error && <Text className="text-xs text-error mt-1.5">{error}</Text>}
        </View>
    );
};

export default CustomInput;