from typing import List


# Approach 1: Sort by length and compare with shortest string
# Time: O(n * m * log n) where n = number of strings, m = length of shortest string
# Space: O(n) for sorting
class Solution1:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if len(strs) == 0:
            return ""
        
        # Sort strings by length to get the shortest one first
        sortedArray = sorted(strs, key=len)
        smallest = sortedArray[0]
        
        # Check each character position in the shortest string
        for i in range(len(smallest)):
            # Compare this position across all other strings
            for word in sortedArray[1:]:
                if word[i] != smallest[i]:
                    # Mismatch found, return prefix up to this point
                    return smallest[:i]
        
        # All characters matched, the shortest string is the common prefix
        return smallest


# Approach 2: Use first string as reference (more efficient)
# Time: O(n * m) where n = number of strings, m = length of first string
# Space: O(1)
class Solution2:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if len(strs) == 0:
            return ""
        
        first = strs[0]
        
        # Check each character position in the first string
        for i in range(len(first)):
            for word in strs[1:]:
                # Check if we've exceeded the word's length or characters don't match
                if len(word) <= i or word[i] != first[i]:
                    return first[:i]
        
        # All characters matched across all strings
        return first


# Improved version with better practices
class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        # Handle edge cases
        if not strs:
            return ""
        if len(strs) == 1:
            return strs[0]
        
        # Use the first string as reference
        prefix = strs[0]
        
        # Compare with each subsequent string
        for s in strs[1:]:
            # Shrink prefix until it matches the start of current string
            while not s.startswith(prefix):
                prefix = prefix[:-1]
                # If prefix becomes empty, no common prefix exists
                if not prefix:
                    return ""
        
        return prefix


# Alternative: Vertical scanning (character by character)
class SolutionVertical:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if not strs:
            return ""
        
        # Check each character position across all strings simultaneously
        for i in range(len(strs[0])):
            char = strs[0][i]
            # Verify this character matches in all other strings
            for s in strs[1:]:
                if i >= len(s) or s[i] != char:
                    return strs[0][:i]
        
        return strs[0]


# Example usage and testing
if __name__ == "__main__":
    test_cases = [
        (["flower", "flow", "flight"], "fl"),
        (["dog", "racecar", "car"], ""),
        (["interspecies", "interstellar", "interstate"], "inters"),
        (["a"], "a"),
        ([], ""),
    ]
    
    solution = Solution()
    
    for inputs, expected in test_cases:
        result = solution.longestCommonPrefix(inputs)
        status = "✓" if result == expected else "✗"
        print(f"{status} Input: {inputs}")
        print(f"  Expected: '{expected}', Got: '{result}'")
        print()