"""
================================================================================
NEXT GREATER ELEMENT I  (LeetCode 496)
================================================================================

# Problem
- For every element in nums1, find its next greater element to the right in
  nums2 (nums1 is always a subset of nums2). If none exists, answer is -1.


# Core Idea 💡
- Brute force checks, for each nums1[i], scans nums2 from scratch = O(n*m).
  Wasteful because we re-scan the same array over and over.
- Key observation: nums2 is fixed. If we precompute "next greater element"
  for EVERY number in nums2 once, we can answer each nums1 query in O(1)
  using a hashmap lookup.
- Pattern: Monotonic Stack (decreasing stack) + Hashmap.
  This is the classic pattern for "next greater / next smaller element"
  problems.


# Algorithm 📝
1. Create an empty hashmap `next_greater` (num -> its next greater number).
2. Create an empty stack `stack` (will hold numbers waiting for their
   "next greater" to appear).
3. Loop through nums2 from left to right, current number = nums2[i]:
     a. While stack is not empty AND top of stack < nums2[i]:
          - Pop the top element `x`.
          - Record next_greater[x] = nums2[i]  (we just found its answer!)
     b. Push nums2[i] onto the stack (it's now waiting for ITS next greater).
4. After the loop, anything left in the stack has no next greater -> map
   lookup will naturally give -1 via .get(num, -1).
5. For each num in nums1, look up next_greater.get(num, -1) and collect
   results.


# Explanation 🧠
- Think of the stack as a "waiting line" of numbers that haven't found
  a bigger number yet, kept in DECREASING order from bottom to top.
- Example: nums2 = [1, 3, 4, 2]
    i=0, num=1: stack empty -> push. stack = [1]
    i=1, num=3: top(1) < 3 -> pop 1, next_greater[1] = 3. stack empty -> push 3.
                stack = [3]
    i=2, num=4: top(3) < 4 -> pop 3, next_greater[3] = 4. push 4.
                stack = [4]
    i=3, num=2: top(4) is NOT < 2 -> stop popping. push 2.
                stack = [4, 2]
    End of loop. Remaining in stack (4, 2) never found anything bigger,
    so they simply won't be in the map -> default -1.
    Final map: {1: 3, 3: 4}
- Why it works: whenever we see a new number, it can ONLY be the "next
  greater" for numbers smaller than it that are still waiting in the
  stack. So we pop all smaller numbers below it, record their answer,
  then push the new number to wait for its own future match.
- Each number is pushed once and popped at most once -> that's why total
  work across the whole loop is linear, not quadratic.
- `next_greater` variable: stores the final answer for every number in
  nums2 (computed once).
- `stack` variable: temporary holding area of numbers still searching
  for a bigger number to their right.


# Time Complexity ⏱️
- TC: O(n + m)  where n = len(nums1), m = len(nums2)
- Why? Each element of nums2 is pushed onto the stack exactly once and
  popped at most once -> O(m) total for building the map. Then O(n) for
  the final lookups in nums1. Compare to brute force's O(n*m).


# Space Complexity 💾
- SC: O(m)
- Why? The hashmap can store up to m entries, and the stack can hold up
  to m elements in the worst case (e.g., strictly increasing array).


# Pros ✅
- Linear time — huge win over brute force when nums2 is large.
- Very reusable pattern: works for "next greater," "next smaller,"
  "previous greater," "previous smaller" with minor tweaks (just flip
  the comparison or iterate direction).
- Clean separation: solve the general problem on nums2 once, then
  answer queries in O(1) each.


# Cons ❌
- Uses extra space for stack + hashmap (not in-place).
- Slight overkill if nums2 is tiny — brute force may be simpler to write
  under time pressure, though still worse asymptotically.
- Only works cleanly because all values are assumed unique (as per
  problem constraints); duplicates would need modification (e.g., store
  indices instead of values in the stack/map).


# Interview Tips 🎯
- Trigger phrase to watch for: "next greater element," "next warmer day,"
  "span of stock prices," "first element to the right that is bigger/
  smaller" -> these all scream Monotonic Stack.
- Interviewer follow-ups:
    - "What if there are duplicates?" -> use indices instead of values.
    - "What about circular array (Next Greater Element II)?" -> iterate
      2*n times using modulo indexing, same stack logic.
    - "Can you do next SMALLER element?" -> flip the comparison to
      `stack[-1] > nums2[i]`.
    - "Can you find it without extra map, just from indices?" -> yes,
      store indices in the stack instead of values.
- Optimization: if nums1 is much smaller than nums2, this approach is
  already optimal — no way to beat O(m) since you must scan nums2 once.


# Pattern Recognition 🔍
- Keywords: "next greater," "next smaller," "previous greater," "daily
  temperatures," "stock span," "largest rectangle in histogram,"
  "remove k digits" -> all Monotonic Stack problems.
- Signal: whenever you need to find the nearest larger/smaller element
  to the left/right in O(n), think Monotonic Stack immediately.


# Remember This ⭐
"Decreasing stack pops when a BIGGER guy walks in — that bigger guy IS
the answer for everyone it just kicked out." Push what's waiting,
pop-and-record the moment something taller shows up. That's the whole
trick.


# Comparison: Brute Force vs Monotonic Stack ⚖️
- Brute Force (Approach 1 below):
    - For each nums1[i], find it in nums2, then walk forward until a
      bigger number is found (or end of array).
    - TC: O(n * m) worst case — for every nums1 element, you may walk
      the entire nums2 array again.
    - SC: O(1) extra (ignoring output array).
    - Fine for small inputs, but slow / repeats work when nums2 is large
      or nums1 has many elements.
- Monotonic Stack (Approach 2 below) — RECOMMENDED:
    - Precomputes the answer for every number in nums2 ONCE, then does
      O(1) hashmap lookups for nums1.
    - TC: O(n + m), SC: O(m).
    - Strictly better asymptotically and the "expected" interview
      answer for this problem.
- Verdict: Always prefer the monotonic stack approach in an interview —
  mention brute force first to show you understand the naive way, then
  optimize into the stack approach to show pattern recognition.
================================================================================
"""

