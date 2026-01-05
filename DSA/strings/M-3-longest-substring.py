
# Approach 1: Hash Map with Manual Window Adjustment
# Time: O(n), Space: O(min(n, m)) where m is charset size
class Solution1:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        Strategy: Use hash map to store character indices.
        When duplicate found, shrink window from left.
        
        Issues with this implementation:
        1. Maintains both 'count' and map, which is redundant
        2. The while loop to find duplicate is less efficient
        3. Manual count tracking can be error-prone
        
        How it works:
        - hmap stores: character -> last seen index
        - When duplicate found, move start pointer past the duplicate
        - Track count of characters in current window
        """
        hmap = {}
        max_count, start = 0, 0
        count = 0
        
        for i in range(len(s)):
            if s[i] not in hmap:
                hmap[s[i]] = i
                count += 1
            else:
                max_count = max(max_count, count)
                
                while s[i] != s[start]:
                    del hmap[s[start]]
                    count -= 1
                    start += 1
                
                start += 1
                hmap[s[i]] = i
        return max(max_count, count)


# Approach 2: Set with Sliding Window (Cleaner)
# Time: O(n), Space: O(min(n, m))
class Solution2:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        Strategy: Use set for O(1) lookup, sliding window technique.
        
        Pros:
        - Cleaner code, no manual count tracking
        - Uses right - left + 1 for window size (more intuitive)
        - Set is simpler than map when we only need existence check
        
        How it works:
        - seen: set of characters in current window [left, right]
        - right pointer expands the window
        - When duplicate found, contract from left until duplicate removed
        - Window size = right - left + 1
        """
        seen = set()
        left = 0
        max_len = 0

        for right in range(len(s)):
            while s[right] in seen:
                seen.remove(s[left])
                left += 1
            
            seen.add(s[right])
            max_len = max(max_len, right - left + 1)

        return max_len


# Approach 3: Optimized Hash Map (Skip unnecessary moves)
# Time: O(n), Space: O(min(n, m))
class Solution3:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        Strategy: Store indices in map, jump left pointer directly.
        
        Optimization: Instead of moving left pointer one by one,
        jump directly to position after the previous occurrence.
        
        Example: "abcabcbb"
        - At second 'a' (index 3), jump left from 0 to 1 (index of 'a' + 1)
        - This skips unnecessary iterations
        
        Key: left = max(left, last_seen[char] + 1)
        The max() ensures we never move left pointer backwards
        """
        char_index = {}
        left = 0
        max_len = 0
        
        for right in range(len(s)):
            char = s[right]
            
            # If character seen and within current window
            if char in char_index and char_index[char] >= left:
                # Jump left pointer to position after last occurrence
                left = char_index[char] + 1
            
            # Update character's last seen index
            char_index[char] = right
            
            # Update maximum length
            max_len = max(max_len, right - left + 1)
        
        return max_len


# Approach 4: Most Pythonic (using max with generator)
class SolutionPythonic:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        Most concise while maintaining clarity.
        """
        if not s:
            return 0
        
        seen = {}
        left = max_len = 0
        
        for right, char in enumerate(s):
            if char in seen and seen[char] >= left:
                left = seen[char] + 1
            seen[char] = right
            max_len = max(max_len, right - left + 1)
        
        return max_len
