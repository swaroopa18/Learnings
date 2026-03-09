from typing import List


class SolutionSquareAndSort:
    """
    Approach: Square each element, then sort.
    Time:  O(n log n)
    Space: O(1) extra
    """

    def sortedSquares(self, nums: List[int]) -> List[int]:
        for idx in range(len(nums)):
            nums[idx] = nums[idx] * nums[idx]
        return sorted(nums)


class SolutionTwoPointers:
    """
    Approach: Two pointers — fill result array from the back.
    Exploits the fact that the input is already sorted.
    Time:  O(n)
    Space: O(n)
    """

    def sortedSquares(self, nums: List[int]) -> List[int]:
        n = len(nums)
        res = [0] * n
        l, r = 0, n - 1
        pos = n - 1
        while l <= r:
            if abs(nums[l]) > abs(nums[r]):
                res[pos] = nums[l] * nums[l]
                l += 1
            else:
                res[pos] = nums[r] * nums[r]
                r -= 1
            pos -= 1
        return res