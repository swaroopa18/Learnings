# https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/

# | Version                | Time   | Space  | Notes                                               |
# | ---------------------- | ------ | ------ | --------------------------------------------------- |
# | Backtracking           | O(2^n) | O(n)   | Tries all possibilities; slow                       |
# | Backtracking + Memo    | O(n·2) | O(n·2) | Top-down DP with cache                              |
# | Tabulation             | O(n·2) | O(n·2) | Bottom-up DP                                        |
# | Space-Optimized DP     | O(n)   | O(1)   | Most efficient DP version                           |
# | Manual Greedy Tracking | O(n)   | O(1)   | Manually detects trend breaks                       |
# | Simplest Greedy (Best) | O(n)   | O(1)   | Add all uphills; optimal for unlimited transactions |

from typing import List

# ---------------------------------------------------
# 🔁 Backtracking (No memoization)
# ---------------------------------------------------
# Time Complexity: O(2^n)
# Space Complexity: O(n) recursion stack
#
# Try every possible decision at each day:
# - Buy or Skip (if allowed to buy)
# - Sell or Skip (if holding stock)
# Exponential because it branches at every index.

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        def backtrack(idx, buy):
            if idx == len(prices):
                return 0  # No more days to process

            if buy:
                # Choose to buy today or skip
                profit = max(
                    -prices[idx] + backtrack(idx + 1, 0),  # Buy
                    backtrack(idx + 1, 1)                  # Skip
                )
            else:
                # Choose to sell today or skip
                profit = max(
                    prices[idx] + backtrack(idx + 1, 1),   # Sell
                    backtrack(idx + 1, 0)                  # Skip
                )
            return profit

        return backtrack(0, 1)  # Start on day 0, with buying allowed


# ---------------------------------------------------
# 🧠 Backtracking + Memoization (Top-down DP)
# ---------------------------------------------------
# Time Complexity: O(n * 2)
# Space Complexity: O(n * 2) for DP + O(n) for recursion stack
#
# Avoids recomputing states using memoization.
# dp[idx][buy] stores the max profit from index `idx` with a buy/sell option.

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        def backtrack(idx, buy, n, dp):
            if idx == n:
                return 0
            if dp[idx][buy] != -1:
                return dp[idx][buy]

            if buy:
                profit = max(
                    -prices[idx] + backtrack(idx + 1, 0, n, dp),  # Buy
                    backtrack(idx + 1, 1, n, dp)                  # Skip
                )
            else:
                profit = max(
                    prices[idx] + backtrack(idx + 1, 1, n, dp),   # Sell
                    backtrack(idx + 1, 0, n, dp)                  # Skip
                )

            dp[idx][buy] = profit
            return profit

        n = len(prices)
        dp = [[-1 for _ in range(2)] for _ in range(n)]  # Initialize memo table
        return backtrack(0, 1, n, dp)


# ---------------------------------------------------
# ⬇️ Tabulation (Bottom-up DP)
# ---------------------------------------------------
# Time Complexity: O(n * 2)
# Space Complexity: O(n * 2)
#
# Iterative version of memoized recursion.
# dp[i][buy] holds max profit from day i with state 'buy' (1 = can buy, 0 = must sell).

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        n = len(prices)
        dp = [[0 for _ in range(2)] for _ in range(n + 1)]

        for ind in range(n - 1, -1, -1):
            for buy in range(2):
                if buy:
                    dp[ind][buy] = max(
                        -prices[ind] + dp[ind + 1][0],  # Buy
                        dp[ind + 1][1]                  # Skip
                    )
                else:
                    dp[ind][buy] = max(
                        prices[ind] + dp[ind + 1][1],   # Sell
                        dp[ind + 1][0]                  # Skip
                    )

        return dp[0][1]  # Max profit starting from day 0, allowed to buy


# ---------------------------------------------------
# 🔁 Space-Optimized Tabulation
# ---------------------------------------------------
# Time Complexity: O(n)
# Space Complexity: O(1)
#
# Since we only use values from day i+1, we don’t need the full DP table.
# We just keep track of 'ahead' and 'current' states for buy and not-buy.

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        n = len(prices)
        aheadNotBuy = aheadBuy = 0  # These represent dp[i+1][0] and dp[i+1][1]

        for ind in range(n - 1, -1, -1):
            curNotBuy = max(prices[ind] + aheadBuy, aheadNotBuy)  # Sell or skip
            curBuy = max(-prices[ind] + aheadNotBuy, aheadBuy)    # Buy or skip

            aheadBuy = curBuy
            aheadNotBuy = curNotBuy

        return aheadBuy


# ---------------------------------------------------
# 🔄 Greedy with manual tracking of profit segments
# ---------------------------------------------------
# Time Complexity: O(n)
# Space Complexity: O(1)
#
# Tracks when a new upward trend begins. If profit drops or flattens,
# it realizes the previous gain and resets the buy price.

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        maxProfit = 0
        newMaxProfit = 0
        buyPrice = prices[0]

        for price in prices[1:]:
            buyPrice = min(buyPrice, price)
            profit = price - buyPrice

            if profit > newMaxProfit:
                newMaxProfit = profit  # Keep riding upward trend
            else:
                maxProfit += newMaxProfit  # Take profit and reset
                buyPrice = price
                newMaxProfit = 0

        return maxProfit + newMaxProfit  # Add any remaining profit


# ---------------------------------------------------
# ✅ Simplest Greedy Approach (Optimal)
# ---------------------------------------------------
# Time Complexity: O(n)
# Space Complexity: O(1)
#
# The best strategy when unlimited transactions are allowed:
# - Buy on any day you see a price increase tomorrow.
# - Sum up all such positive differences.

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        maxProfit = 0
        for i in range(1, len(prices)):
            if prices[i] > prices[i - 1]:
                maxProfit += prices[i] - prices[i - 1]  # Take the gain
        return maxProfit
