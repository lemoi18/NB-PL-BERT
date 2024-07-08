from singleton_decorator import singleton
import re
from Decimal import Decimal
from Fraction import Fraction

@singleton
class Measure:
    """
    Converts measurements to their full Norwegian text representation.
    """
    def __init__(self):
        super().__init__()
        # Regex to detect fractions
        self.fraction_regex = re.compile(r"(((?:-?\d* )?-?\d+ *\/ *-? *\d+)|(-?\d* *(?:½|⅓|⅔|¼|¾|⅕|⅖|⅗|⅘|⅙|⅚|⅐|⅛|⅜|⅝|⅞|⅑|⅒)))")
        # Regex to detect values (integers and decimals)
        self.value_regex = re.compile(r"(-?(?:\d*\.)?\d+)")
        # Regex filter to remove commas
        self.filter_regex = re.compile(r",")
        # Dictionary for recognized units and their translations
        self.unit_dict = {
            "kg": {"singular": "kilogram", "plural": "kilogram"},
            "m": {"singular": "meter", "plural": "meter"},
            "L": {"singular": "liter", "plural": "liter"},
            "cm": {"singular": "centimeter", "plural": "centimeter"},
            "g": {"singular": "gram", "plural": "gram"},
            "mm": {"singular": "millimeter", "plural": "millimeter"},
            "km": {"singular": "kilometer", "plural": "kilometer"},
            # Add more units as needed
        }
        
        # Initialize Decimal and Fraction classes
        self.decimal = Decimal()
        self.fraction = Fraction()

    def convert(self, token: str) -> str:
        # 1 Filter out commas
        token = self.filter_regex.sub("", token)

        # Variable to store the value of the input
        numeric_value = ""
        value = ""
        measure = ""

        # 2 Try to match a fraction
        match = self.fraction_regex.match(token)
        if match:
            numeric_value = match.group(0)
            value = self.fraction.convert(numeric_value)
            measure = token[match.span()[1]:].strip()
        else:
            # 3 Try to match x.y or x
            match = self.value_regex.match(token)
            if match:
                numeric_value = match.group(0)
                value = self.decimal.convert(numeric_value)
                measure = token[match.span()[1]:].strip()

        # List to store measure chunks
        measure_chunks = []
        if measure:
            # 4 Iterate over chunks of the remainder, the actual measure
            for chunk in re.split(r"\s+", measure):
                chunk_trans = self.unit_dict.get(chunk, None)
                if chunk_trans:
                    # 4.1 Match with a dictionary while preserving case sensitivity
                    chunk_trans = chunk_trans["singular" if float(numeric_value.replace(",", ".")) == 1 else "plural"]
                else:
                    # 4.2 Otherwise, match with a dictionary while ignoring case sensitivity
                    chunk_trans = chunk
                measure_chunks.append(chunk_trans)

        # Join the value and measure
        result = f"{value} {' '.join(measure_chunks)}"
        return result.strip()

# Measure Tests
def test_measure(setup_normalization):
    measure = setup_normalization["measure"]
    assertEqualWithColor(measure.convert("5kg"), "fem kilogram", "Measure conversion for '5kg'")
    assertEqualWithColor(measure.convert("100m"), "ett hundre meter", "Measure conversion for '100m'")
    assertEqualWithColor(measure.convert("3L"), "tre liter", "Measure conversion for '3L'")
    assertEqualWithColor(measure.convert("10cm"), "ti centimeter", "Measure conversion for '10cm'")
