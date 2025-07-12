from typing import List

class Solution:
    """
    Gas Station Problem: Find starting gas station index to complete circular route
    
    Problem: Given gas[] and cost[] arrays, find starting station index where we can
    complete a circular trip visiting all stations exactly once.
    """
    
    # APPROACH 1: BRUTE FORCE
    # Time: O(n²), Space: O(1)
    def canCompleteCircuit_bruteforce(self, gas: List[int], cost: List[int]) -> int:
        """
        Try every possible starting station and simulate the journey.
        For each start position, check if we can complete the full circle.
        """
        n = len(gas)
        for start in range(n):
            tank = 0
            for i in range(n):
                station = (i + start) % n
                tank += gas[station] - cost[station]
                if tank < 0:
                    break
            if tank >= 0:
                return start
        return -1
    
    # APPROACH 2: GREEDY SINGLE PASS (OPTIMAL)
    # Time: O(n), Space: O(1)
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        """
        KEY INSIGHTS:
        1. If total_gas < total_cost, impossible to complete circuit
        2. If total_gas >= total_cost, there exists exactly one solution
        3. If we can't reach station j from station i, then we can't reach j 
           from any station between i and j-1
        4. The optimal starting point is right after the "worst" deficit point
        
        Algorithm:
        - Track total surplus/deficit (total_tank)
        - Track current journey surplus/deficit (current_tank)
        - When current_tank goes negative, reset start to next station
        """
        total_tank = 0      # Total gas surplus/deficit for entire circuit
        current_tank = 0    # Current journey surplus/deficit
        start = 0          # Candidate starting station
        
        for i in range(len(gas)):
            total_tank += gas[i] - cost[i]
            current_tank += gas[i] - cost[i]
            
            # If current journey fails, start fresh from next station
            if current_tank < 0:
                start = i + 1
                current_tank = 0
        
        return start if total_tank >= 0 else -1
    
    # APPROACH 3: TWO PASS WITH DEFICIT TRACKING
    # Time: O(n), Space: O(1)
    def canCompleteCircuit_two_pass(self, gas: List[int], cost: List[int]) -> int:
        """
        First pass: Check if solution exists (total_gas >= total_cost)
        Second pass: Find the starting point by tracking maximum deficit
        """
        n = len(gas)
        total_surplus = sum(gas[i] - cost[i] for i in range(n))
        
        if total_surplus < 0:
            return -1
        
        # Find starting point: station after maximum deficit point
        min_surplus = float('inf')
        min_index = 0
        current_surplus = 0
        
        for i in range(n):
            current_surplus += gas[i] - cost[i]
            if current_surplus < min_surplus:
                min_surplus = current_surplus
                min_index = i
        
        return (min_index + 1) % n
    
    # APPROACH 4: PREFIX SUM APPROACH
    # Time: O(n), Space: O(n)
    def canCompleteCircuit_prefix_sum(self, gas: List[int], cost: List[int]) -> int:
        """
        Build prefix sum array to find minimum prefix sum position.
        The starting point is right after the minimum prefix sum position.
        
        KEY INSIGHT: 
        - If we start right after the most negative cumulative sum point,
          we ensure we never run out of gas during the journey.
        """
        n = len(gas)
        diff = [gas[i] - cost[i] for i in range(n)]
        
        # Check if solution exists
        if sum(diff) < 0:
            return -1
        
        # Build prefix sum array
        prefix_sum = [0] * n
        prefix_sum[0] = diff[0]
        for i in range(1, n):
            prefix_sum[i] = prefix_sum[i-1] + diff[i]
        
        # Find index of minimum prefix sum
        min_sum = min(prefix_sum)
        min_index = prefix_sum.index(min_sum)
        
        # Starting point is right after minimum prefix sum position
        return (min_index + 1) % n
    
    # APPROACH 5: SPACE-OPTIMIZED PREFIX SUM
    # Time: O(n), Space: O(1)
    def canCompleteCircuit_prefix_sum_optimized(self, gas: List[int], cost: List[int]) -> int:
        """
        Same logic as prefix sum but without storing the entire array.
        Track minimum sum and its position while calculating prefix sum.
        """
        total_sum = 0
        min_sum = float('inf')
        min_index = 0
        current_sum = 0
        
        for i in range(len(gas)):
            diff = gas[i] - cost[i]
            total_sum += diff
            current_sum += diff
            
            if current_sum < min_sum:
                min_sum = current_sum
                min_index = i
        
        return (min_index + 1) % len(gas) if total_sum >= 0 else -1