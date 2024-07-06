
from singleton_decorator import singleton
import re
from Cardinal import Cardinal
from Ordinal import Ordinal

@singleton
class Date:
    """
    Steps:
    - 1 Preprocess token
      - 1.1 Remove dots from token
      - 1.2 Remove "th", "nd", etc. from "5th July" while preserving "Thursday"
      - 1.3 Check for a day prefix, eg "Thursday 5 may"
      - 1.4 Check for "the" prefix, eg "the 5 july"
    - 2 Match "DD Month" or "Month DD"
    - 3 Match "MM-DD-YY(YY)", "YY(YY)-MM-DD", "DD-Month-YY(YY)", "YY(YY)-Month-DD" or "Month-DD-YY(YY)"
    - 4 Match "DD Month YYYY", "Month YYYY", "YYYY", "YYYYs" or "Month DD, YYYY"

    Edge cases:
    "Thursday 5th of May" -> "torsdag femte av mai"
    "90s"                 -> "nittiårene"
    "December 2010s"      -> "desember tjue tiårene"
    "13 AD"               -> "tretten e kr"
    """
    def __init__(self):
        super().__init__()
        # Regex to remove dots
        self.filter_regex = re.compile(r"[,']")
        # Regex to check for a prefixed day
        self.day_regex = re.compile(r"^(?P<prefix>monday|tuesday|wednesday|thursday|friday|saturday|sunday|mon|tue|wed|thu|fri|sat|sun)\.?", flags=re.I)

        # Regex to check for yyyy-mm-dd date
        self.dash_date_ymd_regex = re.compile(r"^(?P<year>\d{2,5}) *(?:-|\.|/) *(?P<month>\d{1,2}) *(?:-|\.|/) *(?P<day>\d{1,2})$", flags=re.I)
        # Regex to check for mm-dd-yyyy date
        self.dash_date_mdy_regex = re.compile(r"^(?P<month>\d{1,2}) *(?:-|\.|/) *(?P<day>\d{1,2}) *(?:-|\.|/) *(?P<year>\d{2,5})$", flags=re.I)

        # Regex to check for YYYY-Month-DD
        self.text_ymd_regex = re.compile(r"^(?P<year>\d{2,5}) *(?:-|\.|/) *(?P<month>januar|februar|mars|april|mai|juni|juli|august|september|oktober|november|desember|sept|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec) *(?:-|\.|/) *(?P<day>\d{1,2})$", flags=re.I)
        # Regex to check for DD-Month-YYYY
        self.text_dmy_regex = re.compile(r"^(?P<day>\d{1,2}) *(?:-|\.|/) *(?P<month>januar|februar|mars|april|mai|juni|juli|august|september|oktober|november|desember|sept|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec) *(?:-|\.|/) *(?P<year>\d{2,5})$", flags=re.I)
        # Regex to check for Month-DD-YYYY
        self.text_mdy_regex = re.compile(r"^(?P<month>januar|februar|mars|april|mai|juni|juli|august|september|oktober|november|desember|sept|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)?\.? *(?P<day>\d{1,2})? +(?P<year>\d{1,5})(?P<suffix>s?)\/?(?: *(?P<bcsuffix>[A-Z\.]+)?)$", flags=re.I)

        # Regex to check for DD Month YYYY, Month YYYY, YYYY or YYYYs
        self.dmy_regex = re.compile(r"^(?:(?:(?P<day>\d{1,2}) +(of +)?)?(?P<month>januar|februar|mars|april|mai|juni|juli|august|september|oktober|november|desember|sept|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\.? +)?(?P<year>\d{1,5})(?P<suffix>s?)\/?(?: *(?P<bcsuffix>[A-Z\.]+)?)$", flags=re.I)
        # Regex to check for Month DD
        self.md_regex = re.compile(r"^(?P<month>januar|februar|mars|april|mai|juni|juli|august|september|oktober|november|desember|sept|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\.? +(?P<day>\d{1,2})(?: *(?P<bcsuffix>[A-Z\.]+)?)$", flags=re.I)

        # Regex to find "th" in "5th", "nd" in "22nd", "rd" in "3rd", without matching "thursday", "monday", etc.
        self.th_regex = re.compile(r"(?:(?<=\d)|(?<=\d ))(?:th|nd|rd|st)", flags=re.I)

        # Translation dict to convert potential months to the correct format
        self.trans_month_dict = {
            "jan": "januar",
            "feb": "februar",
            "mar": "mars",
            "apr": "april",
            "may": "mai",
            "jun": "juni",
            "jul": "juli",
            "aug": "august",
            "sep": "september",
            "oct": "oktober",
            "nov": "november",
            "dec": "desember",
            "sept": "september",
            "01": "januar",
            "02": "februar",
            "03": "mars",
            "04": "april",
            "05": "mai",
            "06": "juni",
            "07": "juli",
            "08": "august",
            "09": "september",
            "10": "oktober",
            "11": "november",
            "12": "desember",
            "1": "januar",
            "2": "februar",
            "3": "mars",
            "4": "april",
            "5": "mai",
            "6": "juni",
            "7": "juli",
            "8": "august",
            "9": "september"
        }

        # Translation dict to convert days to the correct format
        self.trans_day_dict = {
            "man": "mandag",
            "tir": "tirsdag",
            "ons": "onsdag",
            "tor": "torsdag",
            "fre": "fredag",
            "lør": "lørdag",
            "søn": "søndag"
        }

        # Cardinal and Ordinal conversion
        self.cardinal = Cardinal()
        self.ordinal = Ordinal()
    
    def convert(self, token: str) -> str:

        # dmy to true means the format is "the day of month year"
        dmy = True

        # Prefix could be "Thursday", while Suffix might be "B.C."
        prefix = None
        day = None
        month = None
        year = None
        suffix = None

        # 1.1 Remove dots from token
        token = self.filter_regex.sub("", token).strip()

        # 1.2 Remove "th" from "5th" while preserving "thursday"
        match = self.th_regex.search(token)
        if match:
            token = token[:match.span()[0]] + token[match.span()[1]:]

        # 1.3 Check for a day prefix, eg "Thursday 14 May 2009"
        match = self.day_regex.match(token)
        if match:
            prefix = self.get_prefix(match.group("prefix"))
            token = token[match.span()[1]:].strip()

        # 1.4 Remove "the " if the token starts with it
        if token.lower().startswith("the "):
            token = token[4:]

        def construct_output():
            result_list = []
            result_list.append(prefix)

            # If we want the "the D of M Y" format
            if dmy:
                if day:
                    result_list.append("den")
                    result_list.append(day)
                result_list.append(month)
            else:
                # Otherwise use "M D Y" format
                result_list.append(month)
                result_list.append(day)
            result_list.append(year)
            result_list.append(suffix)
            # Pad non-empty elements of list with spaces
            return " ".join([result for result in result_list if result])

        # 2 Match "DD Month" or "Month DD"
        match = self.md_regex.match(token)
        if not match:
            match = self.text_mdy_regex.match(token)
            # If the second option is matched, we want to use the "M D Y" output format
            if match:
                dmy = False
        if match:
            # Extract the day, month and optionally the suffix from the match
            day = self.ordinal.convert(match.group("day"))
            month = self.get_month(match.group("month"))
            try:
                suffix = " ".join([c for c in match.group("bcsuffix").lower() if c not in (" ", ".")])
            except (IndexError, AttributeError):
                pass
            return construct_output()

        # 3 Match "MM-DD-YY(YY)", "YY(YY)-MM-DD", "DD-Month-YY(YY)", "YY(YY)-Month-DD" or "Month-DD-YY(YY)"
        match = self.dash_date_mdy_regex.match(token) or self.dash_date_ymd_regex.match(token) or self.text_dmy_regex.match(token) or self.text_ymd_regex.match(token) or self.text_mdy_regex.match(token)
        if match:
            # Extract day, month and year from the match
            day, month, year = match.group("day"), match.group("month"), match.group("year")
            
            try:
                # If the format is mm-dd-yyyy, and the "day" > 12, we don't use the dmy output format
                if match.group(0).startswith(month) and int(day) > 12 or prefix and match.group(0).endswith(year) and int(month) <= 12:
                    dmy = False
                
                # Swap the day and month if it's clear that a different format was used
                if int(month) > 12:
                    month, day = day, month
            except ValueError:
                # Get here if month is textual instead of numeric
                pass

            # Convert month, year and day to the correct format
            month, year = self.get_month(month), self.convert_year(year)
            if day:
                day = self.ordinal.convert(day)
            return construct_output()

        # 4 Match "DD Month YYYY", "Month YYYY", "YYYY", "YYYYs" or "Month DD, YYYY"
        match = self.dmy_regex.match(token)
        if not match:
            match = self.mdy_regex.match(token)
            # If the second option is matched, we want to use the "M D Y" output format
            if match:
                dmy = False
        if match:
            # Get and convert day, month, year and optionally suffix. Note that year may be converted using ordinal 
            # conversion if there was a suffix to year, eg: "2000s" -> "two thousands"
            if match.group("day"):
                day = self.ordinal.convert(match.group("day"))
            month = self.get_month(match.group("month"))
            if match.group("suffix"):
                year = self.convert_year(match.group("year"), cardinal=False)
            else:
                year = self.convert_year(match.group("year"))
            try:
                suffix = " ".join([c for c in match.group("bcsuffix").lower() if c not in (" ", ".")])
            except (IndexError, AttributeError):
                pass
            return construct_output()

        return token

    def get_prefix(self, prefix):
        if prefix is None:
            return prefix
        if prefix.lower() in self.trans_day_dict:
            return self.trans_day_dict[prefix.lower()]
        return prefix.lower()

    def convert_year(self, token: str, cardinal:bool = True) -> str:
        # Check for edge case: "00" -> "null null"
        if token == "00":
            return "null null"

        # If the token is of the form "...x00x", then we use cardinal conversion
        # eg 2001 -> "to tusen en"
        if token[-3:-1] == "00":
            
            result = self.cardinal.convert(token)
            # If an ordinal representation is needed, we append 'tallet' for singular years in Norwegian,
            # or adjust appropriately based on Norwegian grammar for specific contexts.
            if not cardinal:
                # In Norwegian, years are often described using the format '[year] tallet' for ordinals.
                result += "tallet"
            return result

        result_list = []
        # Get the value from the third and fourth characters from the right
        if token[-4:-2]:
            result_list.append(self.cardinal.convert(token[-4:-2]))
        # If the last two values are 00, add "hundred" or "hundreds"
        if token[-2:] == "00":
            result_list.append("hundre" if cardinal else "hundrevis")
            return " ".join(result_list)

        # If the second character from the right is a 0, add "null", eg: "nineteen null six",
        # But only if what's before is larger than 10. eg: "201" -> "to hundre en"
        if token[-2:-1] == "0":
            
            if len(token) == 3:
                result_list.append("hundre")
                result_list.append("og")

            else:
                result_list.append("null")

        # Get the text for the right two values
        year_text = self.cardinal.convert(token[-2:])

        # If the value should not simply be a cardinal, replace "y" with "ies", and otherwise add "s". 
        # eg "nineteen thirty" -> "nitten trettiårene"
        if not cardinal:
            # Append 'årene' directly to numeric year text to indicate the plural decade form in Norwegian.
            year_text += "årene" if year_text.isdigit() else "ene"  # Use 'ene' for non-numeric descriptive forms, if applicable.
        result_list.append(year_text)

        return " ".join(result_list)

    def get_month(self, token: str) -> str:
        if not token:
            return token
        if token.lower() in self.trans_month_dict:
            return self.trans_month_dict[token.lower()]
        return token.lower()
