from typing import List


# APPROACH 1: Include/Exclude Pattern with Array
# Time: O(k * 2^9) = O(k * 512) - at most 2^9 subsets to explore
# Space: O(k) - recursion depth limited by k
class Solution:
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        nums = [x for x in range(1, 10)]
        result = []

        def backtrack(path, curr, idx):
            if curr == 0 and len(path) == k:
                result.append(path[:])
                return
            if len(path) == k or curr < 0 or idx >= len(nums):
                return
            
            path.append(nums[idx])
            backtrack(path, curr - nums[idx], idx + 1)
            path.pop()
            
            backtrack(path, curr, idx + 1)

        backtrack([], n, 0)
        return result


# APPROACH 2: For-loop Backtracking with Array
# Time: O(k * C(9,k)) - more efficient pruning
# Space: O(k)
class Solution:
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        nums = [x for x in range(1, 10)]
        result = []

        def backtrack(path, curr, idx):
            if curr == 0 and len(path) == k:
                result.append(path[:])
                return
            if len(path) == k or curr < 0:
                return
            
            for i in range(idx, len(nums)):
                path.append(nums[i])
                backtrack(path, curr - nums[i], i + 1)
                path.pop()

        backtrack([], n, 0)
        return result


# APPROACH 3: Optimized - Direct Integer Range (RECOMMENDED)
# Time: O(k * C(9,k))
# Space: O(k)
# Benefits: No array creation, cleaner code, better pruning
class Solution:
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        result = []

        def backtrack(path, remaining, start):
            if remaining == 0 and len(path) == k:
                result.append(path[:])
                return
            
            # Pruning conditions
            if len(path) == k:
                return
            if remaining < 0:
                return
            
            for num in range(start, 10):
                if num > remaining:
                    break
                
                path.append(num)
                backtrack(path, remaining - num, num + 1)
                path.pop()

        backtrack([], n, 1)
        return result


# APPROACH 4: Best Optimized with Multiple Pruning (INTERVIEW READY)
# Time: O(k * C(9,k))
# Space: O(k)
class Solution:
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        result = []

        def backtrack(path, remaining, start):
            # Success case
            if len(path) == k:
                if remaining == 0:
                    result.append(path[:])
                return
            
            # Pruning 1: Not enough numbers left to reach k
            if 10 - start < k - len(path):
                return
            
            # Pruning 2: Remaining sum is impossible
            # Minimum possible sum with (k - len(path)) numbers starting from start
            needed = k - len(path)
            min_sum = sum(range(start, start + needed))
            if remaining < min_sum:
                return
            
            # Pruning 3: Maximum possible sum is too small
            # Maximum sum using the largest available numbers
            max_sum = sum(range(10 - needed, 10))
            if remaining > max_sum:
                return
            
            for num in range(start, 10):
                # Pruning 4: Current number exceeds remaining
                if num > remaining:
                    break
                
                path.append(num)
                backtrack(path, remaining - num, num + 1)
                path.pop()

        backtrack([], n, 1)
        return result


# APPROACH 5: Math-based Early Termination (Alternative)
# Time: O(k * C(9,k))
# Space: O(k)
class Solution:
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        # Early validation: impossible cases
        # Min sum: 1+2+...+k = k(k+1)/2
        # Max sum: (10-k)+(10-k+1)+...+9 = k(19-k)/2
        min_possible = k * (k + 1) // 2
        max_possible = k * (19 - k) // 2
        
        if n < min_possible or n > max_possible:
            return []
        
        result = []

        def backtrack(path, remaining, start):
            if len(path) == k:
                if remaining == 0:
                    result.append(path[:])
                return
            
            # How many more numbers we need
            needed = k - len(path)
            
            for num in range(start, 10):
                # Skip if too large
                if num > remaining:
                    break
                
                # Skip if remaining numbers can't sum to target
                # Min sum of remaining slots: num+1, num+2, ..., num+needed-1
                min_future_sum = (needed - 1) * num + needed * (needed - 1) // 2
                if remaining - num < min_future_sum:
                    continue
                
                # Skip if max possible sum is too small
                # Max sum: use 9, 8, 7, ... (the largest available)
                max_future_sum = sum(range(10 - needed + 1, 10))
                if remaining - num > max_future_sum:
                    continue
                
                path.append(num)
                backtrack(path, remaining - num, num + 1)
                path.pop()

        backtrack([], n, 1)
        return result


"""
COMPARISON & RECOMMENDATIONS:

**Best for Interviews: APPROACH 3**
- Clean and easy to understand
- Good performance with basic pruning
- No unnecessary complexity
- Time: O(k * C(9,k)), Space: O(k)

**Most Optimized: APPROACH 4**
- Multiple pruning strategies
- Fastest in practice for edge cases
- Still readable and maintainable
- Use when: Performance is critical

**Mathematical Approach: APPROACH 5**
- Early validation before search
- Good for competitive programming
- Slightly more complex logic
- Use when: You want to show mathematical insight

KEY OPTIMIZATIONS EXPLAINED:

1. **num > remaining**: Skip if number exceeds what we need
2. **Not enough numbers left**: 10 - start < k - len(path)
3. **Min/Max sum pruning**: Check if target is achievable
4. **Early validation**: Check k*(k+1)/2 <= n <= k*(19-k)/2

EXAMPLE WALKTHROUGH:
k=3, n=7
- Min possible: 1+2+3 = 6 ✓
- Max possible: 7+8+9 = 24 ✓
- Valid combinations: [1,2,4] only

k=3, n=24
- Min possible: 6 ✓
- Max possible: 7+8+9 = 24 ✓
- Valid combinations: [7,8,9] only

k=3, n=5
- Min possible: 6 ✗
- Return [] immediately (impossible)

TIME COMPLEXITY BREAKDOWN:
- We explore at most C(9,k) combinations
- Each combination takes O(k) to build and copy
- Total: O(k * C(9,k))
- For k=5: C(9,5) = 126, so ~630 operations max

SPACE COMPLEXITY:
- Recursion depth: O(k)
- Path array: O(k)
- Total: O(k)
"""