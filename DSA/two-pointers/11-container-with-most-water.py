#https://leetcode.com/problems/container-with-most-water/description/
import math
from typing import List

# Brute force
# TC: O(n^2)
# SC: O(1)
class Solution:
    def maxArea(self, height: List[int]) -> int:
        maxarea = -math.inf
        for i in range(0, len(height)):
            for j in range(i+1, len(height)):
                area = (j-i) * min(height[j], height[i])
                maxarea = max(maxarea, area)
        return maxarea
        
#------------------------------------------------------------------------------------------------------
    
# Two pointer
# TC: O(n)
# SC: O(1)    
class Solution:
    def maxArea(self, height: List[int]) -> int:
        maxarea = -math.inf
        l, r = 0, len(height) - 1
        while l < r:
            area = (r - l) * min(height[r], height[l])
            maxarea = max(maxarea, area)
            if height[r] < height[l]:
                r -= 1
            else:
                l += 1
        return maxarea
    
 #------------------------------------------------------------------------------------------------------
        
# Two pointer with Early Skipping of Duplicate Heights
# TC: O(n)
# SC: O(1)    
class Solution:
    def maxArea(self, height: List[int]) -> int:
        maxarea = -math.inf
        l, r = 0, len(height) - 1
        while l < r:
            width = r - l
            l_height = height[l]
            r_height = height[r]
            maxarea = max(maxarea, width * min(l_height, r_height))

            if l_height < r_height:
                while l < r and height[l] <= l_height:
                    l += 1
            else:
                while l < r and height[r] <= r_height:
                    r -= 1
        return maxarea