from typing import List


class SolutionBruteForce:
    """
    Approach 1: Brute Force
    -----------------------
    For each number in nums1, locate it inside nums2, then scan forward
    from that position until a strictly greater number is found.

    TC: O(n * m)   where n = len(nums1), m = len(nums2)
    SC: O(1) extra space (not counting the output list)
    """

    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        answers = []
        for i in range(len(nums1)):
            j = 0
            # find nums1[i] inside nums2
            while nums1[i] != nums2[j]:
                j += 1
            # scan forward for the first greater number
            while j < len(nums2):
                if nums1[i] < nums2[j]:
                    answers.append(nums2[j])
                    break
                j += 1
            if j == len(nums2):
                answers.append(-1)
        return answers


class SolutionMonotonicStack:
    """
    Approach 2: Monotonic Stack + Hashmap (Optimal, Recommended)
    --------------------------------------------------------------
    Precompute the "next greater element" for every number in nums2
    using a decreasing monotonic stack, store results in a hashmap,
    then answer each nums1 query in O(1).

    TC: O(n + m)
    SC: O(m)
    """

    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        next_greater = {}
        stack = []
        for i in range(len(nums2)):
            while stack and stack[-1] < nums2[i]:
                next_greater[stack[-1]] = nums2[i]
                stack.pop()
            stack.append(nums2[i])
        return [next_greater.get(num, -1) for num in nums1]


if __name__ == "__main__":
    brute = SolutionBruteForce()
    optimal = SolutionMonotonicStack()

    test_cases = [
        ([4, 1, 2], [1, 3, 4, 2]),   # expected [-1, 3, -1]
        ([2, 4], [1, 2, 3, 4]),      # expected [3, -1]
    ]

    for nums1, nums2 in test_cases:
        print("nums1:", nums1, "nums2:", nums2)
        print("  Brute Force      ->", brute.nextGreaterElement(nums1, nums2))
        print("  Monotonic Stack  ->", optimal.nextGreaterElement(nums1, nums2))
        print()