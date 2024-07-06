from singleton_decorator import singleton
import re

@singleton
class Verbatim:
    """
    Steps:
    - 1 Translate specific symbols and letters
    - 2 Remove unwanted characters

    Edge cases:
    """
    def __init__(self):
        super().__init__()
        # Translation dict for special symbols and Greek letters
        self.trans_dict = {
            "@": "at",
            "#": "hash",
            "&": "og",
            "%": "prosent",
            "$": "dollar",
            "€": "euro",
            "£": "pund",
            "¥": "yen",
            "₩": "won",
            "©": "copyright",
            "®": "registrert",
            "™": "trademark",
            "+": "pluss",
            "=": "lik",
            "<": "mindre enn",
            ">": "større enn",
            "±": "pluss minus",
            "µ": "mikro",
            "π": "pi",
            "√": "kvadratrot",
            "∞": "uendelig",
            "∑": "sum",
            "∏": "produkt",
            "Δ": "delta",
            "λ": "lambda",
            "Ω": "omega",
            "α": "alfa",
            "β": "beta",
            "γ": "gamma",
            "θ": "theta",
            "δ": "delta",
            "φ": "fi",
            "ψ": "psi",
            "ω": "omega",
            " ": " ",
            "\n": " ",
            "\t": " ",
            "\r": " ",
        }
        # Regex to find special symbols
        self.special_symbol_regex = re.compile(r"[@#&%$€£¥₩©®™+=<>±µπ√∞∑∏ΔλΩαβγθδφψω\n\t\r]")

    def convert(self, token: str) -> str:
        # 1 Translate specific symbols and letters
        token = self.special_symbol_regex.sub(lambda m: self.trans_dict.get(m.group(0), m.group(0)), token)
        # 2 Remove unwanted characters
        return re.sub(r"[^\w\s]", "", token)
