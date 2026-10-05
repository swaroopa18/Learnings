"""
LeetCode 739 - Daily Temperatures
----------------------------------
Given a list of daily temperatures, return a list `answer` such that
answer[i] is the number of days you have to wait after day i to get a
warmer temperature. If there is no future day for which this is
possible, answer[i] = 0.

Three approaches are given below, from brute force to optimal.
"""

from typing import List


class SolutionBruteForce:
    """
    Approach 1: Brute Force (Nested Loops)
    ---------------------------------------
    For each day i, scan forward until a warmer day is found.

    Time Complexity:  O(n^2)  -- worst case (strictly decreasing temps),
                                 every pair (i, j) is checked.
    Space Complexity: O(1)    -- excluding the output array.

    Good for understanding the problem, but too slow for large inputs
    (e.g. n = 10^5, as in LeetCode's constraints).
    """

    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        answer = [0] * len(temperatures)
        for i in range(len(temperatures)):
            for j in range(i + 1, len(temperatures)):
                if temperatures[i] < temperatures[j]:
                    answer[i] = j - i
                    break
        return answer


class SolutionStackForward:
    """
    Approach 2: Monotonic Stack (your version, cleaned up)
    --------------------------------------------------------
    Same core idea as the classic monotonic stack solution, just walking
    the array forward and comparing adjacent + stacked indices. It works,
    but mixes two ideas (adjacent-pair check + stack) which makes it a
    bit harder to follow than the standard version below.

    Time Complexity:  O(n) -- each index is pushed and popped at most once.
    Space Complexity: O(n) -- for the stack.
    """

    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        if n == 0:
            return []
        answers = [0] * n
        stack = []
        for i in range(1, n):
            if temperatures[i - 1] < temperatures[i]:
                answers[i - 1] = 1
                while stack:
                    lastIdx = stack[-1]
                    if temperatures[lastIdx] < temperatures[i]:
                        answers[lastIdx] = i - lastIdx
                        stack.pop()
                    else:
                        break
            else:
                stack.append(i - 1)
        return answers


class Solution:
    """
    Approach 3 (RECOMMENDED): Standard Monotonic Decreasing Stack
    -----------------------------------------------------------------
    Idea:
      - Keep a stack of indices whose temperatures are still "waiting"
        for a warmer day. The stack is kept monotonically DECREASING
        in temperature (top of stack = smallest recent temp seen).
      - For each new day i:
          * While the stack is non-empty and today's temperature is
            warmer than the temperature at the index on top of the
            stack, we've found the answer for that index: pop it and
            set answer[popped] = i - popped.
          * Push the current index i onto the stack.
      - Any index left on the stack at the end never finds a warmer
        day, so its answer stays 0 (the initial value).

    Why it's better:
      - Single, clean pass with one loop and one simple invariant
        (monotonic stack), instead of interleaving an adjacent-pair
        check with a stack-resolution loop.
      - Each index is pushed exactly once and popped at most once,
        so total work across the whole run is O(n), not just "usually
        fast" -- it's a tight worst-case bound.

    Time Complexity:  O(n)  -- each index pushed once, popped at most once.
    Space Complexity: O(n)  -- for the stack (worst case: strictly
                                decreasing temperatures never get popped
                                until the end, e.g. [5, 4, 3, 2, 1]).
    """

    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        answer = [0] * n
        stack = []  # stores indices, temperatures[stack] is decreasing

        for i, temp in enumerate(temperatures):
            while stack and temperatures[stack[-1]] < temp:
                prev_index = stack.pop()
                answer[prev_index] = i - prev_index
            stack.append(i)

        return answer