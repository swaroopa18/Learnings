# https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/

# PROBLEM SUMMARY:
# - Can make unlimited transactions (buy-sell pairs)
# - Cannot hold multiple stocks (must sell before buying again)
# - Goal: Maximize total profit
# - Key insight: This is simpler than Stock I because no transaction limit

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
# 🔁 APPROACH 1: Backtracking (No memoization)
# ---------------------------------------------------
# TIME COMPLEXITY: O(2^n) - Exponential because we branch at every day
# SPACE COMPLEXITY: O(n) - Recursion stack depth
#
# CONCEPT: Try every possible decision at each day
# - At each day: 2 choices (buy/skip when can buy, sell/skip when holding)
# - Creates decision tree with 2^n leaf nodes
# - Many redundant calculations (same states reached multiple ways)
#
# STATE DEFINITION: (idx, buy) where:
# - idx: current day (0 to n-1)
# - buy: 1 if we can buy, 0 if we're holding stock (must sell first)
#
# WHY max()?: Represents CHOICE - we're not forced to trade
# - Without max(): Would make suboptimal forced trades
# - With max(): Only trade when profitable
class Solution:
    def maxProfitWithBT(self, prices: List[int]) -> int:
        def backtrack(idx, buy):
            # BASE CASE: No more days to process
            if idx == len(prices):
                return 0  # No profit possible

            if buy:  # Currently allowed to buy (not holding stock)
                # CHOICE 1: Buy today (cost -prices[idx], then can only sell)
                # CHOICE 2: Skip today (no cost, still can buy tomorrow)
                profit = max(
                    -prices[idx] + backtrack(idx + 1, 0),  # Buy: pay price, switch to sell mode
                    backtrack(idx + 1, 1)                  # Skip: no change, stay in buy mode
                )
            else:  # Currently holding stock (must sell before buying)
                # CHOICE 1: Sell today (gain +prices[idx], then can buy again)
                # CHOICE 2: Skip today (no gain, keep holding)
                profit = max(
                    prices[idx] + backtrack(idx + 1, 1),   # Sell: gain price, switch to buy mode
                    backtrack(idx + 1, 0)                  # Skip: no change, stay in sell mode
                )
            return profit

        return backtrack(0, 1)  # Start on day 0, with buying allowed

# ---------------------------------------------------
# 🔁 APPROACH 1B: Backtracking with Path Tracking (Debug Version)
# ---------------------------------------------------
# Same as above but tracks decision paths for understanding
# Useful for visualizing how the algorithm explores all possibilities
class Solution:
    def maxProfitWithBT2(self, prices: List[int]) -> int:
        def solve(day, holding, path=[]):
            # BASE CASE: No more days to trade
            if day >= len(prices):
                print(f"Path: {path}, Final profit: 0")
                return 0
    
            print(f"Day {day}, Price: {prices[day]}, Holding: {holding}")
    
            # OPTION 1: Do nothing today (always available)
            do_nothing = solve(day + 1, holding, path + [f"Day {day}: Do nothing"])
    
            if holding:
                # OPTION 2: Sell today (we have stock to sell)
                sell_profit = prices[day] + solve(day + 1, False, path + [f"Day {day}: Sell at {prices[day]}"])
                print(f"  Sell option: {sell_profit}")
                return max(do_nothing, sell_profit)
            else:
                # OPTION 2: Buy today (we don't have stock)
                buy_profit = -prices[day] + solve(day + 1, True, path + [f"Day {day}: Buy at {prices[day]}"])
                print(f"  Buy option: {buy_profit}")
                return max(do_nothing, buy_profit)
    
        return solve(0, False)


