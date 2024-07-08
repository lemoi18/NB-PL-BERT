from singleton_decorator import singleton
import re
from Digit import Digit
from Cardinal import Cardinal

@singleton
class Decimal:
    """
    Handles the conversion of decimal numbers to their textual representation in Norwegian.
    """
    def __init__(self):
        super().__init__()
        # Regex to detect input of the sort "x.y" or "x,y"
        self.decimal_regex = re.compile(r"(-?\d*)[.,](\d+)(.*)")
        self.number_regex = re.compile(r"(-?\d+)(.*)")
        self.filter_regex = re.compile(r"[,.]")
        self.cardinal = Cardinal()
        self.digit = Digit()
        self.suffixes = ["tusen", "million", "milliard", "billion", "billiard", "trillion"]
        self.suffix_regex = re.compile(f" *({'|'.join(self.suffixes)})")
        self.e_suffix_regex = re.compile(r" *E(-?\d+)")
    
    def convert(self, token: str) -> str:
        # 1 Filter out commas and dots
        token = self.filter_regex.sub(".", token)
        
        # Variable to store values from the input string
        number = ""
        decimal = ""
        
        # 2 Check for the form x.y or x,y
        match = self.decimal_regex.match(token)
        if match:
            # Get the values before and after the separator
            number = match.group(1)
            decimal = match.group(2)
            token = match.group(3)
        else:
            match = self.number_regex.match(token)
            if match:
                # 3 Get the number, and update the token to the remainder
                number = match.group(1)
                token = match.group(2)
        
        # 4 Match suffix, e.g., billion
        match = self.suffix_regex.match(token)
        suffix = ""
        if match:
            suffix = match.group(1)
        else:
            # 5 Otherwise, try to match xEy
            match = self.e_suffix_regex.match(token)
            if match:
                suffix = f"ganger ti til {self.cardinal.convert(match.group(1))}"
        
        # Make list for output
        result_list = []
        if len(decimal) > 0:
            result_list.append("komma")
            # Handle two-digit and single-digit decimals
            if len(decimal) == 2:
                result_list.append(self.cardinal.convert(decimal))
            else:
                for digit in decimal:
                    result_list.append(self.digit.convert(digit))
        
        # 9 If there is a number (there doesn't have to be), then add it in front
        if number:
            result_list.insert(0, self.cardinal.convert(number))
        
        # 10 Add the suffix if applicable
        if suffix:
            result_list.append(suffix)
        
        # 11 Join the result list to form the final output string
        result = " ".join(result_list)
        
        return result
