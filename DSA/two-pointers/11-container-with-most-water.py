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
        n = len(height)
        l, r = 0, n - 1

        max_area = 0

        # We need at least two different boundaries
        # to form a container.
        while l < r:

            # Store the current heights because we may move
            # the pointers in the while loops below.
            l_height = height[l]
            r_height = height[r]

            # Calculate the area formed by the current
            # left and right boundaries.
            #
            # The shorter boundary determines the amount
            # of water that can be contained.
            current_area = (r - l) * min(l_height, r_height)

            # Keep the maximum area seen so far.
            max_area = max(current_area, max_area)

            # ------------------------------------------------
            # If left boundary is shorter or equal
            # ------------------------------------------------
            if height[l] <= height[r]:

                # The current container is limited by l_height.
                #
                # We are going to move l to the right, which
                # decreases the width.
                #
                # Therefore, the only way to possibly get a
                # larger area is to find a height GREATER than
                # the current l_height.
                #
                # Any height <= l_height cannot help:
                #
                #     width decreases
                #     height remains the same or decreases
                #
                # So we skip all such heights.
                while l < r and height[l] <= l_height:
                    l += 1

            # ------------------------------------------------
            # If right boundary is shorter
            # ------------------------------------------------
            else:

                # The current container is limited by r_height.
                #
                # We are going to move r to the left, which
                # decreases the width.
                #
                # Therefore, the only way to possibly get a
                # larger area is to find a height GREATER than
                # the current r_height.
                #
                # Any height <= r_height cannot help because
                # the width becomes smaller and the limiting
                # height does not increase.
                while l < r and height[r] <= r_height:
                    r -= 1

        return max_area
