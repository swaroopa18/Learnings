from queue import PriorityQueue
from typing import List
import heapq
from collections import Counter, deque


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        """
        Task Scheduler - Find minimum time to complete all tasks with cooldown
        
        Problem: Given tasks and cooldown period n, find minimum time to complete all tasks
        where same task must wait n intervals before being executed again.
        
        Current Approach: Simulation with Priority Queue
        - Use max heap to always process most frequent task first
        - Use cooldown queue to track when tasks become available again
        - Simulate time step by step
        """
        
        # Count frequency of each task
        task_freq = {}
        for task in tasks:
            task_freq[task] = task_freq.get(task, 0) + 1

        # Max heap using negative values (PriorityQueue is min heap by default)
        pq = PriorityQueue()
        for task, count in task_freq.items():
            pq.put((-count, task))  # Negative for max heap behavior

        # Queue to track tasks in cooldown: (ready_time, -count, task)
        cool_down = PriorityQueue()
        currentTime = 0
        
        # Simulate execution time step by step
        while not pq.empty() or not cool_down.empty():
            # Check if any task is ready from cooldown
            if not cool_down.empty() and cool_down.queue[0][0] <= currentTime:
                ready_time, count, task = cool_down.get()
                pq.put((count, task))  # Put back in main queue
            
            # Execute highest priority task if available
            if not pq.empty():
                count, task = pq.get()
                # If task has remaining executions, put in cooldown
                if count + 1 != 0:  # count is negative, so +1 moves toward 0
                    cool_down.put((currentTime + n + 1, count + 1, task))
            
            currentTime += 1
        
        return currentTime


class SolutionOptimized:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        """
        Optimized Approach 1: Heap + List simulation
        
        Better than PriorityQueue approach:
        - Uses heapq (more efficient than PriorityQueue)
        - Uses list instead of queue for cooldown tracking
        - Cleaner implementation
        
        Time: O(time * log(unique_tasks)) where time is the result
        Space: O(unique_tasks)
        """
        if n == 0:
            return len(tasks)
        
        # Count task frequencies
        task_count = Counter(tasks)
        
        # Max heap (use negative values)
        heap = [-count for count in task_count.values()]
        heapq.heapify(heap)
        
        time = 0
        
        while heap:
            # Try to execute tasks in current cycle
            cycle = []
            
            # Execute up to n+1 tasks (to fill one complete cycle)
            for _ in range(n + 1):
                if heap:
                    cycle.append(-heapq.heappop(heap))
                
            # Put back tasks that still have remaining executions
            for count in cycle:
                if count > 1:
                    heapq.heappush(heap, -(count - 1))
            
            # Add time for this cycle
            # If heap is empty, we only need time for executed tasks
            # If heap has tasks, we need full cycle time (n+1)
            time += len(cycle) if not heap else n + 1
        
        return time


class SolutionMath:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        """
        Mathematical Approach - Most Efficient
        
        Key insight: The minimum time is determined by either:
        1. The most frequent task's pattern: (max_freq - 1) * (n + 1) + tasks_with_max_freq
        2. Total number of tasks (when cooldown doesn't matter)
        
        Time: O(m) where m is number of tasks
        Space: O(1) - only storing counts
        """
        if n == 0:
            return len(tasks)
        
        # Count frequencies
        task_count = Counter(tasks)
        max_freq = max(task_count.values())
        
        # Count how many tasks have the maximum frequency
        max_freq_tasks = sum(1 for count in task_count.values() if count == max_freq)
        
        # Formula approach:
        # - Most frequent task creates (max_freq - 1) complete cycles
        # - Each cycle needs (n + 1) time slots
        # - Last execution of max frequency tasks
        min_time = (max_freq - 1) * (n + 1) + max_freq_tasks
        
        # The answer is max of calculated time and total tasks
        # (in case we have enough variety that cooldown doesn't matter)
        return max(min_time, len(tasks))


"""
COMPLEXITY ANALYSIS:

1. Original Approach (PriorityQueue simulation):
   Time: O(time * log(unique_tasks)) where time is the final result
   Space: O(unique_tasks)
   - Each time step: O(log(unique_tasks)) for heap operations
   - Total time steps: can be up to (max_freq - 1) * (n + 1) + max_freq_tasks
   
2. Optimized Approach (Heap + cycle processing):
   Time: O(unique_tasks * log(unique_tasks))
   Space: O(unique_tasks)
   - Better constant factors, processes in cycles instead of single time steps
   
3. Mathematical Approach:
   Time: O(m) where m is total number of tasks
   Space: O(1) if using array for counting, O(unique_tasks) if using Counter
   - Most efficient, direct formula calculation

RECOMMENDED APPROACH:
Use Mathematical approach for interviews - it's most efficient and shows deep understanding.
Use Optimized approach if you need to show the simulation logic clearly.

KEY INSIGHTS:
- The bottleneck is always the most frequent task
- If cooldown is 0, answer is just total tasks
- If we have enough task variety, cooldown becomes irrelevant
- The mathematical formula captures both constraints elegantly
"""