# ---------------------------------------------------
# 🧠 APPROACH 2: Backtracking + Memoization (Top-down DP)
# ---------------------------------------------------
# TIME COMPLEXITY: O(n × 2) = O(n) - Each state computed once
# SPACE COMPLEXITY: O(n × 2) for memo + O(n) for recursion stack
#
# OPTIMIZATION: Avoids recomputing states using memoization
# KEY INSIGHT: There are only 2n unique states: (idx, buy) combinations
# - n possible indices × 2 possible buy values = 2n states
# - Each state is computed exactly once and cached
#
# MEMOIZATION PATTERN:
# - Check if state already computed
# - If yes, return cached result
# - If no, compute and cache before returning
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        def backtrack(idx, buy):
            # BASE CASE: No more days
            if idx == n:
                return 0

            # MEMOIZATION: Check if already computed
            if (idx, buy) in memo:
                return memo[(idx, buy)]

            if buy:  # Can buy today
                profit = max(
                    -prices[idx] + backtrack(idx + 1, 0),  # Buy today
                    backtrack(idx + 1, 1)                  # Skip today
                )
            else:  # Must sell (currently holding)
                profit = max(
                    prices[idx] + backtrack(idx + 1, 1),   # Sell today
                    backtrack(idx + 1, 0)                  # Skip today
                )

            # CACHE the result before returning
            memo[(idx, buy)] = profit
            return profit

        n = len(prices)
        memo = {}  # Cache for (idx, buy) -> max_profit
        return backtrack(0, 1)  # Start: day 0, can buy


# ---------------------------------------------------
# ⬇️ APPROACH 3: Tabulation (Bottom-up DP)
# ---------------------------------------------------
# TIME COMPLEXITY: O(n × 2) = O(n)
# SPACE COMPLEXITY: O(n × 2) = O(n)
#
# CONCEPT: Iterative version of memoized recursion
# - Build solutions from base case upward
# - No recursion stack needed
# - Often clearer logic flow
#
# DP STATE DEFINITION:
# - dp[i][0] = max profit on day i when NOT holding stock
# - dp[i][1] = max profit on day i when HOLDING stock
#
# TRANSITION EQUATIONS:
# - dp[i][0] = max(dp[i-1][0], dp[i-1][1] + prices[i])
#   (either didn't hold yesterday, or sell today)
# - dp[i][1] = max(dp[i-1][1], dp[i-1][0] - prices[i])
#   (either held yesterday, or buy today)
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        n = len(prices)
        if n <= 1:
            return 0
        
        # DP TABLE: dp[i][j] where j=0 means not holding, j=1 means holding
        dp = [[0, 0] for _ in range(n)]
        
        # BASE CASE: Day 0
        dp[0][0] = 0           # Don't buy on day 0: profit = 0
        dp[0][1] = -prices[0]  # Buy on day 0: profit = -prices[0]
        
        # FILL TABLE: Day 1 to n-1
        for i in range(1, n):
            # NOT HOLDING stock on day i
            dp[i][0] = max(
                dp[i-1][0],              # Didn't hold yesterday, don't buy today
                dp[i-1][1] + prices[i]   # Held yesterday, sell today
            )
            
            # HOLDING stock on day i
            dp[i][1] = max(
                dp[i-1][1],              # Already held yesterday, keep holding
                dp[i-1][0] - prices[i]   # Didn't hold yesterday, buy today
            )
        
        # RESULT: End without holding stock (we want to have sold everything)
        return dp[n-1][0]


# ---------------------------------------------------
# 🔁 APPROACH 4: Space-Optimized Tabulation
# ---------------------------------------------------
# TIME COMPLEXITY: O(n)
# SPACE COMPLEXITY: O(1) - Only store previous day's values
#
# OPTIMIZATION: Since we only use values from day i-1, we don't need full DP table
# - Replace 2D array with 4 variables
# - Same logic, but constant space
#
# SPACE REDUCTION TECHNIQUE:
# - Old: dp[i-1][0], dp[i-1][1], dp[i][0], dp[i][1]
# - New: not_hold, hold, new_not_hold, new_hold
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if len(prices) <= 1:
            return 0
        
        # SPACE-OPTIMIZED: Only track previous day's states
        hold = -prices[0]    # Max profit while holding stock (bought on day 0)
        not_hold = 0         # Max profit without holding stock (didn't buy on day 0)
        
        for i in range(1, len(prices)):
            # Calculate new states based on previous day
            new_not_hold = max(not_hold, hold + prices[i])  # Don't hold OR sell today
            new_hold = max(hold, not_hold - prices[i])      # Keep holding OR buy today
            
            # Update for next iteration
            not_hold = new_not_hold
            hold = new_hold
        
        return not_hold  # End without holding stock


