#https://leetcode.com/problems/valid-palindrome/description/


# Two pointer approach
# TC: O(n)
# SC: O(1)
class Solution:
    def isPalindrome1(self, s: str) -> bool:
        n = len(s)
        l, r = 0, n - 1
        while l <= r:
            if not s[l].isalnum():
                l += 1
                continue
            if not s[r].isalnum():
                r -= 1
                continue
            if s[l].upper() == s[r].upper():
                l += 1
                r -= 1
            else:
                return False
        return True

#------------------------------------------------------------------------------------------------------

# Clean string first and apply two pointer approach
# TC: O(n)
# SC: O(n)
class Solution:
    def isPalindrome21(self, s: str) -> bool:
        filtered_s = ""
        for char in s:
            if char.isalnum():
                filtered_s += char

        filtered_s = filtered_s.lower()
        n = len(filtered_s)
        l, r = 0, n - 1
        while l <= r:
            if filtered_s[l] != filtered_s[r]:
                    return False
            l += 1
            r -= 1
        return True

#------------------------------------------------------------------------------------------------------

# Using regex
import re
class Solution:
    def isPalindrome(self, s: str) -> bool:
        filtered = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
        return filtered == filtered[::-1]


#------------------------------------------------------------------------------------------------------

# Using regex + two pointer
class Solution:
    def isPalindrome22(self, s: str) -> bool:
        def isValid(char: str) -> bool:
            return re.match(r'[a-zA-Z0-9]', char)
        filtered = [char.lower() for char in s if isValid(char)]
        n = len(filtered)
        l, r = 0, n - 1
        while l <= r:
            if filtered[l] != filtered[r]:
                    return False
            l += 1
            r -= 1
        return True

#------------------------------------------------------------------------------------------------------

# Recursion

import re


class Solution:
    def isValid(self, char: str) -> bool:
        return re.match(r"[a-zA-Z0-9]", char)

    def palindromeRecursive(self, ss: str, left, right):
        if left > right:
            return True
        if ss[left] != ss[right]:
            return False
        return self.palindromeRecursive(ss, left + 1, right - 1)

    def isPalindrome(self, s: str) -> bool:
        filtered = [char.lower() for char in s if self.isValid(char)]
        return self.palindromeRecursive(filtered, 0, len(filtered) - 1)
