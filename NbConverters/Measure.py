from singleton_decorator import singleton
import re
from Decimal import Decimal
from Fraction import Fraction

@singleton
class Measure:
    """
    Steps:
    - 1 Filter out commas
    - 2 Try to match a fraction
      - 2.1 If possible, use Fraction convertor
    - 3 Otherwise, try to match "x.y" or "x"
      - 3.1 If possible, use Decimal convertor
    - 4 Iterate over chunks of the remainder, the actual measure
      - 4.1 Try to match with a dictionary while preserving case sensitivity
      - 4.2 Otherwise try to match with a dictionary while ignoring case sensitivity
      - 4.3 Otherwise add the chunk itself to the output
            Note that plurality of the measures is kept track of
    - 5 Handle the edge case where "cubic centimeter" is written as "c c"

    Edge case:
    All cases of "cm3" are converted to "c c" rather than "cubic centimeter"
    """
    def __init__(self):
        super().__init__()
        # Regex to detect fraction
        self.fraction_regex = re.compile(r"(((?:-?\d* )?-?\d+ *\/ *-? *\d+)|(-?\d* *(?:½|⅓|⅔|¼|¾|⅕|⅖|⅗|⅘|⅙|⅚|⅐|⅛|⅜|⅝|⅞|⅑|⅒)))")
        # Regex to detect whether "of a" should be used. Matches only when "of a" should NOT be used
        self.of_a_regex = re.compile(r"(-?\d+ -?\d+ *\/ *-? *\d+)|(-?\d+ *(?:½|⅓|⅔|¼|¾|⅕|⅖|⅗|⅘|⅙|⅚|⅐|⅛|⅜|⅝|⅞|⅑|⅒))")
        # Regex to detect input to pass to digit convertor, including potential million/billion suffix
        self.value_regex = re.compile(r"(-?(?: |\d)*\.?\d+ *(?:thousand|million|billion|trillion|quadrillion|quintillion|sextillion|septillion|octillion|undecillion|tredecillion|quattuordecillion|quindecillion|sexdecillion|septendecillion|octodecillion|novemdecillion|vigintillion)?)")
        # Regex filter to remove commas
        self.filter_regex = re.compile(r"[,]")
        # Regex filter to remove spaces
        self.filter_space_regex = re.compile(r"[ ]")
        # Regex to remove letters
        self.letter_filter_regex = re.compile(r"[^0-9\-\.]")

        # Prefix dict for 10^i with i > 0
        # Prefix dict
        self.prefix_dict = {
            "Y": "yotta",
            "Z": "zetta",
            "E": "exa",
            "P": "peta",
            "T": "tera",
            "G": "giga",
            "M": "mega",
            "k": "kilo",
            "h": "hekto",
            "da": "deka",
            "d": "desi",
            "c": "centi",
            "m": "milli",
            "μ": "mikro",
            "µ": "mikro", # legacy symbol. 
            "n": "nano",
            "p": "piko",
            "f": "femto",
            "a": "atto",
            "z": "zepto",
            "y": "yocto"
        }

        # Translation dict for prefixable measure types. 
        # These will get prefixed with 
        self.prefixable_trans_dict = {
            "m": {
                "singular": "meter",
                "plural": "meter"
            },
            "b": {
                "singular": "bit", # Note that this messes with byte whenever the lowercase is used
                "plural": "bit"
            },
            "B": {
                "singular": "byte",
                "plural": "byte"
            },
            "bps": {
                "singular": "bit per sekund", # Note that this messes with byte whenever the lowercase is used
                "plural": "bit per sekund"
            },
            "Bps": {
                "singular": "byte per sekund",
                "plural": "byte per sekund"
            },
            "g": {
                "singular": "gram",
                "plural": "gram"
            },
            "gf": {
                "singular": "gram kraft",
                "plural": "gram kraft"
            },
            "W": {
                "singular": "watt",
                "plural": "watt"
            },
            "Wh": {
                "singular": "watt time",
                "plural": "watt timer"
            },
            "Hz": {
                "singular": "hertz",
                "plural": "hertz"
            },
            "hz": {
                "singular": "hertz",
                "plural": "hertz"
            },
            "J": {
                "singular": "joule",
                "plural": "joule"
            },
            "L": {
                "singular": "liter",
                "plural": "liter"
            },
            "V": {
                "singular": "volt",
                "plural": "volt"
            },
            "f": {
                "singular": "farad",
                "plural": "farad"
            },
            "s": {
                "singular": "sekund",
                "plural": "sekunder"
            },
            "A": {
                "singular": "ampere",
                "plural": "ampere"
            },
            "Ah": {
                "singular": "ampere time",
                "plural": "ampere timer"
            },
            "Pa": {
                "singular": "pascal",
                "plural": "pascal"
            },
            "C": {
                "singular": "coulomb",
                "plural": "coulomb"
            },
            "Bq": {
                "singular": "becquerel",
                "plural": "becquerel"
            },
            "N": {
                "singular": "newton",
                "plural": "newton"
            },
            "bar": {
                "singular": "bar",
                "plural": "bar"
            },
            "lm": { # TODO: This turns "Klm" -> "kilolumens", while Kilometer may have been intended?
                "singular": "lumen",
                "plural": "lumen"
            },
            "cal": {
                "singular": "kalori",
                "plural": "kalorier"
            },
        }

        # Transformed prefixed dict using self.prefixable_trans_dict and the dict of prefixes
        self.prefixed_dict = {prefix + prefixed: {"singular": self.prefix_dict[prefix] + self.prefixable_trans_dict[prefixed]["singular"], "plural": self.prefix_dict[prefix] + self.prefixable_trans_dict[prefixed]["plural"]} for prefixed in self.prefixable_trans_dict for prefix in self.prefix_dict}
        self.prefixed_dict = {**self.prefixed_dict, **self.prefixable_trans_dict}

        # Translation dict for non-prefixed measure types
        # Also overrides values from self.prefixed_dict, like "mb" -> "millibyte"
        self.custom_dict = {
            "%": {
                "singular": "prosent",
                "plural": "prosent"
            },
            "pc": {
                "singular": "prosent",
                "plural": "prosent"
            },
            "ft": {
                "singular": "fot",
                "plural": "føtter"
            },
            "mi": {
                "singular": "mil",
                "plural": "mil"
            },
            "mb": {
                "singular": "megabyte",
                "plural": "megabyte"
            },
            "ha": {
                "singular": "hektar",
                "plural": "hektar"
            },
            "\"": {
                "singular": "tommer",
                "plural": "tommer"
            },
            "in": {
                "singular": "tommer",
                "plural": "tommer"
            },
            "\'": {
                "singular": "fot",
                "plural": "føtter"
            },
            "rpm": {
                "singular": "omdreining per minutt",
                "plural": "omdreininger per minutt" # on "per x", x is always singular
            },
            "hp": {
                "singular": "hestekrefter",
                "plural": "hestekrefter"
            },
            "cc": {
                "singular": "kubikkcentimeter",
                "plural": "kubikkcentimeter"
            },
            "oz": {
                "singular": "unse",
                "plural": "unser",
            },
            "mph": {
                "singular": "mile per time",
                "plural": "miles per time"
            },
            "lb": {
                "singular": "pund",
                "plural": "pund"
            },
            "lbs": {
                "singular": "pund", # Always plural due to how "lbs" itself is already plural
                "plural": "pund"
            },
            "kt": {
                "singular": "knop",
                "plural": "knop"
            },
            "dB": {
                "singular": "desibel",
                "plural": "desibel"
            },
            "AU": {
                "singular": "astronomisk enhet",
                "plural": "astronomiske enheter"
            },
            "st": {
                "singular": "stein",
                "plural": "stein" # Stein is always singular, eg "ni stein"
            },
            "yd": {
                "singular": "yard",
                "plural": "yard"
            },
            "yr": {
                "singular": "år",
                "plural": "år"
            },
            "yrs": {
                "singular": "år", #TODO Consider years as "yrs" is already plural
                "plural": "år"
            },
            "eV": {
                "singular": "elektron volt",
                "plural": "elektron volt"
            },
            "/": {
                "singular": "per",
                "plural": "per"
            },
            "sq": {
                "singular": "kvadrat",
                "plural": "kvadrat"
            },
            "2": {
                "singular": "kvadrat",
                "plural": "kvadrat"
            },
            "²": {
                "singular": "kvadrat",
                "plural": "kvadrat"
            },
            "3": {
                "singular": "kubikk",
                "plural": "kubikk"
            },
            "³": {
                "singular": "kubikk",
                "plural": "kubikk"
            },
            "h": {
                "singular": "time",
                "plural": "timer"
            },
            "hr": {
                "singular": "time",
                "plural": "timer"
            },
            "hrs": {
                "singular": "time", # TODO: Consider plural as "hrs" is already plural
                "plural": "timer"
            },
            "ch": {
                "singular": "kjede",
                "plural": "kjeder"
            },
            "KiB": {
                "singular": "kibibyte",
                "plural": "kibibyte"
            },
            "MiB": {
                "singular": "mebibyte",
                "plural": "mebibyte"
            },
            "GiB": {
                "singular": "gibibyte",
                "plural": "gibibyte"
            },
            "pH": { # The data parses "pH" as "pico henrys"
                "singular": "p h",
                "plural": "p h"
            },
            "kph": {
                "singular": "kilometer per time",
                "plural": "kilometer per time"
            },
            "Da": {
                "singular": "dalton",
                "plural": "dalton"
            },
            "cwt": {
                "singular": "hundreweight",
                "plural": "hundreweight"
            },
            "Sv": {
                "singular": "sievert",
                "plural": "sievert",
            },
            "C": { # Overrides Coulomb
                "singular": "celsius", 
                "plural": "celsius"
            },
            "degrees": {
                "singular": "grad",
                "plural": "grader"
            },
            "degree": {
                "singular": "grad",
                "plural": "grader"
            },
            "atm": {
                "singular": "atmosfære",
                "plural": "atmosfærer"
            },
            "min": {
                "singular": "minutt",
                "plural": "minutter"
            },
            "cd": {
                "singular": "candela",
                "plural": "candela"
            },
            "ly": {
                "singular": "lysår",
                "plural": "lysår"
            },
            "kts": {
                "singular": "knop",
                "plural": "knop"
            },
            "mol": {
                "singular": "mol",
                "plural": "mol"
            },
            "Nm": { # Overrides nanometers on the lowercase
                "singular": "newton meter",
                "plural": "newton meter"
            },
            "Ω": {
                "singular": "ohm",
                "plural": "ohm"
            },
            "bbl": {
                "singular": "fat",
                "plural": "fat"
            },
            "gal": {
                "singular": "gallon",
                "plural": "gallon"
            },
            "cal": { # This overides "cal" from kalori, while preserving eg "kcal".
            # This overrides "cal" from kalori, while preserving eg "kcal".
                "singular": "kalori",
                "plural": "kalorier"
            },
        }

        # Combine all dictionaries
        self.trans_dict = {**self.prefixed_dict, **self.custom_dict}
        
        # Initialize Decimal and Fraction classes
        self.decimal = Decimal()
        self.fraction = Fraction()
    
    def convert(self, token: str) -> str:
        # 1 Filter out commas
        token = self.filter_regex.sub("", token)

        # Variable to store the value of the input
        value = ""
        measure = ""

        # 2 Try to match a fraction
        match = self.fraction_regex.match(token)
        if match:
            value = self.fraction.convert(match.group(0))
            measure = token[match.span()[1]:].strip()

        else:
            # 3 Try to match x.y or x
            match = self.value_regex.match(token)
            if match:
                value = self.decimal.convert(match.group(0))
                measure = token[match.span()[1]:].strip()

        # List to store measure chunks
        measure_chunks = []
        if measure:
            # 4 Iterate over chunks of the remainder, the actual measure
            for chunk in re.split(r"\s+", measure):
                chunk_trans = self.trans_dict.get(chunk.lower(), None)
                if chunk_trans:
                    # 4.1 Match with a dictionary while preserving case sensitivity
                    chunk_trans = chunk_trans.get("singular" if len(value) == 1 else "plural")
                else:
                    # 4.2 Otherwise, match with a dictionary while ignoring case sensitivity
                    chunk_trans = self.trans_dict.get(chunk.lower(), {"singular": chunk, "plural": chunk}).get("singular" if len(value) == 1 else "plural")
                measure_chunks.append(chunk_trans)
        
        # 5 Handle edge cases
        if measure.lower() == "cc":
            measure_chunks = ["kubikkcentimeter"]

        # Join the value and measure
        result = f"{value} {' '.join(measure_chunks)}"
        return result

