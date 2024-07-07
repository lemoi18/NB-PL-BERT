from singleton_decorator import singleton
import re
from Roman import Roman
from Cardinal import Cardinal

@singleton
class Ordinal:
    """
    Steg:
    1. Filtrer ut kommaer, mellomrom og ordinalindikatorer.
    2. Sjekk for romertall, og konverter til heltall som streng hvis det er tilfelle.
    3. Hvis det er tilfelle, sett prefiks til "den".
    4. Hvis ikke, fjern potensielt ordinal-suffiks ("a", "e", "ende", "nde" eller "ste").
    5. Konverter det gjenværende heltallet som streng til kardinaltall, og erstatt det siste ordet med et ord i ordinal stil.
    6. Bruk prefiks hvis nødvendig.
    
    Kanttilfeller:
    II -> (noen ganger) andre
    II -> (noen ganger) den andre
    
    Merk:
    Verdiene er alltid:
    - Romertall (inkludert prikker)
    - Tall (potensielt med kommaer og/eller mellomrom)
    - Potensielt suffiksert med disse: "a", "e", "ende", "nde" eller "ste".
    - Tall + ª eller º (Ordinalindikatorer)
    
    Uteblitte tilfeller:
    - Når innholdet ikke er av de nevnte formene
    - Forskjellen mellom kanttilfelle 1 og kanttilfelle 2. Prefikset "den" er alltid foran når det er et romertall.
    """
    def __init__(self):
        super().__init__()
        # Regex to filter out commas, spaces, and ordinal indicators
        self.filter_regex = re.compile(r"[, ºª]")
        # Regex to detect the standard cases
        self.standard_case_regex = re.compile(r"(?i)(\d+)(a|e|ende|nde|ste)?")
        # Roman conversion and detection of roman numeral cases
        self.roman = Roman()
        # Cardinal conversion
        self.cardinal = Cardinal()

        # Translation from Cardinal style to Ordinal style
        self.trans_denominator = {
            "null": "nullte",
            "en": "første",
            "to": "andre",
            "tre": "tredje",
            "fire": "fjerde",
            "fem": "femte",
            "seks": "sjette",
            "sju": "sjuende",
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
        if self.roman.check_if_roman(token):
            # 3. Hvis det er tilfelle, sett prefiks til "den".
            token = self.roman.convert(token)
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
