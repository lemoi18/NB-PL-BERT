from singleton_decorator import singleton
import re

@singleton
class Cardinal:
    """
    Steps
    - 1 Remove dots
    - 2 Check whether we are dealing with a Roman Numeral
    - 3 If we are, convert the largest found roman numeral to an integer, and then a string representing that integer
    - 4 If we are, check whether we should include the "'s" suffix (see special cases)
    - 5 Filter out any non digit characters, except "-"
    - 6 Check whether we should use the "minus" prefix
    - 7 Remove all remaining "-" characters
    - 8 If "0", add "null" to the output list
    - 9 If not "0", split string into chunks of max size 3, such that the smallest chunk includes the left most characters
    -   10 Split up each chunk into `hundred` and `rest`
    -   11 Add "x hundred" if `hundred` > 0
    -   12 Add the textual value representing `rest`
    -   13 Add the suffix for the chunk, eg million, milliard, etc.
    -   14 Add the output for the chunk to the total output
    - 15 Reduce the total output list into one string
    - 16 Add pre- and/or suffixes

    Special Cases:
    II -> to
    -2 -> minus to
    I. -> en
    IV's -> fire's

    Notes:
    - There are no "og"s, nor any dashes in the results, eg no "tjue-en" or "hundre og en"
    """
    def __init__(self):
        super().__init__()
        # Regex to remove non digits (spaces, commas etc.), but keep "-"
        self.filter_regex = re.compile("[^0-9\-]")
        # Regex to remove non digits (spaces, commas, "-", etc.)
        self.filter_strict_regex = re.compile("[^0-9]")
        # Regex out dots
        self.dot_filter_regex = re.compile("[.]")

        # List of suffixes
        self.scale_suffixes = [
            "tusen", 
            "million", 
            "milliard", 
            "billion", 
            "billiard", 
            "trillion"
        ]

        # Translation dict for small numbers
        self.small_trans_dict = {
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

        # Translation dict for multiples of tens
        self.tens_trans_dict = {
            "1": "ti",
            "2": "tjue",
            "3": "tretti",
            "4": "førti",
            "5": "femti",
            "6": "seksti",
            "7": "sytti",
            "8": "åtti",
            "9": "nitti"
        }

        # Translation dict for special cases
        self.special_trans_dict = {
            11: "elleve",
            12: "tolv",
            13: "tretten",
            14: "fjorten",
            15: "femten",
            16: "seksten",
            17: "sytten",
            18: "atten",
            19: "nitten"
        }

    def _give_chunk(self, num_str: str, size:int = 3) -> str:
        # While string not empty
        while num_str:
            # yield `size` last elements
            yield num_str[-size:]
            # Shrink num_str
            num_str = num_str[:-size]

    def convert(self, token: str) -> str:
        # 1 Remove Dots
        token = self.dot_filter_regex.sub("", token)

        # 5 Filter out non digits (but keep "-")
        token = self.filter_regex.sub("", token)

        # 6 Prefix for final result. 
        prefix = ""
        while len(token) > 0 and token[0] == "-":
            token = token[1:]
            prefix = "minus" if prefix == "" else ""

        # 7 Now remove all '-' that may exist somewhere not at the start of a number
        token = self.filter_strict_regex.sub("", token)

        # List to store separate words representing the number
        text_list = []

        # 8 The character 0 should only be "null" if there is nothing to the left of it. Otherwise we ignore it.
        if token == len(token) * "0":
            text_list.append("null")
        else:
            # 9 Split up number into chunks
            for depth, chunk in enumerate(self._give_chunk(token)):
                chunk_text_list = []
                # 10 Split up chunk into two sections
                hundred, rest = chunk[-3:-2], chunk[-2:]
                
                # 11 Get "x hundred" prefix
                if len(hundred) != 0 and int(hundred) != 0:
                    chunk_text_list.append(self.small_trans_dict[hundred])
                    chunk_text_list.append("hundre")
                
                # 12 Get text form of `rest`
                if int(rest) in self.special_trans_dict:
                    chunk_text_list.append(self.special_trans_dict[int(rest)])
                else:
                    if len(rest) == 2 and rest[-2] != "0":
                        chunk_text_list.append(self.tens_trans_dict[rest[-2]])
                    if rest[-1] != "0":
                        chunk_text_list.append(self.small_trans_dict[rest[-1]])
                
                # 13 Add suffix based on depth. Eg million, milliard.
                if depth > 0 and len(chunk_text_list) > 0:
                    try:
                        chunk_text_list.append(self.scale_suffixes[depth-1])
                    except IndexError:
                        pass
                
                # 14 Put the text from this chunk at the start of the text_list
                text_list = chunk_text_list + text_list
        
        # 15 Join the list elements with spaces
        token = " ".join(text_list)

        # 16 Apply prefix, if applicable
        if prefix:
            token = f"{prefix} {token}"

        return token
