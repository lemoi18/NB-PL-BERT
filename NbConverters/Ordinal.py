from singleton_decorator import singleton
import re
from Cardinal import Cardinal

@singleton
class Ordinal:
    """
    Handles the conversion of ordinal numbers to their textual representation in Norwegian.
    """
    def __init__(self):
        super().__init__()
        self.filter_regex = re.compile(r"[, ºª]")
        self.standard_case_regex = re.compile(r"(?i)(\d+)(a|e|ende|nde|ste)?")
        self.cardinal = Cardinal()
        self.trans_denominator = {
            "null": "nullte",
            "en": "første",
            "ett": "første",
            "to": "andre",
            "tre": "tredje",
            "fire": "fjerde",
            "fem": "femte",
            "seks": "sjette",
            "syv": "syvende",
            "åtte": "åttende",
            "ni": "niende",
            "ti": "tiende",
            "elleve": "ellevte",
            "tolv": "tolvte",
            "tretten": "trettende",
            "fjorten": "fjortende",
            "femten": "femtende",
            "seksten": "sekstende",
            "sytten": "syttende",
            "atten": "attende",
            "nitten": "nittende",
            "tjue": "tjuende",
            "tjueen": "tjueførste",
            "tjueett": "tjueførste",
            "tjueto": "tjueandre",
            "tjuetre": "tjuetredje",
            "tjuefire": "tjuefjerde",
            "tjuefem": "tjuefemte",
            "tjueseks": "tjuesjette",
            "tjuesju": "tjuesjuende",
            "tjueåtte": "tjueåttende",
            "tjueni": "tjueniende",
            "tretti": "trettiende",
            "trettien": "trettiførste",
            "førti": "førtiende",
            "femti": "femtiende",
            "seksti": "sekstiende",
            "sytti": "syttiende",
            "åtti": "åttiende",
            "nitti": "nittiende",
            "hundre": "hundrede",
            "tusen": "tusende",
            "million": "millionte",
            "milliard": "milliardte",
            "billion": "billionte",
        }
    
    def convert(self, token: str) -> str:
        token = self.filter_regex.sub("", token)
        match = self.standard_case_regex.fullmatch(token)
        if match:
            token = match.group(1)
        number_text_list = self.cardinal.convert(token).split(" ")
        number_text_list[-1] = self.trans_denominator.get(number_text_list[-1], number_text_list[-1])
        return " ".join(number_text_list)

