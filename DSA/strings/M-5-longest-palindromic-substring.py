class Solution:
    def longestPalindrome(self, s: str) -> str:
        """
        Find the longest palindromic substring in s.
        
        Current approach: Expand Around Center
        Time: O(n²), Space: O(1)
        
        Issue with current code: Doesn't handle single characters properly
        when no expansion is possible.
        """
        n = len(s)
        longest = ""
        
        # Check odd-length palindromes (single center)
        for i in range(n):
            left, right = i - 1, i + 1
            curr = s[i]  # Start with center character
            
            while left >= 0 and right < n:
                if s[left] != s[right]:
                    break
                curr = s[left : right + 1]
                left -= 1
                right += 1
            
            if len(curr) > len(longest):
                longest = curr
        
        # Check even-length palindromes (two centers)
        for i in range(n):
            left, right = i, i + 1
            curr = ""
            
            while left >= 0 and right < n:
                if s[left] != s[right]:
                    break
                curr = s[left : right + 1]
                left -= 1
                right += 1
            
            if len(curr) > len(longest):
                longest = curr
        
        return longest


# ============================================================================
# BEST APPROACH 1: Optimized Expand Around Center
# ============================================================================
class Solution_Best:
    def longestPalindrome(self, s: str) -> str:
        """
        Time: O(n²) - worst case, but efficient in practice
        Space: O(1) - only store indices
        
        Best for: Most interview scenarios, clean and intuitive
        """
        def expand_around_center(left: int, right: int) -> int:
            """Expand outward and return length of palindrome."""
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            return right - left - 1  # Length of palindrome
        
        if not s:
            return ""
        
        start = 0
        max_len = 0
        
        for i in range(len(s)):
            # Odd-length palindromes (single center)
            len1 = expand_around_center(i, i)
            # Even-length palindromes (two centers)
            len2 = expand_around_center(i, i + 1)
            
            curr_max = max(len1, len2)
            
            if curr_max > max_len:
                max_len = curr_max
                # Calculate start position from center
                start = i - (curr_max - 1) // 2
        
        return s[start : start + max_len]


# ============================================================================
# APPROACH 2: Dynamic Programming
# ============================================================================
class Solution_DP:
    def longestPalindrome(self, s: str) -> str:
        """
        Time: O(n²)
        Space: O(n²) - DP table
        
        Best for: When you need to check if multiple substrings are palindromes
        """
        n = len(s)
        if n < 2:
            return s
        
        # dp[i][j] = True if s[i:j+1] is a palindrome
        dp = [[False] * n for _ in range(n)]
        start = 0
        max_len = 1
        
        # Every single character is a palindrome
        for i in range(n):
            dp[i][i] = True
        
        # Check two-character substrings
        for i in range(n - 1):
            if s[i] == s[i + 1]:
                dp[i][i + 1] = True
                start = i
                max_len = 2
        
        # Check substrings of length 3 and above
        for length in range(3, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1  # End index
                
                # s[i:j+1] is palindrome if s[i] == s[j] and s[i+1:j] is palindrome
                if s[i] == s[j] and dp[i + 1][j - 1]:
                    dp[i][j] = True
                    start = i
                    max_len = length
        
        return s[start : start + max_len]


# ============================================================================
# APPROACH 3: Manacher's Algorithm (Advanced)
# ============================================================================
class Solution_Manacher:
    def longestPalindrome(self, s: str) -> str:
        """
        Time: O(n) - optimal!
        Space: O(n)
        
        Best for: Large inputs where performance is critical
        More complex but theoretically optimal
        """
        # Preprocess: insert '#' between characters
        # "babad" -> "#b#a#b#a#d#"
        t = '#'.join(f'^{s}$')
        n = len(t)
        
        # p[i] = radius of palindrome centered at i
        p = [0] * n
        center = 0  # Center of rightmost palindrome
        right = 0   # Right boundary of rightmost palindrome
        
        max_len = 0
        center_index = 0
        
        for i in range(1, n - 1):
            # Mirror of i with respect to center
            mirror = 2 * center - i
            
            # If i is within right boundary, use previously computed values
            if i < right:
                p[i] = min(right - i, p[mirror])
            
            # Try to expand palindrome centered at i
            while t[i + (1 + p[i])] == t[i - (1 + p[i])]:
                p[i] += 1
            
            # Update center and right boundary if expanded past right
            if i + p[i] > right:
                center = i
                right = i + p[i]
            
            # Track longest palindrome
            if p[i] > max_len:
                max_len = p[i]
                center_index = i
        
        # Extract original palindrome
        start = (center_index - max_len) // 2
        return s[start : start + max_len]


# ============================================================================
# COMPARISON & WHEN TO USE EACH
# ============================================================================
"""
1. EXPAND AROUND CENTER (Solution_Best) ⭐ RECOMMENDED FOR INTERVIEWS
   Pros: Clean, intuitive, O(1) space, easy to explain
   Cons: O(n²) time
   Use when: Default choice for interviews

2. DYNAMIC PROGRAMMING (Solution_DP)
   Pros: Stores all palindrome information, can answer multiple queries
   Cons: O(n²) space, slower in practice
   Use when: Need to check multiple substrings for palindromes

3. MANACHER'S ALGORITHM (Solution_Manacher)
   Pros: Optimal O(n) time complexity
   Cons: Complex, harder to implement correctly, not intuitive
   Use when: Very large inputs (n > 10^5), optimization is critical

Test cases:
- "babad" -> "bab" or "aba"
- "cbbd" -> "bb"
- "a" -> "a"
- "ac" -> "a" or "c"
- "racecar" -> "racecar"
- "abcba" -> "abcba"
"""