from typing import List


class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        subsets = []

        def backtrack(idx, path):
            subsets.append(path[:])
            if idx >= len(nums):
                return
            for i in range(idx, len(nums)):
                if i != idx and nums[i] == nums[i - 1]:
                    continue
                path.append(nums[i])
                backtrack(i + 1, path)
                path.pop()

        backtrack(0, [])
        return subsets
