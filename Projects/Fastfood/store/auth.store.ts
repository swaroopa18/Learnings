import { create } from 'zustand';
import { getCurrentUser } from '../lib/appwrite';
import { User } from '../types';

export { User };

type AuthState = {
    isAuthenticated: boolean;
    user: User | null;
    isLoading: boolean;

    setAuthenticated: (value: boolean) => void;
    setUser: (user: User | null) => void;
    setLoading: (loading: boolean) => void;

    fetchAuthenticatedUsers: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
    isAuthenticated: false,
    user: null,
    isLoading: false,
    setAuthenticated: (value) => set({ isAuthenticated: value }),
    setUser: (user) => set({ user, isAuthenticated: !!user }),
    setLoading: (loading) => set({ isLoading: loading }),
    fetchAuthenticatedUsers: async () => {
        set({ isLoading: true })

        try {
            const user = await getCurrentUser()
            if (user) {
                set({ isAuthenticated: true, user })
            } else {
                set({ isAuthenticated: false, user: null })
            }
        }
        catch (error) {
            set({ isAuthenticated: false, user: null })
        } finally {
            set({ isLoading: false })
        }
    }
}))

export default useAuthStore;