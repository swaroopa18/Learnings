import { ImageSourcePropType } from 'react-native';

export interface User {
  $id: string;
  name: string;
  email: string;
  avatar?: string;
  accountId?: string;
  [key: string]: any;
}

export interface TabBarIconProps {
  focused?: boolean;
  icon?: ImageSourcePropType | any;
  title?: string;
  color?: string;
  size?: number;
}

