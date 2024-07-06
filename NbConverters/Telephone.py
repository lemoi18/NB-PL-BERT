from singleton_decorator import singleton
import re

@singleton
class Telephone:
    """
    Converts telephone numbers to their full Norwegian text representation.
    """
    def __init__(self):
        super().__init__()
        self.phone_regex = re.compile(r"(\+?\d{1,3})?[-.\s]?(\d{1,4})[-.\s]?(\d{1,4})[-.\s]?(\d{1,4})[-.\s]?(\d{1,4})")

    def convert(self, token: str) -> str:
        match = self.phone_regex.match(token)
        if match:
            parts = [part for part in match.groups() if part]
            return " ".join(self.convert_part(part) for part in parts)
        return token

    def convert_part(self, part: str) -> str:
        if part.startswith("+"):
            return f"pluss {self.convert_digits(part[1:])}"
        return self.convert_digits(part)

    def convert_digits(self, digits: str) -> str:
        digit_map = {
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
        }
        return " ".join(digit_map[digit] for digit in digits)