from singleton_decorator import singleton
import re, os
from Cardinal import Cardinal
from Digit import Digit

@singleton
class Money:
    """
    Converts monetary amounts to their full Norwegian text representation.
    """
    def __init__(self):
        super().__init__()
        # Regex to detect input of the sort "x.y" or ".y"
        self.decimal_regex = re.compile(r"(.*?)(-?\d*)\.(\d+)(.*)")
        # Regex to detect a number
        self.number_regex = re.compile(r"(.*?)(-?\d+)(.*)")
        # Regex filter to remove commas and spaces
        self.filter_regex = re.compile(r"[, ]")

        # Suffixes for currencies with decimal support
        # In a perfect world this dict would contain all currencies
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

        # Suffixes for currencies
        with open(os.path.join(os.path.dirname(__file__), "money.json"), "r") as f:
            import json
            self.currencies = {**json.load(f), **self.currencies}

        # List of potential suffixes
        self.suffixes = [
            "lakh",
            "crore",
            "thousand",
            "million",
            "billion",
            "trillion",
            "quadrillion",
            "quintillion",
            "sextillion",
            "septillion",
            "octillion",
            "undecillion",
            "tredecillion",
            "quattuordecillion",
            "quindecillion",
            "sexdecillion",
            "septendecillion",
            "octodecillion",
            "novemdecillion",
            "vigintillion"
        ]

        # Dict of abbreviated suffixes, or other suffixes that need transformations
        self.abbr_suffixes = {
            "k": "thousand",
            "m": "million",
            "bn": "billion",
            "b": "billion",
            "t": "trillion",
            "cr": "crore",
            "crores": "crore",
            "lakhs": "lakh",
            "lacs": "lakh"
        }

        # Regular expression to detect the suffixes
        self.suffix_regex = re.compile(f"(quattuordecillion|septendecillion|novemdecillion|quindecillion|octodecillion|tredecillion|sexdecillion|vigintillion|quadrillion|quintillion|undecillion|sextillion|septillion|octillion|thousand|trillion|million|billion|crores|crore|lakhs|lakh|lacs|bn|cr|k|m|b|t)(.*)", flags=re.I)

        self.currency_regex = re.compile(r"(.*?)(dollar|usd|rs\.|r\$|aed|afn|all|amd|ang|aoa|ars|aud|awg|azn|bam|bbd|bdt|bgn|bhd|bif|bmd|bnd|bob|brl|bsd|btc|btn|bwp|byn|bzd|cad|cdf|chf|clf|clp|cnh|cny|cop|crc|cuc|cup|cve|czk|djf|dkk|dop|dzd|egp|ern|etb|eur|fjd|fkp|gbp|gel|ggp|ghs|gip|gmd|gnf|gtq|gyd|hkd|hnl|hrk|htg|huf|idr|ils|imp|inr|iqd|irr|isk|jep|jmd|jod|jpy|kes|kgs|khr|kmf|kpw|krw|kwd|kyd|kzt|lak|lbp|lkr|lrd|lsl|lyd|mad|mdl|mga|mkd|mmk|mnt|mop|mro|mru|mur|mvr|mwk|mxn|myr|mzn|nad|ngn|nio|nok|npr|nzd|omr|pab|pen|pgk|php|pkr|pln|pyg|qar|ron|rsd|rub|rwf|sar|sbd|scr|sdg|sek|sgd|shp|sll|sos|srd|ssp|std|stn|svc|syp|szl|thb|tjs|tmt|tnd|top|try|ttd|twd|tzs|uah|ugx|usd|uyu|uzs|vef|vnd|vuv|wst|xaf|xag|xau|xcd|xdr|xof|xpd|xpf|xpt|yer|zar|zmw|zwl|fim|bef|cyp|ats|ltl|zl|u\$s|rs|tk|r$|dm|\$|€|£|¥)(.*?)", flags=re.I)

        # Cardinal and Digit conversion
        self.cardinal = Cardinal()
        self.digit = Digit()

    def convert(self, token: str) -> str:
        # 1 Remove commas and spaces
        token = self.filter_regex.sub("", token)

        # Before and After track sections before and after a number respectively
        before = ""
        after = ""

        # Currency will be a dict for the currency
        currency = None

        # Number represents x in "x.y" or "x", while number represents y
        number = ""
        decimal = ""

        # Scale represents the numerical scale, eg "million" or "lakh"
        scale = ""

        # 2 Try to match a decimal of roughly the form x.y
        # Match the reverse so the regex "anchors" around the last dot instead of the first.
        # This helps with cases such as "Rs.12.38".
        match = self.decimal_regex.search(token[::-1])
        if match:
            # If there is a match, store what appears before and after the match
            # as well as the number and decimal values.
            before = match.group(4)[::-1]
            number = match.group(3)[::-1]
            decimal = match.group(2)[::-1]
            after = match.group(1)[::-1]

        else:
            # 3 Otherwise, try to match an integer
            match = self.number_regex.search(token)
            if match:
                before = match.group(1)
                number = match.group(2)
                after = match.group(3)

        # 4 Check the text before the number for a currency
        if before:
            before = before.lower()
            if before in self.currencies:
                currency = self.currencies[before]
            elif before[-1] in self.currencies:
                currency = self.currencies[before[-1]]

        # 5 Check after for currency and or suffixes
        if after:
            # 5.1 Match from start of after, no case, to try and find suffixes like "thousand", "million", "bn"
            match = self.suffix_regex.match(after)
            if match:
                scale = match.group(1).lower()
                scale = self.abbr_suffixes[scale] if scale in self.abbr_suffixes else scale
                after = match.group(2)

            # 5.2 Match from start of after, no case, try to find currencies
            if after.lower() in self.currencies:
                currency = self.currencies[after.lower()]
                after = ""

        # Decimal_support tracks whether the current currency supports decimal values
        # for "one euro and fifteen cents" instead of "one point fifteen euro"
        decimal_support = currency and "number" in currency
        result_list = []
        if decimal_support and not scale:
            # 6 If the current currency has decimal support and there is no scale like million, 
            # then we want to output like "x kroner y øre"

            # Only output number if:
            # Number exists and
            #   Number is not 0
            #   OR
            #   Number is 0 but there is no decimal
            if number and (number != "0" or not decimal):
                result_list.append(self.cardinal.convert(number))
                result_list.append(currency["number"]["singular" if number == "1" else "plural"])
                if decimal and decimal != "0" * len(decimal):
                    result_list.append("og")
            # If a decimal exists and it's not just 0's, then pad it to length 2 and add the cardinal representation of the value
            # plus the text representation of the decimal, eg "øre"
            if decimal and decimal != "0" * len(decimal):
                # Pad decimal to length 2. "5" -> "50"
                decimal = f"{decimal:0<2}"
                result_list.append(self.cardinal.convert(decimal))
                result_list.append(currency["decimal"]["singular" if decimal == "01" else "plural"])
        
        else:
            # 7 If there is a scale or no decimal support, output should be like "en point to millioner kroner"
            if number:
                result_list.append(self.cardinal.convert(number))
            if decimal and decimal != "0" * len(decimal):
                result_list.append("point")
                result_list.append(self.digit.convert(decimal))
            # If "million" exists:
            if scale:
                result_list.append(scale)
            # Add currency
            if currency:
                # Ensure currency is of the form {'singular': '...', 'plural': '...'}
                if decimal_support:
                    currency = currency["number"]
                # Add the currency in singular when these conditions apply
                if number == "1" and not decimal and not scale:
                    result_list.append(currency["singular"])
                else:
                    result_list.append(currency["plural"])
        
        # 8 Append a potentially remaining "after"
        if after:
            result_list.append(after.lower())

        # Convert list of values into the final result
        result = " ".join(result_list)

        return result
