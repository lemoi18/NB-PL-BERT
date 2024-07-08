from singleton_decorator import singleton
import re
from Cardinal import Cardinal

@singleton
class Fraction:
    """
    Converts fractions to their textual representation in Norwegian.
    """
    def __init__(self):
        super().__init__()
        self.filter_regex = re.compile(",")
        self.space_filter_regex = re.compile(" ")
        self.trans_dict = {
            "½": {"prepended": "en", "single": "en", "text": "halv"},
            "⅓": {"prepended": "en", "single": "en", "text": "tredjedel"},
            "⅔": {"prepended": "to", "single": "to", "text": "tredjedeler"},
            "¼": {"prepended": "en", "single": "en", "text": "fjerdedel"},
            "¾": {"prepended": "tre", "single": "tre", "text": "fjerdedeler"},
            "⅕": {"prepended": "en", "single": "en", "text": "femtedel"},
            "⅖": {"prepended": "to", "single": "to", "text": "femtedeler"},
            "⅗": {"prepended": "tre", "single": "tre", "text": "femtedeler"},
            "⅘": {"prepended": "fire", "single": "fire", "text": "femtedeler"},
            "⅙": {"prepended": "en", "single": "en", "text": "sjettedel"},
            "⅚": {"prepended": "fem", "single": "fem", "text": "sjettedeler"},
            "⅐": {"prepended": "en", "single": "en", "text": "syvendedel"},
            "⅛": {"prepended": "en", "single": "en", "text": "åttendedel"},
            "⅜": {"prepended": "tre", "single": "tre", "text": "åttendedeler"},
            "⅝": {"prepended": "fem", "single": "fem", "text": "åttendedeler"},
            "⅞": {"prepended": "syv", "single": "syv", "text": "åttendedeler"},
            "⅑": {"prepended": "en", "single": "en", "text": "niendedel"},
            "⅒": {"prepended": "en", "single": "en", "text": "tiendedel"}
        }
        self.special_regex = re.compile(f"({'|'.join(self.trans_dict.keys())})")
        self.cardinal = Cardinal()
        self.slash_regex = re.compile(r"(-?\d{1,3}( \d{3})+|-?\d+) *\/ *(-?\d{1,3}( \d{3})+|-?\d+)")
        self.trans_denominator = {
            "null": "nullte", "en": "første", "to": "andre", "tre": "tredje", "fire": "fjerde",
            "fem": "femte", "seks": "sjette", "syv": "syvende", "åtte": "åttende", "ni": "niende",
            "ti": "tiende", "elleve": "ellevte", "tolv": "tolvte", "tretten": "trettende",
            "fjorten": "fjortende", "femten": "femtende", "seksten": "sekstende", "sytten": "syttende",
            "atten": "attende", "nitten": "nittende", "tyve": "tyvende", "hundre": "hundrede",
            "tusen": "tusende", "million": "millionte", "milliard": "milliardte", "billion": "billionte"
        }

        self.edge_dict = {
            "1": {"singular": "over en", "plural": "over en"},
            "2": {"singular": "halv", "plural": "halv"},
            "4": {"singular": "fjerdedel", "plural": "fjerdedeler"}
        }
        self.small_denominators = {
            "1": {"singular": "over en", "plural": "over en"},
            "2": {"singular": "halv", "plural": "halv"},
            "3": {"singular": "tredjedel", "plural": "tredjedeler"},
            "4": {"singular": "fjerdedel", "plural": "fjerdedeler"},
            "5": {"singular": "femtedel", "plural": "femtedeler"},
            "6": {"singular": "sjettedel", "plural": "sjettedeler"},
            "7": {"singular": "syvendedel", "plural": "syvendedeler"},
            "8": {"singular": "åttendedel", "plural": "åttendedeler"},
            "9": {"singular": "niendedel", "plural": "niendedeler"},
            "10": {"singular": "tiendedel", "plural": "tiendedeler"},
            "11": {"singular": "ellevte", "plural": "ellevtedeler"},
            "12": {"singular": "tolvte", "plural": "tolvtedeler"}
        }

    def convert(self, token: str) -> str:
        # 1 Filter commas and dots, but keep spaces
        token = self.filter_regex.sub("", token)
        # 2 Check for special unicode case
        match = self.special_regex.search(token)
        if match:
            # 3 Get fraction match from first group
            frac = match.group(1)
            frac_dict = self.trans_dict[frac]

            # 4 Check whether remainder contains a number, e.g., in "1½"
            remainder = self.special_regex.sub("", token)
            # 5 If it does, convert it using the Cardinal conversion: "1202" -> "en tusen to hundre to"
            if remainder:
                prefix = self.cardinal.convert(remainder)
                result = f"{prefix} og {frac_dict['prepended']} {frac_dict['text']}"
            else:
                result = f"{frac_dict['single']} {frac_dict['text']}"
        
        else:
            # 6 Match .../... as two groups
            match = self.slash_regex.search(token)
            if match:
                # 7 Get the numerator and denominators from the groups
                numerator = match.group(1)
                denominator = match.group(3)
                
                # 8 Strip the numerator and denominator of spaces
                numerator = self.space_filter_regex.sub("", numerator)
                denominator = self.space_filter_regex.sub("", denominator)

                # 9 The numerator is a number in cardinal style
                numerator_text = self.cardinal.convert(numerator)

                # 10 Check if the denominator is a small denominator
                if denominator in self.small_denominators:
                    denominator_text = self.small_denominators[denominator]['plural' if int(numerator) > 1 else 'singular']
                else:
                    # Handle edge cases
                    if denominator in self.edge_dict:
                        result = f"{numerator_text} {self.edge_dict[denominator][('singular' if abs(int(numerator)) == 1 else 'plural')]}"
                    else:
                        # 11 Convert the denominator to ordinal style
                        denominator_text_list = self.cardinal.convert(denominator).split(" ")
                        last_word = denominator_text_list[-1]
                        if last_word in self.trans_denominator:
                            denominator_text_list[-1] = self.trans_denominator[last_word]
                        else:
                            # For large numbers, allow both ordinal and -del suffix forms
                            ordinal_form = f"{last_word}te"
                            del_form = f"{last_word}del"
                            if abs(int(numerator)) != 1:
                                ordinal_form += "er"
                                del_form += "er"
                            denominator_text_list[-1] = f"{del_form}"
                        denominator_text = " ".join(denominator_text_list)
                
                result = f"{numerator_text} {denominator_text}"
                
                # 12 Get remaining values
                remainder = self.slash_regex.sub("", token)
                if remainder:
                    # 13 Transform remaining values to cardinal
                    remainder_text = self.cardinal.convert(remainder)
                    # Potentially transform "en" to "en" if possible
                    result_list = result.split()
                    if result_list[0] == "en":
                        result_list[0] = "en"
                    # Prepend the remaining values in cardinal style
                    result = f"{remainder_text} og {' '.join(result_list)}"
            
            else:
                # Unhandled case. Should not occur if token really is of the FRACTION class
                result = token

        return result
