from singleton_decorator import singleton
import re, os
from Cardinal import Cardinal
import json

@singleton
class Money:
    """
    Handles the conversion of monetary values to their textual representation in Norwegian.
    """
    def __init__(self):
        super().__init__()
        self.decimal_regex = re.compile(r"(.*?)(-?\d*)\.(\d+)(.*)")
        self.number_regex = re.compile(r"(.*?)(-?\d+)(.*)")
        self.filter_regex = re.compile(r"[, ]")

        self.currencies = {
            "$": {
                "number": {
                    "singular": "dollar",
                    "plural": "dollar"
                },
                "decimal": {
                    "singular": "cent",
                    "plural": "cent"
                }
            },
            "usd": {
                "number": {
                    "singular": "amerikansk dollar",
                    "plural": "amerikanske dollar"
                },
                "decimal": {
                    "singular": "cent",
                    "plural": "cent"
                }
            },
            "€": {
                "number": {
                    "singular": "euro",
                    "plural": "euro"
                },
                "decimal": {
                    "singular": "cent",
                    "plural": "cent"
                }
            },
            "£": {
                "number": {
                    "singular": "pund",
                    "plural": "pund"
                },
                "decimal": {
                    "singular": "penny",
                    "plural": "pence"
                }
            },
            "kr": {
                "number": {
                    "singular": "krone",
                    "plural": "kroner"
                },
                "decimal": {
                    "singular": "øre",
                    "plural": "øre"
                }
            },
            "nok": {
                "number": {
                    "singular": "norsk krone",
                    "plural": "norske kroner"
                },
                "decimal": {
                    "singular": "øre",
                    "plural": "øre"
                }
            }
        }

        #with open(os.path.join(os.path.dirname(__file__), "money.json"), "r") as f:
         #   self.currencies.update(json.load(f))

        # List of potential suffixes in Norwegian
        self.suffixes = [
            "tusen", "million", "milliard", "billion", "billiard", 
            "trillion", "trilliard", "kvadrillion", "kvintillion", 
            "sekstillion", "septillion", "oktilion", "nonillion", "desillion"
        ]

        # Dict of abbreviated suffixes, or other suffixes that need transformations in Norwegian
        self.abbr_suffixes = {
            "k": "tusen",
            "m": "million",
            "bn": "milliard",
            "b": "milliard",
            "t": "billion"
        }

        # Ensure suffix_regex does not interfere with currency symbols
        self.suffix_regex = re.compile(f"({'|'.join(self.abbr_suffixes.keys())})(.*)", flags=re.I)
        self.currency_regex = re.compile(r"(.*?)(dollar|usd|€|£|kr|nok)(.*?)", flags=re.I)

        self.cardinal = Cardinal()

    def convert(self, token: str) -> str:
        token = self.filter_regex.sub("", token)

        before = ""
        after = ""
        currency = None
        number = ""
        decimal = ""
        scale = ""

        match = self.decimal_regex.search(token[::-1])
        if match:
            before = match.group(4)[::-1]
            number = match.group(3)[::-1]
            decimal = match.group(2)[::-1]
            after = match.group(1)[::-1]
        else:
            match = self.number_regex.search(token)
            if match:
                before = match.group(1)
                number = match.group(2)
                after = match.group(3)

        if before:
            before = before.lower()
            if before in self.currencies:
                currency = self.currencies[before]
            elif before[-1] in self.currencies:
                currency = self.currencies[before[-1]]

        if after:
            # Ensure currency matching happens before suffix matching
            if after.lower() in self.currencies:
                currency = self.currencies[after.lower()]
                after = ""
            else:
                match = self.suffix_regex.match(after)
                if match:
                    scale = match.group(1).lower()
                    scale = self.abbr_suffixes[scale] if scale in self.abbr_suffixes else scale
                    after = match.group(2)

        decimal_support = currency and "number" in currency
        result_list = []
        if decimal_support and not scale:
            if number and (number != "0" or not decimal):
                result_list.append(self.cardinal.convert(number))
                result_list.append(currency["number"]["singular" if number == "1" else "plural"])
                if decimal and decimal != "0" * len(decimal):
                    result_list.append("og")
            if decimal and decimal != "0" * len(decimal):
                decimal = f"{decimal:0<2}"
                result_list.append(self.cardinal.convert(decimal))
                result_list.append(currency["decimal"]["singular" if decimal == "01" else "plural"])
        else:
            if number:
                result_list.append(self.cardinal.convert(number))
            if decimal and decimal != "0" * len(decimal):
                result_list.append("og")
                result_list.append(self.cardinal.convert(decimal))  # Use cardinal for digit conversion
            if scale:
                result_list.append(scale)
            if currency:
                if decimal_support:
                    currency = currency["number"]
                if number == "1" and not decimal and not scale:
                    result_list.append(currency["singular"])
                else:
                    result_list.append(currency["plural"])

        if after:
            result_list.append(after.lower())

        result = " ".join(result_list)
        return result