# ---------------------------------------------------
# 🔄 APPROACH 5: Greedy with Manual Profit Tracking
# ---------------------------------------------------
# TIME COMPLEXITY: O(n)
# SPACE COMPLEXITY: O(1)
#
# CONCEPT: Manually track upward trends and realize profits when trends break
# - Track current buying price and unrealized profit
# - When profit decreases, realize current profit and reset
# - More complex than simple greedy but shows the trend-following logic
#
# ALGORITHM FLOW:
# 1. Track buyPrice (lowest price seen in current trend)
# 2. Track newMaxProfit (unrealized profit in current trend)
# 3. When trend breaks (profit decreases), realize profit and reset
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        maxProfit = 0        # Total realized profit
        newMaxProfit = 0     # Unrealized profit in current trend
        buyPrice = prices[0] # Current buy price (lowest in trend)

        for price in prices[1:]:
            # Update buy price to lowest seen in current trend
            buyPrice = min(buyPrice, price)
            profit = price - buyPrice  # Unrealized profit if we sell today

            if profit > newMaxProfit:
                # Trend continuing up, update unrealized profit
                newMaxProfit = profit
            else:
                # Trend broken! Realize previous profit and reset
                maxProfit += newMaxProfit  # Add realized profit
                buyPrice = price           # Reset buy price to current price
                newMaxProfit = 0           # Reset unrealized profit

        # Don't forget remaining unrealized profit
        return maxProfit + newMaxProfit


# ---------------------------------------------------
# ✅ APPROACH 6: Simplest Greedy (Peak-Valley) - OPTIMAL
# ---------------------------------------------------
# TIME COMPLEXITY: O(n)
# SPACE COMPLEXITY: O(1)
#
# CORE INSIGHT: With unlimited transactions, optimal strategy is:
# "Capture every upward price movement"
#
# MATHEMATICAL PROOF:
# - Any optimal solution can be decomposed into upward moves
# - Missing any upward move means missing profit
# - Therefore: max profit = sum of all positive differences
#
# VISUALIZATION: [1, 3, 2, 4]
# - Day 1→2: +2 profit (buy at 1, sell at 3)
# - Day 2→3: +0 profit (price drops, don't trade)
# - Day 3→4: +2 profit (buy at 2, sell at 4)
# - Total: 2 + 0 + 2 = 4
#
# GREEDY PROOF: If prices[i] > prices[i-1], we MUST capture this gain
# in any optimal solution (otherwise we're leaving money on the table)
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        maxProfit = 0
        
        # Scan through prices and capture every upward move
        for i in range(1, len(prices)):
            if prices[i] > prices[i - 1]:
                # Capture the gain (equivalent to buy yesterday, sell today)
                maxProfit += prices[i] - prices[i - 1]
                
        return maxProfit

# ---------------------------------------------------
# 🎯 INTERVIEW TIPS AND KEY INSIGHTS
# ---------------------------------------------------

"""
1. PROBLEM RECOGNITION:
   - Stock II is EASIER than Stock I because unlimited transactions
   - No need to track "best buy day" - we can buy/sell optimally at each step

2. APPROACH EVOLUTION:
   - Backtracking: Understand the problem structure
   - Memoization: Recognize overlapping subproblems
   - Tabulation: Convert to iterative DP
   - Space optimization: Reduce space complexity
   - Greedy: Find the mathematical insight

3. WHY GREEDY WORKS:
   - Unlimited transactions mean we can capture every profitable opportunity
   - Any optimal solution includes all upward price movements
   - Missing any upward move = suboptimal

4. COMMON MISTAKES:
   - Forgetting that we can't hold multiple stocks
   - Not understanding why max() is needed (represents choice)
   - Overcomplicating when greedy solution exists

5. INTERVIEW STRATEGY:
   - Start with brute force to show problem understanding
   - Optimize to DP to show algorithmic thinking
   - Discover greedy to show mathematical insight
   - Always explain the "why" behind each optimization

6. FOLLOW-UP QUESTIONS:
   - What if transaction fees exist? (Stock with fees)
   - What if limited to k transactions? (Stock III/IV)
   - What if cooldown period? (Stock with cooldown)
"""