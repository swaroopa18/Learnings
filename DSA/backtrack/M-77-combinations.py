from typing import List

# APPROACH 1: Basic Backtracking with Array
# Time: O(k * C(n,k)) - C(n,k) combinations, each takes O(k) to copy
# Space: O(k) - recursion depth is k
class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        nums = [i for i in range(1, n + 1)]
        combinations = []

        def dfs(path, idx):
            if len(path) == k:
                combinations.append(path[:])  # O(k) copy operation
                return
            for i in range(idx, len(nums)):
                path.append(nums[i])
                dfs(path, i + 1)
                path.pop()

        dfs([], 0)
        return combinations


# APPROACH 2: Optimized Backtracking (Best for interviews)
# Time: O(k * C(n,k))
# Space: O(k) - recursion depth
# Note: Avoids creating nums array, works directly with integers
class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        combinations = []

        def dfs(path, idx):
            if len(path) == k:
                combinations.append(path[:])
                return
            # Pruning optimization: only continue if we have enough numbers left
            # We need k - len(path) more numbers, and we have n - idx + 1 available
            for i in range(idx, n + 1):
                if n - i + 1 < k - len(path):  # Not enough numbers left
                    break
                path.append(i)
                dfs(path, i + 1)
                path.pop()

        dfs([], 1)
        return combinations


# APPROACH 3: Include/Exclude Pattern
# Time: O(k * C(n,k))
# Space: O(n) - recursion depth can go to n in worst case
# Note: Binary tree exploration - at each number, decide to include or exclude
class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        combinations = []

        def dfs(path, idx):
            # Base case: found a valid combination
            if len(path) == k:
                combinations.append(path[:])
                return
            # Base case: exhausted all numbers
            if idx > n:
                return
            
            # Pruning: if we can't possibly reach k elements, stop early
            remaining = n - idx + 1
            needed = k - len(path)
            if remaining < needed:
                return
            
            # Include current number
            path.append(idx)
            dfs(path, idx + 1)
            path.pop()
            
            # Exclude current number
            dfs(path, idx + 1)

        dfs([], 1)
        return combinations


# APPROACH 4: Iterative with Bit Manipulation (Alternative)
# Time: O(k * C(n,k))
# Space: O(1) excluding output
# Note: Good for small n (n <= 20), uses bitmask to generate combinations
class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        combinations = []
        # Iterate through all possible bitmasks
        for mask in range(1 << n):
            if bin(mask).count('1') == k:  # Check if exactly k bits are set
                combination = []
                for i in range(n):
                    if mask & (1 << i):
                        combination.append(i + 1)
                combinations.append(combination)
        return combinations


"""
COMPARISON & RECOMMENDATIONS:

1. **Approach 1**: Good for understanding, but creates unnecessary array
   - Use when: Learning backtracking basics

2. **Approach 2**: RECOMMENDED for interviews
   - Most efficient and clean
   - Easy to explain and understand
   - Has pruning optimization built-in
   - Use when: Most practical situations

3. **Approach 3**: Include/exclude pattern
   - Good for understanding recursion tree
   - Slightly deeper recursion than Approach 2
   - Use when: Problem explicitly asks for this pattern

4. **Approach 4**: Bit manipulation
   - Only practical for small n (n <= 20)
   - Time complexity degrades badly: O(2^n * n)
   - Use when: n is very small or learning bit manipulation

KEY OPTIMIZATION:
The pruning check: if n - i + 1 < k - len(path): break
This stops early when there aren't enough numbers left to complete the combination.

Example: n=4, k=3, path=[1]
- At i=4: we need 2 more numbers, but only have 1 left (4-4+1=1)
- So we can skip i=4 entirely
"""