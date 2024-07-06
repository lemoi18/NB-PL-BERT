import singleton
from singleton_decorator import singleton
import re

@singleton
class Address:
    """
    Steps:
    - 1 Replace all "-" and "/" with " "
    - 2 Remove all dots
    - 3 Remove trailing spaces
    - 4 Split by spaces
    - 5 Convert each word to number if possible
    - 6 Join the words with a space

    Edge cases:
    """
    def __init__(self):
        super().__init__()
        # Regex to replace "-" and "/"
        self.replace_regex = re.compile(r"[-/]")
        # Regex to remove dots
        self.filter_regex = re.compile(r"[.]")
        # Regex to match digits
        self.digit_regex = re.compile(r"^\d+$")
    
    def convert(self, token: str) -> str:
        # 1 Replace all "-" and "/" with " "
        token = self.replace_regex.sub(" ", token)
        # 2 Remove all dots
        token = self.filter_regex.sub("", token)
        # 3 Remove trailing spaces
        token = token.strip()
        # 4 Split by spaces
        words = token.split()
        # 5 Convert each word to number if possible
        words = [self.convert_word(word) for word in words]
        # 6 Join the words with a space
        return " ".join(words)

    def convert_word(self, word: str) -> str:
        if self.digit_regex.match(word):
            return " ".join([self.digit_to_text(digit) for digit in word])
        return word

    def digit_to_text(self, digit: str) -> str:
        return {
            "0": "null",
            "1": "en",
            "2": "to",
            "3": "tre",
            "4": "fire",
            "5": "fem",
            "6": "seks",
            "7": "sju",
            "8": "åtte",
            "9": "ni"
        }[digit]
