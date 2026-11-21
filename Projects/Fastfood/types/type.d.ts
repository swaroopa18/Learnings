declare interface User {
  $id: string;
  name: string;
  email: string;
  avatar?: string;
  accountId?: string;
  [key: string]: any;
}

declare interface TabBarIconProps {
  focused?: boolean;
  icon?: any;
  title?: string;
  color?: string;
  size?: number;
}
