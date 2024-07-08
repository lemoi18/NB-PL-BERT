from singleton_decorator import singleton
import re
from Cardinal import Cardinal
from Ordinal import Ordinal

@singleton
class Date:
    """
    Converts dates to their Norwegian textual representations.
    """
    def __init__(self):
        super().__init__()
        self.filter_regex = re.compile(r"[,']")
        self.day_regex = re.compile(r"^(?P<prefix>monday|tuesday|wednesday|thursday|friday|saturday|sunday|mon|tue|wed|thu|fri|sat|sun)\.?", flags=re.I)
        self.dash_date_ymd_regex = re.compile(r"^(?P<year>\d{2,5}) *(?:-|\.|/) *(?P<month>\d{1,2}) *(?:-|\.|/) *(?P<day>\d{1,2})$", flags=re.I)
        self.dash_date_dmy_regex = re.compile(r"^(?P<day>\d{1,2}) *(?:-|\.|/) *(?P<month>\d{1,2}) *(?:-|\.|/) *(?P<year>\d{2,5})$", flags=re.I)
        self.text_ymd_regex = re.compile(r"^(?P<year>\d{2,5}) *(?:-|\.|/) *(?P<month>januar|februar|mars|april|mai|juni|juli|august|september|oktober|november|desember|sept|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec) *(?:-|\.|/) *(?P<day>\d{1,2})$", flags=re.I)
        self.text_dmy_regex = re.compile(r"^(?P<day>\d{1,2}) *(?:-|\.|/) *(?P<month>januar|februar|mars|april|mai|juni|juli|august|september|oktober|november|desember|sept|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec) *(?:-|\.|/) *(?P<year>\d{2,5})$", flags=re.I)
        self.dmy_regex = re.compile(r"^(?:(?:(?P<day>\d{1,2}) +(of +)?)?(?P<month>januar|februar|mars|april|mai|juni|juli|august|september|oktober|november|desember|sept|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\.? +)?(?P<year>\d{1,5})(?P<suffix>s?)\/?(?: *(?P<bcsuffix>[A-Z\.]+)?)$", flags=re.I)
        self.md_regex = re.compile(r"^(?P<month>januar|februar|mars|april|mai|juni|juli|august|september|oktober|november|desember|sept|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\.? +(?P<day>\d{1,2})(?: *(?P<bcsuffix>[A-Z\.]+)?)$", flags=re.I)
        self.th_regex = re.compile(r"(?:(?<=\d)|(?<=\d ))(?:th|nd|rd|st)", flags=re.I)

        self.trans_month_dict = {
            "jan": "januar", "feb": "februar", "mar": "mars", "apr": "april", "may": "mai", "jun": "juni",
            "jul": "juli", "aug": "august", "sep": "september", "oct": "oktober", "nov": "november", "dec": "desember",
            "sept": "september", "01": "januar", "02": "februar", "03": "mars", "04": "april", "05": "mai",
            "06": "juni", "07": "juli", "08": "august", "09": "september", "10": "oktober", "11": "november", "12": "desember",
            "1": "januar", "2": "februar", "3": "mars", "4": "april", "5": "mai", "6": "juni", "7": "juli", "8": "august", "9": "september"
        }

        self.trans_day_dict = {
            "man": "mandag", "tir": "tirsdag", "ons": "onsdag", "tor": "torsdag",
            "fre": "fredag", "lør": "lørdag", "søn": "søndag"
        }

        self.cardinal = Cardinal()
        self.ordinal = Ordinal()
    
    def convert(self, token: str) -> str:
        dmy = True
        prefix, day, month, year, suffix = None, None, None, None, None

        token = self.filter_regex.sub("", token).strip()
        match = self.th_regex.search(token)
        if match:
            token = token[:match.span()[0]] + token[match.span()[1]:]
        match = self.day_regex.match(token)
        if match:
            prefix = self.get_prefix(match.group("prefix"))
            token = token[match.span()[1]:].strip()
        if token.lower().startswith("the "):
            token = token[4:]

        def construct_output():
            result_list = [prefix]
            if dmy:
                if day:
                    result_list.append("den")
                    result_list.append(day)
                result_list.append(month)
            else:
                result_list.append(month)
                result_list.append(day)
            result_list.append(year)
            result_list.append(suffix)
            return " ".join([result for result in result_list if result])

        match = self.md_regex.match(token)
        if not match:
            match = self.text_dmy_regex.match(token)
        if match:
            day = self.ordinal.convert(match.group("day"))
            month = self.get_month(match.group("month"))
            try:
                suffix = " ".join([c for c in match.group("bcsuffix").lower() if c not in (" ", ".")])
            except (IndexError, AttributeError):
                pass
            return construct_output()

        match = self.dash_date_dmy_regex.match(token) or self.dash_date_ymd_regex.match(token) or self.text_dmy_regex.match(token) or self.text_ymd_regex.match(token)
        if match:
            day, month, year = match.group("day"), match.group("month"), match.group("year")
            try:
                if int(month) > 12:
                    month, day = day, month
            except ValueError:
                pass
            month, year = self.get_month(month), self.convert_year(year)
            if day:
                day = self.ordinal.convert(day)
            return construct_output()

        match = self.dmy_regex.match(token)
        if match:
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

    def convert_year(self, token: str, cardinal: bool = True) -> str:
        if token == "00":
            return "null null"
        if token[-3:-1] == "00":
            result = self.cardinal.convert(token)
            if not cardinal:
                result += "tallet"
            return result

        result_list = []
        if token[-4:-2]:
            result_list.append(self.cardinal.convert(token[-4:-2]))
        if token[-2:] == "00":
            result_list.append("hundre" if cardinal else "hundrevis")
            return " ".join(result_list)
        if token[-2:-1] == "0":
            if len(token) == 3:
                result_list.append("hundre")
                result_list.append("og")
            else:
                result_list.append("null")

        year_text = self.cardinal.convert(token[-2:])
        if not cardinal:
            year_text += "årene" if year_text.isdigit() else "ene"
        result_list.append(year_text)

        return " ".join(result_list)

    def get_month(self, token: str) -> str:
        if not token:
            return token
        if token.lower() in self.trans_month_dict:
            return self.trans_month_dict[token.lower()]
        return token.lower()
