# APPROACH 1: Two-pass with prefix + reverse suffix arrays
# Build a prefix sum array left-to-right, and a reverse suffix sum array right-to-left.
# At pivot index i: prefix_sums[i] includes nums[i], and rev_sums[n-i-1] also includes nums[i].
# So the condition prefix_sums[i] == rev_sums[n-i-1] means:
#   left_sum_including_i == right_sum_including_i → both sides "meet" at i (with overlap).
# This works because the overlap (nums[i]) is symmetric on both sides.
# Space: O(n) for both arrays. Time: O(n).
from typing import List


class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        n = len(nums)
        prefix_sums = []
        curr_sum = 0
        for num in nums:
            curr_sum += num
            prefix_sums.append(curr_sum)  # prefix_sums[i] = sum(nums[0..i])
       
        rev_sums = []
        curr_sum = 0
        for num in nums[::-1]:
            curr_sum += num
            rev_sums.append(curr_sum)     # rev_sums[j] = sum(nums[n-1-j..n-1])
                                          # so rev_sums[n-1-i] = sum(nums[i..n-1])

        for i in range(n):
            if prefix_sums[i] == rev_sums[n-i-1]:  # both include nums[i], so overlap cancels out
                return i
        return -1


# APPROACH 2: One prefix array, shrinking total from the right
# Build prefix sums once. Then walk through, maintaining a "remaining right total"
# that shrinks by nums[i] after each check.
# At index i, curr_sum represents sum(nums[i..n-1]) — i.e. the right side including nums[i].
# Condition: prefix_sums[i] == curr_sum means left (including i) == right (including i).
# Same symmetric overlap logic as Approach 1, just without the second array.
# Space: O(n) for prefix array. Time: O(n).
class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        n = len(nums)
        prefix_sums = []
        curr_sum = 0
        for num in nums:
            curr_sum += num
            prefix_sums.append(curr_sum)

        curr_sum = prefix_sums[n - 1]   # start = total sum = right side including nums[0]
        for i in range(n):
            if prefix_sums[i] == curr_sum:  # left (0..i) == right (i..n-1)
                return i
            curr_sum -= nums[i]             # shrink right side: exclude nums[i] for next iteration
        return -1


# APPROACH 3: O(1) space — update left and right simultaneously (subtract-after-check)
# right_sum starts as the total. At each index i, we first add nums[i] to left_sum,
# then check if left_sum == right_sum.
# At the moment of the check:
#   left_sum  = sum(nums[0..i])     (includes nums[i])
#   right_sum = sum(nums[i..n-1])   (still includes nums[i], not yet removed)
# Again, nums[i] appears on both sides — same symmetric overlap as above.
# After the check, right_sum -= nums[i] to "consume" the current element.
# Space: O(1). Time: O(n).
class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        n = len(nums)
        left_sum, right_sum = 0, sum(nums)  # right_sum = total sum initially

        for i in range(n):
            left_sum += nums[i]             # extend left to include nums[i]
            if left_sum == right_sum:       # check: both sides include nums[i]
                return i
            right_sum -= nums[i]            # shrink right to exclude nums[i]

        return -1


# APPROACH 4: O(1) space — subtract-before-check (cleanest semantics)
# Unlike Approach 3, here we subtract nums[i] from right_sum BEFORE the check.
# At the moment of the check:
#   left_sum  = sum(nums[0..i-1])   (excludes nums[i])
#   right_sum = sum(nums[i+1..n-1]) (excludes nums[i])
# This directly matches the problem definition: left side strictly excludes pivot,
# right side strictly excludes pivot. No overlap — most intuitive correctness.
# After the check, we grow left_sum to include nums[i] for the next iteration.
# Space: O(1). Time: O(n).
class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        n = len(nums)
        left_sum, right_sum = 0, sum(nums)

        for i in range(n):
            right_sum -= nums[i]            # remove nums[i] from right → right excludes pivot
            if left_sum == right_sum:       # clean check: strictly left == strictly right
                return i
            left_sum += nums[i]             # grow left to include nums[i] for next step

        return -1