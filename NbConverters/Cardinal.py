from singleton_decorator import singleton
import re

@singleton
class Cardinal:
    """
    Handles the conversion of cardinal numbers to their textual representation in Norwegian.
    """
    def __init__(self):
        super().__init__()
        self.filter_regex = re.compile("[^0-9\-]")
        self.dot_filter_regex = re.compile("[.]")

        # List of suffixes for scales
        self.scale_suffixes = [
            ("tusen", "tusen"),        # singular and plural are the same
            ("million", "millioner"),
            ("milliard", "milliarder"),
            ("billion", "billioner"),
            ("billiard", "billiarder"),
            ("trillion", "trillioner")
        ]

        # Translation dict for small numbers
        self.small_trans_dict = {
            "1": ["en", "ett"],
            "2": "to",
            "3": "tre",
            "4": "fire",
            "5": "fem",
            "6": "seks",
            "7": "syv",
            "8": "åtte",
            "9": "ni"
        }

        # Special translation cases for 10-19
        self.special_trans_dict = {
            10: "ti",
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

        # Translation dict for multiples of tens
        self.tens_trans_dict = {
            "2": "tjue",
            "3": "tretti",
            "4": "førti",
            "5": "femti",
            "6": "seksti",
            "7": "sytti",
            "8": "åtti",
            "9": "nitti"
        }

    def _give_chunk(self, num_str: str, size: int = 3):
        """
        Yield chunks of the number string from right to left.
        """
        while num_str:
            yield num_str[-size:]
            num_str = num_str[:-size]

    def _translate_small_number(self, number: str, use_ett: bool = False) -> str:
        """
        Translate a single-digit number to its Norwegian word.
        """
        if number in self.small_trans_dict:
            translations = self.small_trans_dict[number]
            if isinstance(translations, list):
                return translations[1] if use_ett else translations[0]
            return translations
        return ""

    def _translate_tens_number(self, number: str) -> str:
        """
        Translate a tens digit to its Norwegian word.
        """
        if number in self.tens_trans_dict:
            return self.tens_trans_dict[number]
        return ""

    def convert(self, token: str, context: str = "") -> str:
        """
        Convert a numeric string into its Norwegian text representation.
        The context parameter helps decide whether to use "en" or "ett" for 1.
        """
        # Determine whether to use "ett" based on context
        use_ett = context.lower() in ["ett", "nøytrum"]

        # Clean the input token
        token = self.dot_filter_regex.sub("", token)
        token = self.filter_regex.sub("", token)

        # Handle negative numbers
        prefix = ""
        if token.startswith("-"):
            token = token[1:]
            prefix = "minus"

        text_list = []

        if token == len(token) * "0":
            text_list.append("null")
        else:
            chunks = list(self._give_chunk(token))
            for depth, chunk in enumerate(chunks):
                chunk_text_list = []
                if len(chunk) == 3:
                    hundred, rest = chunk[0], chunk[1:]
                else:
                    hundred, rest = "", chunk

                # Handle hundreds
                if hundred and int(hundred) != 0:
                    chunk_text_list.append(self._translate_small_number(hundred, use_ett=True))
                    chunk_text_list.append("hundre")

                # Handle 10-19
                if int(rest) in self.special_trans_dict:
                    chunk_text_list.append(self.special_trans_dict[int(rest)])
                else:
                    # Handle tens and units
                    if len(rest) == 2 and rest[0] != "0":
                        chunk_text_list.append(self._translate_tens_number(rest[0]))
                        if rest[1] != "0":
                            chunk_text_list[-1] += self._translate_small_number(rest[1], use_ett)
                    elif rest[-1] != "0":
                        chunk_text_list.append(self._translate_small_number(rest[-1], use_ett))

                if depth > 0:
                    # Translate the thousand chunk properly
                    if len(chunk_text_list) == 0:
                        continue
                    if depth == 1:
                        chunk_text_list = [self.special_trans_dict[int(chunk)] if int(chunk) in self.special_trans_dict else self._translate_small_number(chunk)] + ["tusen"]
                    else:
                        suffix_singular, suffix_plural = self.scale_suffixes[depth-1]
                        chunk_text_list.append(suffix_singular if int(chunk) == 1 else suffix_plural)

                text_list = chunk_text_list + text_list

        token = " ".join(text_list)
        if prefix:
            token = f"{prefix} {token}"

        return token
