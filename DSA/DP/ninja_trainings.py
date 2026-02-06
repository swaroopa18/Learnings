# https://www.naukri.com/code360/problems/ninja%E2%80%99s-training_3621003?leftPanelTabValue=PROBLEM

"""
PROBLEM: Ninja's Training
- Ninja trains for n days
- Each day has 3 activities with different points
- Can't do the same activity on consecutive days
- Maximize total points

Example:
Day 0: [10, 40, 70]
Day 1: [20, 50, 80]
Day 2: [30, 60, 90]

If we pick activity 2 on day 0 (70 points), we can only pick activity 0 or 1 on day 1
"""

from typing import List

# ============================================================================
# APPROACH 1: RECURSION (Your Original - Exponential Time)
# ============================================================================
# Time: O(3^n) - For each day we try 2-3 choices, leading to exponential calls
# Space: O(n) - Recursion stack depth
# This will TLE for large inputs

def ninjaTraining_recursive(n: int, points: List[List[int]]) -> int:
    def fun(day, last):
        # Base case: reached the last day
        if day == n - 1:
            maxi = 0
            # Pick the best activity that's not the same as last
            for i in range(3):
                if i != last:
                    maxi = max(maxi, points[n - 1][i])
            return maxi

        # Try all activities except the one we did yesterday
        maxi = 0
        for i in range(3):
            if i != last:
                # Points today + best we can get from tomorrow onwards
                curr = points[day][i] + fun(day + 1, i)
                maxi = max(maxi, curr)
        return maxi

    # Start from day 0, with 'last=3' meaning no activity done yet
    return fun(0, 3)


# ============================================================================
# APPROACH 2: MEMOIZATION (Top-Down DP)
# ============================================================================
# Time: O(n * 4 * 3) = O(n) - We have n days × 4 possible last values × 3 choices
# Space: O(n * 4) - DP table + recursion stack
# WHY IT WORKS: Same subproblems are computed multiple times in recursion
# We cache results for (day, last_activity) states

def ninjaTraining_memo(n: int, points: List[List[int]]) -> int:
    # dp[day][last] = max points from 'day' onwards when 'last' activity was done
    dp = [[-1] * 4 for _ in range(n)]
    
    def solve(day, last):
        # Base case
        if day == n - 1:
            maxi = 0
            for i in range(3):
                if i != last:
                    maxi = max(maxi, points[day][i])
            return maxi
        
        # Check if already computed
        if dp[day][last] != -1:
            return dp[day][last]
        
        # Try all valid activities
        maxi = 0
        for i in range(3):
            if i != last:
                curr = points[day][i] + solve(day + 1, i)
                maxi = max(maxi, curr)
        
        dp[day][last] = maxi
        return maxi
    
    return solve(0, 3)  # Start with no previous activity (3 means none)


# ============================================================================
# APPROACH 3: TABULATION (Bottom-Up DP) - RECOMMENDED ✓
# ============================================================================
# Time: O(n * 4 * 3) = O(n)
# Space: O(n * 4) - Can be optimized to O(1)
# WHY THIS IS BEST: Iterative, easier to understand, no recursion overhead

def ninjaTraining_tabulation(n: int, points: List[List[int]]) -> int:
    # dp[i][j] = max points from day i to n-1, when activity j was done on day i-1
    # j = 0,1,2 (activities), j = 3 (no previous activity)
    dp = [[0] * 4 for _ in range(n)]
    
    # Base case: Day 0
    # If no previous activity (3), we can choose any of the 3 activities
    dp[0][0] = points[0][0]  # If we choose activity 0 on day 0
    dp[0][1] = points[0][1]  # If we choose activity 1 on day 0
    dp[0][2] = points[0][2]  # If we choose activity 2 on day 0
    dp[0][3] = max(points[0][0], points[0][1], points[0][2])  # Best on day 0
    
    # Fill the table from day 1 to n-1
    for day in range(1, n):
        for last in range(4):
            dp[day][last] = 0
            # Try all activities except 'last'
            for activity in range(3):
                if activity != last:
                    # Current activity points + best from previous day when 'activity' was done
                    curr_points = points[day][activity] + dp[day - 1][activity]
                    dp[day][last] = max(dp[day][last], curr_points)
    
    # Answer: max points on last day with no constraint (last=3)
    return dp[n - 1][3]


# ============================================================================
# APPROACH 4: SPACE OPTIMIZED (Bottom-Up DP) - MOST OPTIMAL ✓✓
# ============================================================================
# Time: O(n)
# Space: O(1) - Only need previous day's data
# WHY: We only need the previous row to compute current row

def ninjaTraining(n: int, points: List[List[int]]) -> int:
    # prev[j] = max points when activity j was done on previous day
    prev = [0] * 4
    
    # Base case: Day 0
    prev[0] = points[0][0]
    prev[1] = points[0][1]
    prev[2] = points[0][2]
    prev[3] = max(points[0][0], points[0][1], points[0][2])
    
    # Process each day
    for day in range(1, n):
        curr = [0] * 4
        
        for last in range(4):
            curr[last] = 0
            # Try each activity
            for activity in range(3):
                if activity != last:
                    # Current activity points + best when we did 'activity' yesterday
                    curr[last] = max(curr[last], 
                                   points[day][activity] + prev[activity])
        
        prev = curr  # Move to next day
    
    return prev[3]  # No constraint on last activity


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test case 1
    n1 = 3
    points1 = [[10, 40, 70],
               [20, 50, 80],
               [30, 60, 90]]
    print(f"Test 1: {ninjaTraining(n1, points1)}")  # Expected: 210 (70+50+90)
    
    # Test case 2
    n2 = 2
    points2 = [[10, 50, 1],
               [5, 100, 11]]
    print(f"Test 2: {ninjaTraining(n2, points2)}")  # Expected: 110 (10+100)