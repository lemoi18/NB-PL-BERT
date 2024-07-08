from singleton_decorator import singleton
import re
from Decimal import Decimal
from Fraction import Fraction

from singleton_decorator import singleton

import re


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
            Note that flertallity of the measures is kept track of
    - 5 Handle the edge case where "cubic centimeter" is written as "c c"

    Edge case:
    All cases of "cm3" are converted to "c c" rather than "cubic centimeter"

    Missed Cases:
        Before          "Correct"                                   Predicted
        1/2 kg          half a kilogram                             one half of a kilogram
        7.62 mm M       seven point six two millimeters             seven point six two millimeters meters
        57m             fifty seven minutes                         fifty seven meters
        2.3Kb           two point three kilobits                    two point three kilobytes
    
    Differences between my predictions and "Correct" values:
        Lack of spaces:
            Before          "Correct"                                   Predicted
            100mA           one hundred milli amperes                   one hundred milliamperes
            200mA           two hundred milli amperes                   two hundred milliamperes
            135 KC          one hundred thirty five kilo coulombs       one hundred thirty five kilocoulombs
            97Gs            ninety seven giga seconds                   ninety seven gigaseconds
            ...             ...                                         ...
            Note that several hundred of these occurrences exist within the training data.
        
        Incorrect measure on the data's side:
            Before          "Correct"                                   Predicted
            13.0 pH         thirteen point zero pico henrys             thirteen point zero p h

        No translation on the data's side:
            Before          "Correct"                                   Predicted
            30 million km   30 million km                               thirty million kilometers
            549 KiB         549 KiB                                     five hundred forty nine kibibytes
            1.60 MiB        1.60 MiB                                    one point six o mebibytes
            1000/year       one thousand per years                      one thousand per year
            ...             ...                                         ...
            Note that several dozens of these occurrences exist within the training data.
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
            "h": "hecto",
            "da": "deca",
            "d": "deci",
            "c": "centi",
            "m": "milli",
            "μ": "micro",
            "µ": "micro", # legacy symbol. 
            "n": "nano",
            "p": "pico",
            "f": "femto",
            "a": "atto",
            "z": "zepto",
            "y": "yocto"
        }

        # Translation dict for prefixable measure types. 
        # These will get prefixed with 
        self.prefixable_trans_dict = {
            "m": {
                "entall": "meter",
                "flertall": "meter"
            },
            "b": {
                "entall": "bit", # Merk at dette forstyrrer byte når det brukes i små bokstaver
                "flertall": "biter"
            },
            "B": {
                "entall": "byte",
                "flertall": "bytes"
            },
            "bps": {
                "entall": "bit per sekund", # Merk at dette forstyrrer byte når det brukes i små bokstaver
                "flertall": "biter per sekund"
            },
            "Bps": {
                "entall": "byte per sekund",
                "flertall": "bytes per sekund"
            },
            "g": {
                "entall": "gram",
                "flertall": "gram"
            },
            "gf": {
                "entall": "gram kraft",
                "flertall": "gram kraft"
            },
            "W": {
                "entall": "watt",
                "flertall": "watt"
            },
            "Wh": {
                "entall": "watt time",
                "flertall": "watt timer"
            },
            "Hz": {
                "entall": "hertz",
                "flertall": "hertz"
            },
            "hz": {
                "entall": "hertz",
                "flertall": "hertz"
            },
            "J": {
                "entall": "joule",
                "flertall": "joule"
            },
            "L": {
                "entall": "liter",
                "flertall": "liter"
            },
            "V": {
                "entall": "volt",
                "flertall": "volt"
            },
            "f": {
                "entall": "farad",
                "flertall": "farad"
            },
            "s": {
                "entall": "sekund",
                "flertall": "sekunder"
            },
            "A": {
                "entall": "ampere",
                "flertall": "ampere"
            },
            "Ah": {
                "entall": "amp time",
                "flertall": "amp timer"
            },
            "Pa": {
                "entall": "pascal",
                "flertall": "pascal"
            },
            "s": {
                "entall": "sekund",
                "flertall": "sekunder"
            },
            "C": {
                "entall": "coulomb",
                "flertall": "coulomb"
            },
            "Bq": {
                "entall": "becquerel",
                "flertall": "becquerel"
            },
            "N": {
                "entall": "newton",
                "flertall": "newton"
            },
            "bar": {
                "entall": "bar",
                "flertall": "bar"
            },
            "lm": { # TODO: Dette endrer "Klm" -> "kilolumen", mens Kilometer kan ha vært ment?
                "entall": "lumen",
                "flertall": "lumen"
            },
            "cal": {
                "entall": "kalori",
                "flertall": "kalorier"
            },
        }

        # Transformed prefixed dict using self.prefixable_trans_dict and the dict of prefixes
        self.prefixed_dict = {prefix + prefixed: {"entall": self.prefix_dict[prefix] + self.prefixable_trans_dict[prefixed]["entall"], "flertall": self.prefix_dict[prefix] + self.prefixable_trans_dict[prefixed]["flertall"]} for prefixed in self.prefixable_trans_dict for prefix in self.prefix_dict}
        self.prefixed_dict = {**self.prefixed_dict, **self.prefixable_trans_dict}

        # Translation dict for non-prefixed measure types
        # Also overrides values from self.prefixed_dict, like "mb" -> "millibyte"
        self.custom_dict = {
            "%": {
                "entall": "prosent",
                "flertall": "prosent"
            },
            "pc": {
                "entall": "prosent",
                "flertall": "prosent"
            },
            "ft": {
                "entall": "fot",
                "flertall": "fot"
            },
            "mi": {
                "entall": "mile",
                "flertall": "miles"
            },
            "mb": {
                "entall": "megabyte",
                "flertall": "megabytes"
            },
            "ha": {
                "entall": "hektar",
                "flertall": "hektar"
            },
            "\"": {
                "entall": "tommer",
                "flertall": "tommer"
            },
            "in": {
                "entall": "tommer",
                "flertall": "tommer"
            },
            "\'": {
                "entall": "foot",
                "flertall": "feet"
            },
            "rpm": {
                "entall": "omdreining per minutt",
                "flertall": "omdreining per minutt" # on "per x", x is always entall
            },
            "hp": {
                "entall": "hestekrefter",
                "flertall": "hestekrefter"
            },
            "cc": {
                "entall": "c c",
                "flertall": "c c"
            },
            "oz": {
                "entall": "ounce",
                "flertall": "ounces",
            },
            "mph": {
                "entall": "mile per hour",
                "flertall": "miles per hour"
            },
            "lb": {
                "entall": "pound",
                "flertall": "pounds"
            },
            "lbs": {
                "entall": "pounds", # Always flertall due to how "lbs" itself is already flertall
                "flertall": "pounds"
            },
            "kt": {
                "entall": "knot",
                "flertall": "knots"
            },
            "dB": {
                "entall": "desibel",
                "flertall": "desibel"
            },
            "AU": {
                "entall": "astronomical unit",
                "flertall": "astronomical units"
            },
            "st": {
                "entall": "stone",
                "flertall": "stone" # Stone is always entall, eg "nine stone"
            },
            "yd": {
                "entall": "yard",
                "flertall": "yards"
            },
            "eV": {
                "entall": "electron volt",
                "flertall": "electron volts"
            },
            "/": {
                "entall": "per",
                "flertall": "per"
            },
            "sq": {
                "entall": "kvadrat",
                "flertall": "kvadrat"
            },
            "2": {
                "entall": "kvadrat",
                "flertall": "kvadrat"
            },
            "²": {
                "entall": "kvadrat",
                "flertall": "kvadrat"
            },
            "3": {
                "entall": "cubic",
                "flertall": "cubic"
            },
            "³": {
                "entall": "kubikk",
                "flertall": "kubikk"
            },
            "h": {
                "entall": "hour",
                "flertall": "hours"
            },
            "hr": {
                "entall": "hour",
                "flertall": "hours"
            },
            "t": {
                "entall": "time", # TODO: Consider flertall as "hrs" is already flertall
                "flertall": "timer"
            },
            "KiB": {
                "entall": "kibibyte",
                "flertall": "kibibytes"
            },
            "MiB": {
                "entall": "mebibyte",
                "flertall": "mebibytes"
            },
            "GiB": {
                "entall": "gibibyte",
                "flertall": "gibibytes"
            },
            "pH": { # The data parses "pH" as "pico henrys"
                "entall": "p h",
                "flertall": "p h"
            },
            "kmt": {
                "entall": "kilometer per time",
                "flertall": "kilometers per timer"
            },
            "Sv": {
                "entall": "sievert",
                "flertall": "sieverts",
            },
            "C": { # Overrides Coulomb
                "entall": "celcius", 
                "flertall": "celcius"
            },
            "grader": {
                "entall": "grad",
                "flertall": "grader"
            },
            "grad": {
                "entall": "grad",
                "flertall": "grader"
            },
            "atm": {
                "entall": "atmosfære",
                "flertall": "atmosfærer"
            },
            "min": {
                "entall": "minutt",
                "flertall": "minutter"
            },
            "mol": {
                "entall": "mol",
                "flertall": "mole"
            },
            "Nm": { # Overrides nanometers on the lowercase
                "entall": "newton meter",
                "flertall": "newton meters"
            },
            "Ω": {
                "entall": "ohm",
                "flertall": "ohms"
            },
            "bbl": {
                "entall": "barrel",
                "flertall": "barrels"
            },
            "gal": {
                "entall": "gallon",
                "flertall": "gallons"
            },
            "cal": { # This overides "cal" from calorie, while preserving eg "kcal". "cal" is more often used to refer to caliber than calorie I reckon, hence this entry
                "entall": "cal",
                "flertall": "cal"
            }
        }
        # Overstyr og legg til verdier fra custom_dict til prefixed_dict
        self.prefixed_dict = {**self.prefixed_dict, **self.custom_dict}

        # Versjon med små bokstaver av self.prefixed_dict
        self.lower_prefixed_dict = {key.lower(): self.prefixed_dict[key] for key in self.prefixed_dict}
        # Merk, byte og bit overlapper.                               Byte har forrang
        # elektronvolt og exavolt overlapper.                      Elektronvolt har forrang
        # hektar og hektoampere overlapper.                        Hektar har forrang
        # pascal og picoampere og petaampere overlapper.         Pascal har forrang
        # mega... og milli... overlapper.                             Milli... har forrang
        # piko... og peta... overlapper.                              Piko... har forrang
        # zetta... og zepto... overlapper.                            Zepto... har forrang
        # yotta... og yocto... overlapper.                            Yocto... har forrang
        # Daltons og desiamperes overlapper.                          Daltons har forrang
        # Flere overlapp kan eksistere

        # Spesielle suffikser hvor hele suffikset skal deles
        self.special_suffixes = re.compile(r"(\/|per(?!cent)|sq|2|²|3|³)")

        # Desimal- og Brøk-konvertering
        self.decimal = Decimal()
        self.fraction = Fraction()

    def convert(self, token: str) -> str:
        print(f"Original token: {token}")
        token = self.filter_regex.sub("", token)
        print(f"Token after removing commas: {token}")
        
        result_list = []
        plural = False

        match = self.fraction_regex.match(token)
        if match:
            print(f"Fraction match: {match.group(0)}")
            result_list.append(self.fraction.convert(match.group(0)))
            token = token[:match.span()[0]] + token[match.span()[1]:]
            token = self.filter_space_regex.sub("", token)
            print(f"Token after fraction processing: {token}")
            if self.of_a_regex.match(match.group(0)):
                plural = True
            else:
                result_list.append("av en" if token and token[0] in list("aeiou") else "av en")
        else:
            match = self.value_regex.match(token)
            if match:
                print(f"Value match: {match.group(1)}")
                result_list.append(self.decimal.convert(self.filter_space_regex.sub("", match.group(1))))
                token = token[:match.span()[0]] + token[match.span()[1]:]
                print(f"Token after value processing: {token}")
                if abs(float(self.letter_filter_regex.sub("", match.group(1)))) != 1 or "." in match.group(1):
                    plural = True

        per = False
        for split_token in token.split(" "):
            for i, token in enumerate(self.split_token(split_token)):
                print(f"Processing split token: {token}")
                if token in self.prefixed_dict:
                    result_list.append(self.prefixed_dict[token]["flertall" if plural and not per else "entall"])
                elif token.lower() in self.lower_prefixed_dict:
                    result_list.append(self.lower_prefixed_dict[token.lower()]["flertall" if plural and not per else "entall"])
                else:
                    result_list.append(token)
                if result_list[-1] == "per" and i != 0:
                    per = True
                elif result_list[-1] not in ("kvadrat", "kubikk"):
                    per = False
        
        result = " ".join(result_list)
        print(f"Result before edge case handling: {result}")
        result = re.sub(r"kubikkcentimeter?", "c c", result)
        print(f"Final result: {result}")

        return result

        
    def split_token(self, token: str) -> str:
        while True:
            # Finn match for suffiksseparator
            match = self.special_suffixes.search(token)
            if match:
                # Få start- og sluttindeks for match
                s1, s2 = match.span()
                if match.group(1) in ("sq", "2", "²", "3", "³"):
                    yield token[s1:s2]
                    if token[:s1]:
                        yield token[:s1]
                else:
                    if token[:s1]:
                        yield token[:s1]
                    yield token[s1:s2]
                
                # Reduser token
                token = token[s2:]
            else:
                # Hvis det ikke er noen match, returner resten av token, hvis ikke tom
                if token:
                    yield token
                # Avslutt while-løkken
                break