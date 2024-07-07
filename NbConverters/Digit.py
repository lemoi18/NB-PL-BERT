from singleton_decorator import singleton
import re

@singleton
class Digit:
    """
    Steps:
    - 1 Filter out anything that isn't a digit
    - 2 Check for special case
    - 3 Convert each digit to text
    - 4 Space out the text

    Special Cases:
    007 -> null null syv
    while 003 -> null null tre
    """
    def __init__(self):
        super().__init__()
        # Regex used to filter out non digits
        self.filter_regex = re.compile("[^0-9]")
        # Translation dict to convert digits to text
        self.trans_dict = {
            "0": "null",
            "1": "en",
            "2": "to",
            "3": "tre",
            "4": "fire",
            "5": "fem",
            "6": "seks",
            "7": "syv",
            "8": "åtte",
            "9": "ni"
        }

    def convert(self, token: str) -> str:
        # 1 Filter out anything that isn't a digit
        token = self.filter_regex.sub("", token)
        # 2 Check for special case
        if token == "007":
            return "null null syv"
        # 3 & 4 Convert each digit to text and space out the text
        token = " ".join([self.trans_dict[c] for c in token])
        return token
