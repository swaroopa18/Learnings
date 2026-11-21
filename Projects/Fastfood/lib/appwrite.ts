import { Account, Avatars, Client, Databases, ID, Query } from 'react-native-appwrite';
import { User } from '../types';

export const appwriteConfig = {
  endpoint: process.env.EXPO_PUBLIC_APPWRITE_END_POINT!,
  projectId: process.env.EXPO_PUBLIC_APPWRITE_PROJECT_ID!,
  platform: 'com.jsm.foodordering',
  databaseId: '6b012616001916e784ce',
  userCollectionId: '6b012663001011d4b001',
};

const client = new Client();

client
  .setEndpoint(appwriteConfig.endpoint)
  .setProject(appwriteConfig.projectId)
  .setPlatform(appwriteConfig.platform);

export const account = new Account(client);
export const databases = new Databases(client);
export const avatar = new Avatars(client);

interface CreateUserParams {
  email: string;
  password: string;
  name: string;
}

interface SignInParams {
  email: string;
  password: string;
}

export const createUser = async ({ email, password, name }: CreateUserParams) => {
  try {
    try {
      await account.deleteSession('current');
    } catch {
    }

    let newAccount;
    try {
      newAccount = await account.create(ID.unique(), email, password, name);
    } catch (accountError: any) {
      if (accountError?.code === 409) {
        await signin({ email, password });
        newAccount = await account.get();
      } else {
        throw accountError;
      }
    }

    if (!newAccount) throw new Error('Failed to create account');

    try {
      await signin({ email, password });
    } catch {
      // Session might already be established
    }

    // 3. Build avatar URL from user initials
    const avatarUrl = avatar.getInitialsURL(name).toString();

    // 4. Create user profile document in Appwrite Database
    try {
      const newUser = await databases.createDocument(
        appwriteConfig.databaseId,
        appwriteConfig.userCollectionId,
        ID.unique(),
        {
          accountId: newAccount.$id,
          email,
          name,
          avatar: avatarUrl,
        }
      );
      return newUser;
    } catch (dbError) {
      console.warn('Document creation warning:', dbError);
      return newAccount;
    }
  } catch (error) {
    console.error('createUser error:', error);
    throw error;
  }
};

export const signin = async ({ email, password }: SignInParams) => {
  try {
    // If a session already exists, delete it first to prevent conflict
    try {
      await account.deleteSession('current');
    } catch {
      // Ignore if no session active
    }

    const session = await account.createEmailPasswordSession(email, password);
    return session;
  } catch (error) {
    console.error('signin error:', error);
    throw error;
  }
};

export const signOut = async () => {
  try {
    await account.deleteSession('current');
  } catch (error) {
    console.error('signOut error:', error);
    throw error;
  }
};

export const getCurrentUser = async (): Promise<User | null> => {
  try {
    const currentAccount = await account.get();
    if (!currentAccount) return null;

    try {
      const currentUser = await databases.listDocuments(
        appwriteConfig.databaseId,
        appwriteConfig.userCollectionId,
        [Query.equal('accountId', currentAccount.$id)]
      );

      if (currentUser && currentUser.documents.length > 0) {
        return currentUser.documents[0] as unknown as User;
      }
    } catch {
      // Fallback to account info if database document query fails
    }

    return currentAccount as unknown as User;
  } catch {
    return null;
  }
};