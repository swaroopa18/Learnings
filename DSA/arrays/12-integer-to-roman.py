# https://leetcode.com/problems/integer-to-roman/description/


# Time complexity: O(1)
# Space complexity: O(1)
class Solution:
    def intToRoman(self, num: int) -> str:
        val_to_symbol = [
            (1000, "M"),
            (900, "CM"),
            (500, "D"),
            (400, "CD"),
            (100, "C"),
            (90, "XC"),
            (50, "L"),
            (40, "XL"),
            (10, "X"),
            (9, "IX"),
            (5, "V"),
            (4, "IV"),
            (1, "I"),
        ]

        roman = ""
        for val, symbol in val_to_symbol:
            while num >= val:
                roman += symbol
                num -= val
        return roman



# Time complexity: O(n)
# Space complexity: O(n)
class Solution:
    def intToRoman(self, num: int) -> str:
        if num == 0:
            return ""
        if num >= 1000:
            return "M" + self.intToRoman(num - 1000)
        if num >= 900:
            return "CM" + self.intToRoman(num - 900)
        if num >= 500:
            return "D" + self.intToRoman(num - 500)
        if num >= 400:
            return "CD" + self.intToRoman(num - 400)
        if num >= 100:
            return "C" + self.intToRoman(num - 100)
        if num >= 90:
            return "XC" + self.intToRoman(num - 90)
        if num >= 50:
            return "L" + self.intToRoman(num - 50)
        if num >= 40:
            return "XL" + self.intToRoman(num - 40)
        if num >= 10:
            return "X" + self.intToRoman(num - 10)
        if num >= 9:
            return "IX" + self.intToRoman(num - 9)
        if num >= 5:
            return "V" + self.intToRoman(num - 5)
        if num >= 4:
            return "IV" + self.intToRoman(num - 4)
        if num >= 1:
            return "I" + self.intToRoman(num - 1)