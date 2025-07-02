#https://leetcode.com/problems/best-time-to-buy-and-sell-stock/

import math
from typing import List

# -----------------------------------------------
# 🔴 Brute Force Approach
# -----------------------------------------------
# Time Complexity: O(n^2)
# Space Complexity: O(1)
#
# Description:
# This approach tries every possible pair (buy day i, sell day j)
# and calculates the profit. It keeps track of the maximum profit found.
# It is not efficient for large inputs due to the nested loop.
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        maxProfit = 0
        for i in range(0, len(prices)):
            for j in range(i + 1, len(prices)):
                maxProfit = max(maxProfit, prices[j] - prices[i])
        return maxProfit

# -----------------------------------------------
# ✅ Greedy / Min Price Approach
# -----------------------------------------------
# Time Complexity: O(n)
# Space Complexity: O(1)
#
# Description:
# Track the lowest price so far as the potential buy price.
# At each step, calculate the profit if selling today and
# update the maxProfit if it’s higher than previous.
# This is the most optimal approach for this problem.
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        maxProfit = 0
        buyPrice = math.inf
        for i in range(0, len(prices)):
            buyPrice = min(buyPrice, prices[i])
            maxProfit = max(maxProfit, prices[i] - buyPrice)
        return maxProfit


# -----------------------------------------------
# 🧠 Dynamic Programming Approach
# -----------------------------------------------
# Time Complexity: O(n)
# Space Complexity: O(n)
#
# Description:
# We use a DP array where dp[i] represents the max profit
# up to day i. At each day, we update:
#   - the lowest price seen so far
#   - the max profit by comparing the previous max profit
#     and the profit from selling on day i
# This is slightly less optimal than greedy because of O(n) space.

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        minPrice = prices[0]
        n = len(prices)
        if n == 0:
            return 0
        dp = [0] * n
        for i in range(1, n):
            minPrice = min(minPrice, prices[i])
            dp[i] = max(dp[i - 1], prices[i] - minPrice)
        return dp[-1]