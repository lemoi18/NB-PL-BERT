from singleton_decorator import singleton
import re
from Roman import Roman
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
        self.roman = Roman()
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
            "tjueto": "tjuandre",
            "tjuetre": "tjuetredje",
            "tjuefire": "tjuefjerde",
            "tjuefem": "tjuefemte",
            "tjueseks": "tjuesjette",
            "tjuesju": "tjuesjuende",
            "tjueåtte": "tjueåttende",
            "tjueni": "tjueniende",
            "tretti": "trettiende",
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
        # 1. Filtrer ut kommaer, mellomrom og ordinalindikatorer.
        token = self.filter_regex.sub("", token)

        prefix = ""

        # 2. Sjekk for romertall, og konverter til heltall som streng hvis det er tilfelle.
        if self.cardinal.roman.check_if_roman(token):
            # 3. Hvis det er tilfelle, sett prefiks til "den".
            token = self.cardinal.roman.convert(token)
            prefix = "den"
        else:
            # 4. Hvis ikke, fjern potensielt ordinal-suffiks ("a", "e", "ende", "nde" eller "ste").
            match = self.standard_case_regex.fullmatch(token)
            if match:
                token = match.group(1)

        # 5. Konverter det gjenværende heltallet som streng til kardinaltall, 
        # og erstatt det siste ordet med et ord i ordinal stil.
        number_text_list = self.cardinal.convert(token).split(" ")
        number_text_list[-1] = self.trans_denominator.get(number_text_list[-1], number_text_list[-1])
        result = " ".join(number_text_list)

        # 6. Bruk prefiks hvis nødvendig.
        if prefix:
            result = f"{prefix} {result}"

        return result

