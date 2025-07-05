# https://leetcode.com/problems/product-of-array-except-self/description/
from typing import List


# SOLUTION 1: Three Arrays Approach
# TC: O(3n) SC: O(3n)
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        prefix, suffix, result = [1] * len(nums), [1] * len(nums), [1] * len(nums)

        for i in range(len(nums)):
            if i == 0:
                prefix[i] = nums[i]
            else:
                prefix[i] = prefix[i - 1] * nums[i]

        for i in range(len(nums) - 1, -1, -1):
            if i == len(nums) - 1:
                suffix[i] = nums[i]
            else:
                suffix[i] = suffix[i + 1] * nums[i]

        for i in range(len(nums)):
            if i == 0:
                result[i] = suffix[i + 1]
            elif i == len(nums) - 1:
                result[i] = prefix[i - 1]
            else:
                result[i] = prefix[i - 1] * suffix[i + 1]
        return result

# SOLUTION 2: Space-Optimized Approach
# TC: O(2n) SC: O(n)
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        result = [1] * len(nums)

        for i in range(1, len(nums)):
            result[i] = result[i - 1] * nums[i - 1]

        mult = 1
        for i in range(len(nums) - 2, -1, -1):
            mult = mult * nums[i + 1]
            result[i] = result[i] * mult

        return result

# SOLUTION 3: Most Readable Version (Cleaner logic)
# TC: O(n) SC: O(1)
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        result = [1] * n
        
        # Calculate left products
        left_product = 1
        for i in range(n):
            result[i] = left_product
            left_product *= nums[i]
        
        # Calculate and multiply right products
        right_product = 1
        for i in range(n - 1, -1, -1):
            result[i] *= right_product
            right_product *= nums[i]
        
        return result
