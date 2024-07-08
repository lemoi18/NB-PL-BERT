from singleton_decorator import singleton
import re
from Cardinal import Cardinal
from Digit import Digit

@singleton
class Electronic:
    """
    Steps (data):
    - 1 Convert token to lowercase
    - 2 Handle edge case with just ::
    - 3 Handle "#Text" -> "hash tag text" edge case
    - 4 Iterate over token
      - 4.1 If the token starts with "http(s)://", and ".com" is encountered, add "dot com"
      - 4.2 Use digit or cardinal conversion to convert numbers
      - 4.3 Or add non-numeric characters using the right translation directory, 
            depending on whether the token starts with "http(s)://"

    Edge case:
    "::" -> "::"
    rather than "kolon kolon"
    "#Text" -> "hash tag text"
    """
    def __init__(self):
        super().__init__()
        # Translation dict for URL sections
        self.data_https_dict = {
            "/": "skråstrek",
            ":": "kolon",
            ".": "prikk",
            "#": "hash",
            "-": "bindestrek",

            "é": "e akutt",

            "(": "åpne parentes",
            ")": "lukk parentes",
            "_": "understrek",
            ",": "komma",
            "%": "prosent",
            "~": "tilde",
            ";": "semikolon",
            "'": "enkelt anførselstegn",
            "\"": "dobbel anførselstegn",

            "0": "null",
            "1": "en",
            "2": "to",
            "3": "tre",
            "4": "fire",
            "5": "fem",
            "6": "seks",
            "7": "syv",
            "8": "åtte",
            "9": "ni",
        }

        # Translation dict for sensible conversion
        self.sensible_trans_dict = {
            "/": "skråstrek",
            ":": "kolon",
            ".": "prikk",
            "#": "hash",
            "-": "bindestrek",
            "é": "e akutt",
            "(": "åpne parentes",
            ")": "lukk parentes",
            "_": "understrek",
            ",": "komma",
            "%": "prosent",
            "~": "tilde",
            ";": "semikolon",
            "'": "enkelt anførselstegn",
            "\"": "dobbel anførselstegn",
            "=" : "er lik",

            "0": "null",
            "1": "en",
            "2": "to",
            "3": "tre",
            "4": "fire",
            "5": "fem",
            "6": "seks",
            "7": "syv",
            "8": "åtte",
            "9": "ni",
        }

        # Regex to test for "https?://"
        self.data_http_regex = re.compile(r"https?://")
        
        # Cardinal and digit conversion
        self.cardinal = Cardinal()
        self.digit = Digit()

    def convert(self, token: str) -> str:
        # 1 Convert to lowercase
        token = token.lower()

        # 2 Check for edge case with just ::
        if token == "::":
            return token

        # 3 Check for #Text -> "hash tag text"
        if token[0] == "#" and len(token) > 1:
            return self.convert_hash_tag(token)

        # Variable stating whether token starts with http(s)://
        http = self.data_http_regex.match(token) is not None
        # Get the translation dict to use for this token
        data_trans_dict = self.data_https_dict if http else self.sensible_trans_dict
        
        result_list = []
        c_index = 0

        while c_index < len(token):
            if http and token[c_index:].startswith("http://"):
                result_list.append("http kolon skråstrek skråstrek")
                c_index += len("http://")
                continue
            elif http and token[c_index:].startswith("https://"):
                result_list.append("https kolon skråstrek skråstrek")
                c_index += len("https://")
                continue
            elif token[c_index:].startswith(".com"):
                result_list.append("prikk com")
                c_index += len(".com")
                continue

            # Handle digits
            if token[c_index].isdigit():
                digits = []
                while c_index < len(token) and token[c_index].isdigit():
                    digits.append(token[c_index])
                    c_index += 1
                if len(digits) == 2:
                    text = self.cardinal.convert("".join(digits))
                else:
                    text = self.digit.convert("".join(digits))
                result_list.append(text)
                continue

            # Handle special characters
            char = token[c_index]
            if char in data_trans_dict:
                result_list.append(data_trans_dict[char])
            else:
                result_list.append(char)

            c_index += 1

        return " ".join(result_list)
    
    def convert_hash_tag(self, token: str) -> str:
        # Parse the hash tag message
        out = ["hash tag"]
        for char in token[1:].lower():
            if char in self.sensible_trans_dict:
                out.append(self.sensible_trans_dict[char])
            else:
                out.append(char)
        return " ".join(out).strip()