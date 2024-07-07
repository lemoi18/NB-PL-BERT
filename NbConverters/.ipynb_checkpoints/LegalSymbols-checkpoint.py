from singleton_decorator import singleton
import re

@singleton
class LegalSymbols:
    """
    This class handles the conversion of legal symbols and specific terms into their full forms.
    """
    def __init__(self):
        super().__init__()
        self.legal_trans_dict = {
            "§": "paragraf",
            "¶": "avsnitt",
            "•": "punkt",
            "-": "bindestrek"
        }
        
        # Patterns for detecting legal symbols, sections, sub-sections, and list items
        self.section_regex = re.compile(r"§\s*(\d+)")
        self.sub_section_regex = re.compile(r"§\s*(\d+)\s*-\s*(\d+)")
        self.list_regex = re.compile(r"(\d+)\.")
        self.letter_list_regex = re.compile(r"([a-zA-Z])\)")

        # Number to text conversion dictionary for basic numbers
        self.num_dict_list = {
            "1": "første",
            "2": "andre",
            "3": "tredje",
            "4": "fjerde",
            "5": "femte",
            "6": "sjette",
            "7": "sjuende",
            "8": "åttende",
            "9": "niende",
            "10": "tiende",
            "11": "ellevte",
            "12": "tolvte",
            # Add more as needed
        }
        self.num_dict = {
            "1": "en",
            "2": "to",
            "3": "tre",
            "4": "fire",
            "5": "fem",
            "6": "seks",
            "7": "syv",
            "8": "åtte",
            "9": "ni",
            "10": "ti",
            "11": "ellve",
            "12": "tolv",
            # Add more as needed
        }
        # Letter to text conversion dictionary for list items
        self.letter_dict = {
            "a": "a",
            "b": "b",
            "c": "c",
            "d": "d",
            "e": "e",
            "f": "f",
            "g": "g",
            "h": "h",
            "i": "i",
            "j": "j",
            "k": "k",
            "l": "l",
            "m": "m",
            "n": "n",
            "o": "o",
            "p": "p",
            "q": "q",
            "r": "r",
            "s": "s",
            "t": "t",
            "u": "u",
            "v": "v",
            "w": "w",
            "x": "x",
            "y": "y",
            "z": "z",
            # Add uppercase handling if needed
        }

    def convert(self, token: str) -> str:
        # Handle specific legal symbols
        if token in self.legal_trans_dict:
            return self.legal_trans_dict[token]

        # Handle section symbols with numbers
        match = self.section_regex.match(token)
        if match:
            section_number = match.group(1)
            return f"paragraf {self.number_to_text(section_number)}"

        # Handle sub-sections with ranges
        match = self.sub_section_regex.match(token)
        if match:
            start_section, end_section = match.group(1), match.group(2)
            return f"paragraf {self.number_to_text(start_section)} til paragraf {self.number_to_text(end_section)}"

        # Handle list items with numbers
        match = self.list_regex.match(token)
        if match:
            list_number = match.group(1)
            return f"{self.number_to_text_list(list_number)} punkt"

        # Handle list items with letters
        match = self.letter_list_regex.match(token)
        if match:
            list_letter = match.group(1)
            return f"{self.letter_dict[list_letter.lower()]} punkt"

        # If no specific match is found, return the original token
        return token

    def number_to_text(self, number: str) -> str:
        # Convert numbers to their textual representation
        # This function can be extended to handle more complex numbers if needed
        if number in self.num_dict:
            return self.num_dict[number]
        return number
    def number_to_text_list(self, number: str) -> str:
        # Convert numbers to their textual representation
        # This function can be extended to handle more complex numbers if needed
        if number in self.num_dict_list:
            return self.num_dict_list[number]
        return number
