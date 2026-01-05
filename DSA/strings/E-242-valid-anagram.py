
from collections import Counter


# Approach 1: Two Hash Maps (Your First Solution)
# Time: O(n + m), Space: O(n + m)
class Solution1:
    def isAnagram(self, s: str, t: str) -> bool:
        """
        Strategy: Build frequency maps for both strings and compare them.
        
        Pros: Clear logic, easy to understand
        Cons: Redundant - we check both maps separately
        Note: The double loop at the end is unnecessary
        """
        smap, tmap = {}, {}

        # Build frequency map for string s
        for char in s:
            smap[char] = smap.get(char, 0) + 1
        
        # Build frequency map for string t
        for char in t:
            tmap[char] = tmap.get(char, 0) + 1
        
        # Check if all characters in smap match tmap
        for char in smap:
            if tmap.get(char, 0) != smap[char]:
                return False
        
        # Check if all characters in tmap match smap
        # This catches cases where t has extra characters not in s
        for char in tmap:
            if smap.get(char, 0) != tmap[char]:
                return False
        
        return True


# Approach 2: Single Hash Map with Increment/Decrement
# Time: O(n + m), Space: O(n)
class Solution2:
    def isAnagram(self, s: str, t: str) -> bool:
        """
        Strategy: Use one map, increment for s, decrement for t.
        If anagram, all counts should be zero.
        
        Pros: More elegant, single map
        Cons: Doesn't catch length mismatch early
        
        ISSUE: This has a bug! It doesn't check if len(s) == len(t)
        Example: s="a", t="ab" would return False (correct by accident)
        But s="ab", t="a" would return False checking "b": 1 != 0 (correct)
        Actually works, but less efficient than early length check
        """
        hmap = {}
        
        # Increment count for each character in s
        for char in s:
            hmap[char] = hmap.get(char, 0) + 1
        
        # Decrement count for each character in t
        for char in t:
            hmap[char] = hmap.get(char, 0) - 1

        # All values should be 0 if strings are anagrams
        return all(value == 0 for value in hmap.values())


# Approach 3: Fixed Array (Optimal for lowercase letters only)
# Time: O(n + m), Space: O(1) - fixed 26 size
class Solution3:
    def isAnagram(self, s: str, t: str) -> bool:
        """
        Strategy: Use array of size 26 for lowercase English letters.
        
        Pros: O(1) space, very fast in practice
        Cons: Only works for lowercase a-z
        
        Note: ord('a') = 97, so ord(char) - ord('a') maps:
              'a' -> 0, 'b' -> 1, ..., 'z' -> 25
        """
        counts = [0] * 26
        
        # Increment for characters in s
        for char in s:
            counts[ord(char) - ord("a")] += 1
        
        # Decrement for characters in t
        for char in t:
            counts[ord(char) - ord("a")] -= 1

        # All counts should be 0
        return all(value == 0 for value in counts)


# Improved versions with best practices
class SolutionImproved:
    def isAnagram(self, s: str, t: str) -> bool:
        """
        Most Pythonic: Direct comparison of Counter objects
        Time: O(n + m), Space: O(n)
        """
        # Early exit: different lengths can't be anagrams
        if len(s) != len(t):
            return False
        
        return Counter(s) == Counter(t)


class SolutionOptimized:
    def isAnagram(self, s: str, t: str) -> bool:
        """
        Optimized hash map approach with early exit
        Time: O(n + m), Space: O(n)
        """
        # Early length check saves unnecessary computation
        if len(s) != len(t):
            return False
        
        counts = {}
        
        # Single pass: increment for s, decrement for t
        for char in s:
            counts[char] = counts.get(char, 0) + 1
        
        for char in t:
            if char not in counts:
                return False  # Early exit: char in t not in s
            counts[char] -= 1
            if counts[char] < 0:
                return False  # Early exit: too many of this char in t
        
        return True