import unittest
from colorama import Fore, Style, init

from Cardinal import Cardinal
from Digit import Digit
from Decimal import Decimal
from Date import Date
from Address import Address
from Verbatim import Verbatim
from Measure import Measure
from Fraction import Fraction
from Telephone import Telephone
from Electronic import Electronic
from Time import Time
from Roman import Roman
from Range import Range
from Letters import Letters
from LegalSymbols import LegalSymbols
from Ordinal import Ordinal
from Money import Money

init(autoreset=True)

class TestNormalization(unittest.TestCase):
    def setUp(self):
        self.cardinal = Cardinal()
        self.digit = Digit()
        self.decimal = Decimal()
        self.date = Date()
        self.address = Address()
        self.verbatim = Verbatim()
        self.measure = Measure()
        self.fraction = Fraction()
        self.telephone = Telephone()
        self.electronic = Electronic()
        self.time = Time()
        self.roman = Roman()
        self.range_converter = Range()
        self.letters = Letters()
        self.legal_symbols = LegalSymbols()
        self.ordinal = Ordinal()
        self.money = Money()
    def assertEqualWithColor(self, actual, expected, message):
        try:
            self.assertEqual(actual, expected)
            print(Fore.GREEN + "SUCCESS: " + message + Style.RESET_ALL)
        except AssertionError:
            print(Fore.RED + "FAIL: " + message + Style.RESET_ALL)
            print(Fore.YELLOW + f"Expected: {expected}, got: {actual}" + Style.RESET_ALL)
            print("----------------------------------------------------------------------")



    # Cardinal Tests
    def test_cardinal_single_digit(self):
        self.assertEqualWithColor(self.cardinal.convert("1"), "en", "Cardinal conversion for '1'")
        self.assertEqualWithColor(self.cardinal.convert("2"), "to", "Cardinal conversion for '2'")

    def test_cardinal_multiple_digits(self):
        self.assertEqualWithColor(self.cardinal.convert("10"), "ti", "Cardinal conversion for '10'")
        self.assertEqualWithColor(self.cardinal.convert("11"), "elleve", "Cardinal conversion for '11'")
        self.assertEqualWithColor(self.cardinal.convert("21"), "tjueen", "Cardinal conversion for '21'")

    def test_digit_single_digit(self):
        self.assertEqualWithColor(self.digit.convert("1"), "en", "Digit conversion for '1'")
        self.assertEqualWithColor(self.digit.convert("5"), "fem", "Digit conversion for '5'")

    def test_digit_multiple_digits(self):
        self.assertEqualWithColor(self.digit.convert("10"), "en null", "Digit conversion for '10'")
        self.assertEqualWithColor(self.digit.convert("123"), "en to tre", "Digit conversion for '123'")

    def test_decimal(self):
        self.assertEqualWithColor(self.decimal.convert("3.14"), "tre komma fjorten", "Decimal conversion for '3.14'")
        self.assertEqualWithColor(self.decimal.convert("0.5"), "null komma fem", "Decimal conversion for '0.5'")

    def test_date(self):
        self.assertEqualWithColor(self.date.convert("12/03/2021"), "tolvte mars tjue tjuen", "Date conversion for '12/03/2021'")
        self.assertEqualWithColor(self.date.convert("01/01/2020"), "første januar tjuetjue", "Date conversion for '01/01/2020'")

    # Address Tests
    def test_address(self):
        self.assertEqualWithColor(self.address.convert("Oslo123"), "Oslo en to tre", "Address conversion for 'Oslo123'")
        self.assertEqualWithColor(self.address.convert("123B"), "en to tre B", "Address conversion for '123B'")

    # Verbatim Tests
    def test_verbatim(self):
        self.assertEqualWithColor(self.verbatim.convert("&"), "og", "Verbatim conversion for '&'")
        self.assertEqualWithColor(self.verbatim.convert("@"), "at", "Verbatim conversion for '@'")

    # Measure Tests
    def test_measure(self):
        self.assertEqualWithColor(self.measure.convert("5kg"), "fem kilo", "Measure conversion for '5kg'")
        self.assertEqualWithColor(self.measure.convert("100m"), "hundre meter", "Measure conversion for '100m'")

    # Fraction Tests
    def test_fraction(self):
        self.assertEqualWithColor(self.fraction.convert("1/2"), "en halv", "Fraction conversion for '1/2'")
        self.assertEqualWithColor(self.fraction.convert("3/4"), "tre firedeler", "Fraction conversion for '3/4'")

    # Telephone Tests
    def test_telephone(self):
        self.assertEqualWithColor(self.telephone.convert("123-4567"), "en to tre fire fem seks sju", "Telephone conversion for '123-4567'")
        self.assertEqualWithColor(self.telephone.convert("555-1234"), "fem fem fem en to tre fire", "Telephone conversion for '555-1234'")

    # Electronic Tests
    def test_electronic(self):
        self.assertEqualWithColor(self.electronic.convert("http://example.com"), "h t t p : / / e x a m p l e . c o m", "Electronic conversion for 'http://example.com'")
        self.assertEqualWithColor(self.electronic.convert("#hashtag"), "hash tag h a s h t a g", "Electronic conversion for '#hashtag'")

    # Time Tests
    def test_time(self):
        self.assertEqualWithColor(self.time.convert("12:30"), "tolv tretti", "Time conversion for '12:30'")
        self.assertEqualWithColor(self.time.convert("5:45"), "fem førtifem", "Time conversion for '5:45'")

    # Roman Tests
    def test_roman(self):
        self.assertEqualWithColor(self.roman.convert("IV")[0], "4", "Roman numeral conversion for 'IV'")
        self.assertEqualWithColor(self.roman.convert("X")[0], "10", "Roman numeral conversion for 'X'")

    # Range Tests
    def test_range(self):
        self.assertEqualWithColor(self.range_converter.convert("1-10"), "en til ti", "Range conversion for '1-10'")
        self.assertEqualWithColor(self.range_converter.convert("5-7"), "fem til sju", "Range conversion for '5-7'")

    # Letters Tests
    def test_letters(self):
        self.assertEqualWithColor(self.letters.convert("NASA"), "N A S A", "Letters conversion for 'NASA'")
        self.assertEqualWithColor(self.letters.convert("abc"), "a b c", "Letters conversion for 'abc'")

    # LegalSymbols Tests
    def test_legal_symbols(self):
        self.assertEqualWithColor(self.legal_symbols.convert("§ 1"), "paragraf en", "Legal symbols conversion for '§ 1'")
        self.assertEqualWithColor(self.legal_symbols.convert("¶"), "avsnitt", "Legal symbols conversion for '¶'")
        self.assertEqualWithColor(self.legal_symbols.convert("•"), "punkt", "Legal symbols conversion for '•'")
        self.assertEqualWithColor(self.legal_symbols.convert("1."), "første punkt", "Legal symbols conversion for '1.'")
        self.assertEqualWithColor(self.legal_symbols.convert("2."), "andre punkt", "Legal symbols conversion for '2.'")
        self.assertEqualWithColor(self.legal_symbols.convert("§ 5 - 7"), "paragraf fem til paragraf sju", "Legal symbols conversion for '§ 5 - 7'")

    # Ordinal Tests
    def test_ordinal(self):
        self.assertEqualWithColor(self.ordinal.convert("1st"), "første", "Ordinal conversion for '1st'")
        self.assertEqualWithColor(self.ordinal.convert("2nd"), "andre", "Ordinal conversion for '2nd'")
        self.assertEqualWithColor(self.ordinal.convert("III"), "den tredje", "Ordinal conversion for 'III'")
        self.assertEqualWithColor(self.ordinal.convert("4th"), "fjerde", "Ordinal conversion for '4th'")

    # Money Tests
    def test_money(self):
        self.assertEqualWithColor(self.money.convert("$5"), "fem dollar", "Money conversion for '$5'")
        self.assertEqualWithColor(self.money.convert("€10"), "ti euro", "Money conversion for '€10'")
        self.assertEqualWithColor(self.money.convert("£20"), "tjue pund", "Money conversion for '£20'")
        self.assertEqualWithColor(self.money.convert("kr 100"), "hundre kroner", "Money conversion for 'kr 100'")
        self.assertEqualWithColor(self.money.convert("NOK 750,000"), "sju hundre femti tusen norske kroner", "Money conversion for 'NOK 750,000'")
        self.assertEqualWithColor(self.money.convert("12.50 kr"), "tolv kroner og femti øre", "Money conversion for '12.50 kr'")

if __name__ == "__main__":
    unittest.main()
