from typing import List
import heapq

class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        """
        Find the k closest points to the origin (0, 0) using Euclidean distance.
        
        Args:
            points: List of [x, y] coordinates
            k: Number of closest points to return
            
        Returns:
            List of k closest points to origin
            
        Time Complexity: O(n log k) where n is number of points
        Space Complexity: O(k) for the heap
        
        Algorithm:
        - Use a max heap to maintain k closest points
        - For each point, calculate squared distance (no need for sqrt since we only compare)
        - Keep heap size at most k by removing farthest point when needed
        - Use negative distances to simulate max heap with Python's min heap
        """
        max_heap = []
        
        for point in points:
            dist_squared = point[0] * point[0] + point[1] * point[1]
            
            if len(max_heap) < k:
                heapq.heappush(max_heap, (-dist_squared, point))
            else:
                if max_heap[0][0] < -dist_squared:
                    heapq.heappop(max_heap)
                    heapq.heappush(max_heap, (-dist_squared, point))
        
        return [point for _, point in max_heap]

# Alternative O(n log n) solution using sorting
class SolutionAlternative:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        """
        Alternative approach using sorting.
        
        Time Complexity: O(n log n)
        Space Complexity: O(n) for sorting
        
        Simpler but less efficient for large n and small k.
        """
        points.sort(key=lambda p: p[0] * p[0] + p[1] * p[1])
        return points[:k]
