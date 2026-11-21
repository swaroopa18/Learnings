import { Image, Text, TouchableOpacity, View } from 'react-native';

const CartButton = () => {
    const noOfItems = 10;
    return (
        <TouchableOpacity className='cart-btn' onPress={() => { }}>
            <Image
                source={{ uri: "https://cdn-icons-png.flaticon.com/512/263/263142.png" }}
                className='size-5'
                resizeMode='contain'
                style={{ tintColor: '#FFFFFF' }}
            />
            {noOfItems > 0 ? (
                <View className='cart-badge'>
                    <Text className='small-bold text-white'>{noOfItems}</Text>
                </View>
            ) : null}
        </TouchableOpacity>
    );
};

export default CartButton;