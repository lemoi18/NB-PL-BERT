import pytest
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

@pytest.fixture
def setup_normalization():
    return {
        "cardinal": Cardinal(),
        "digit": Digit(),
        "decimal": Decimal(),
        "date": Date(),
        "address": Address(),
        "verbatim": Verbatim(),
        "measure": Measure(),
        "fraction": Fraction(),
        "telephone": Telephone(),
        "electronic": Electronic(),
        "time": Time(),
        "roman": Roman(),
        "range_converter": Range(),
        "letters": Letters(),
        "legal_symbols": LegalSymbols(),
        "ordinal": Ordinal(),
        "money": Money()
    }

def assertEqualWithColor(actual, expected, message):
    if isinstance(expected, tuple):
        assert actual in expected, f"FAIL: {message} - Expected one of {expected}, got: {actual}"
    else:
        assert actual == expected, f"FAIL: {message} - Expected: {expected}, got: {actual}"
    print(Fore.GREEN + "SUCCESS: " + message + Style.RESET_ALL)

def test_cardinal(setup_normalization):
    cardinal = setup_normalization["cardinal"]
    assertEqualWithColor(cardinal.convert("1", context="hannkjønn"), "en", "Cardinal conversion for '1' in hannkjønn context")
    assertEqualWithColor(cardinal.convert("1", context="nøytrum"), "ett", "Cardinal conversion for '1' in nøytrum context")
    assertEqualWithColor(cardinal.convert("2"), "to", "Cardinal conversion for '2'")
    assertEqualWithColor(cardinal.convert("10"), "ti", "Cardinal conversion for '10'")
    assertEqualWithColor(cardinal.convert("11"), "elleve", "Cardinal conversion for '11'")
    assertEqualWithColor(cardinal.convert("21"), ("tjueen", "enogtyve"), "Cardinal conversion for '21'")
    assertEqualWithColor(cardinal.convert("100"), "ett hundre", "Cardinal conversion for '100'")
    assertEqualWithColor(cardinal.convert("1200"), "en tusen to hundre", "Cardinal conversion for '1200'")
    assertEqualWithColor(cardinal.convert("1500"), "en tusen fem hundre", "Cardinal conversion for '1500'")
    assertEqualWithColor(cardinal.convert("5000000"), "fem millioner", "Cardinal conversion for '5000000'")
    assertEqualWithColor(cardinal.convert("2000000000"), "to milliarder", "Cardinal conversion for '2000000000'")



def test_digit(setup_normalization):
    digit = setup_normalization["digit"]
    assertEqualWithColor(digit.convert("1"), "en", "Digit conversion for '1'")
    assertEqualWithColor(digit.convert("5"), "fem", "Digit conversion for '5'")
    assertEqualWithColor(digit.convert("10"), "en null", "Digit conversion for '10'")
    assertEqualWithColor(digit.convert("123"), "en to tre", "Digit conversion for '123'")
    assertEqualWithColor(digit.convert("456"), "fire fem seks", "Digit conversion for '456'")

def test_decimal(setup_normalization):
    decimal = setup_normalization["decimal"]
    assertEqualWithColor(decimal.convert("3,14"), "tre komma fjorten", "Decimal conversion for '3.14'")
    assertEqualWithColor(decimal.convert("0,5"), "null komma fem", "Decimal conversion for '0.5'")
    assertEqualWithColor(decimal.convert("2,718"), "to komma syv en åtte", "Decimal conversion for '2.718'")
    assertEqualWithColor(decimal.convert("1,618"), "en komma seks en åtte", "Decimal conversion for '1.618'")

def test_date(setup_normalization):
    date = setup_normalization["date"]
    assertEqualWithColor(date.convert("12/03/2021"), ("tolvte mars tjue tjueen", "den tolvte mars tjue tjueen"), "Date conversion for '12/03/2021'")
    assertEqualWithColor(date.convert("01/01/2020"), ("første januar tjuetjue", "den første januar tjue tjue"), "Date conversion for '01/01/2020'")
    assertEqualWithColor(date.convert("25/12/2022"), ("den tjuefemte desember tjue tjueto", "tjuefemte desember to tusen og tjue to"), "Date conversion for '25/12/2022'")
    assertEqualWithColor(date.convert("31/10/1999"), ("den trettiførste oktober nitten nittini", "trettiførste oktober nitten hundre og nitti ni"), "Date conversion for '31/10/1999'")


def test_address(setup_normalization):
    address = setup_normalization["address"]
    assertEqualWithColor(address.convert("Oslo123"), "Oslo en to tre", "Address conversion for 'Oslo123'")
    assertEqualWithColor(address.convert("Bergen45"), "Bergen fire fem", "Address conversion for 'Bergen45'")
    assertEqualWithColor(address.convert("Trondheim678"), "Trondheim seks syv åtte", "Address conversion for 'Trondheim678'")
    assertEqualWithColor(address.convert("Stavanger9"), "Stavanger ni", "Address conversion for 'Stavanger9'")
    assertEqualWithColor(address.convert("Oslo-123"), "Oslo en to tre", "Address conversion for 'Oslo-123'")
    assertEqualWithColor(address.convert("Bergen.45"), "Bergen fire fem", "Address conversion for 'Bergen.45'")

# Verbatim Tests
def test_verbatim(setup_normalization):
    verbatim = setup_normalization["verbatim"]
    assertEqualWithColor(verbatim.convert("&"), "og", "Verbatim conversion for '&'")
    assertEqualWithColor(verbatim.convert("@"), "at", "Verbatim conversion for '@'")
    assertEqualWithColor(verbatim.convert("#"), "hash", "Verbatim conversion for '#'")
    #assertEqualWithColor(verbatim.convert("*"), "stjerne", "Verbatim conversion for '*'")

# Measure Tests
def test_measure(setup_normalization):
    measure = setup_normalization["measure"]
    assertEqualWithColor(measure.convert("5kg"), "fem kilogram", "Measure conversion for '5kg'")
    assertEqualWithColor(measure.convert("100m"), "ett hundre meter", "Measure conversion for '100m'")
    assertEqualWithColor(measure.convert("3L"), "tre liter", "Measure conversion for '3L'")
    assertEqualWithColor(measure.convert("10cm"), "ti centimeter", "Measure conversion for '10cm'")
    assertEqualWithColor(measure.convert("10s"), "ti sekunder", "Measure conversion for '10s'")
    assertEqualWithColor(measure.convert("10cm/s"), "ti centimeter per sekunder", "Measure conversion for '10cm/s'")


def test_fraction(setup_normalization):
    fraction = setup_normalization["fraction"]
    assertEqualWithColor(fraction.convert("1/2"), "en halv", "Fraction conversion for '1/2'")
    assertEqualWithColor(fraction.convert("3/4"), "tre fjerdedeler", "Fraction conversion for '3/4'")
    assertEqualWithColor(fraction.convert("2/3"), "to tredjedeler", "Fraction conversion for '2/3'")
    assertEqualWithColor(fraction.convert("5/12"), "fem tolvtedeler", "Fraction conversion for '5/12'")
    assertEqualWithColor(fraction.convert("1/50"), "en femtidel", "Fraction conversion for '1/50'")
    assertEqualWithColor(fraction.convert("3/72"), "tre syttitodeler", "Fraction conversion for '3/72'")
    assertEqualWithColor(fraction.convert("1/4"), "en fjerdedel", "Fraction conversion for '1/4'")







# Telephone Tests
def test_telephone(setup_normalization):
    telephone = setup_normalization["telephone"]
    assertEqualWithColor(telephone.convert("454 90 073"), "fire fem fire ni null null syv tre", "Telephone conversion for '454 90 073'")
    assertEqualWithColor(telephone.convert("+47 926 51 793"), "pluss fire syv ni to seks fem en syv ni tre", "Telephone conversion for '+47 926 51 793'")
    assertEqualWithColor(telephone.convert("45490073"), "fire fem fire ni null null syv tre", "Telephone conversion for '45490073'")


def test_electronic(setup_normalization):
    electronic = setup_normalization["electronic"]
    assertEqualWithColor(electronic.convert("http://example.com"), "http kolon skråstrek skråstrek e x a m p l e prikk com", "Electronic conversion for 'http://example.com'")
    assertEqualWithColor(electronic.convert("https://example.com"), "https kolon skråstrek skråstrek e x a m p l e prikk com", "Electronic conversion for 'https://example.com'")
    assertEqualWithColor(electronic.convert("#Example"), "hash tag e x a m p l e", "Electronic conversion for '#Example'")
    assertEqualWithColor(electronic.convert("user-name"), "u s e r bindestrek n a m e", "Electronic conversion for 'user-name'")

# Time Tests
def test_time(setup_normalization):
    time = setup_normalization["time"]
    assertEqualWithColor(time.convert("12:30"), "tolv tretti", "Time conversion for '12:30'")
    assertEqualWithColor(time.convert("05:45"), "null fem førtifem", "Time conversion for '05:45'")
    assertEqualWithColor(time.convert("00:00"), "null null null null", "Time conversion for '00:00'")
    assertEqualWithColor(time.convert("23:59"), "tjuetre femtini", "Time conversion for '23:59'")

# Roman Tests
def test_roman(setup_normalization):
    roman = setup_normalization["roman"]
    assertEqualWithColor(roman.convert("IV")[0], "4", "Roman numeral conversion for 'IV'")
    assertEqualWithColor(roman.convert("X")[0], "10", "Roman numeral conversion for 'X'")
    assertEqualWithColor(roman.convert("IX")[0], "9", "Roman numeral conversion for 'IX'")
    assertEqualWithColor(roman.convert("MMXXI")[0], "2021", "Roman numeral conversion for 'MMXXI'")

# Range Tests
def test_range(setup_normalization):
    range_converter = setup_normalization["range_converter"]
    assertEqualWithColor(range_converter.convert("1-10"), "en til ti", "Range conversion for '1-10'")
    assertEqualWithColor(range_converter.convert("5-7"), "fem til syv", "Range conversion for '5-7'")
    assertEqualWithColor(range_converter.convert("0-100"), "null til ett hundre", "Range conversion for '0-100'")
    assertEqualWithColor(range_converter.convert("200-300"), "to hundre til tre hundre", "Range conversion for '200-300'")

# Letters Tests
def test_letters(setup_normalization):
    letters = setup_normalization["letters"]
    assertEqualWithColor(letters.convert("NASA"), "N A S A", "Letters conversion for 'NASA'")
    assertEqualWithColor(letters.convert("abc"), "a b c", "Letters conversion for 'abc'")
    assertEqualWithColor(letters.convert("XYZ"), "X Y Z", "Letters conversion for 'XYZ'")


def test_legal_symbols(setup_normalization):
    assertEqualWithColor(setup_normalization["legal_symbols"].convert("§ 1"), "paragraf en", "Legal symbols conversion for '§ 1'")
    assertEqualWithColor(setup_normalization["legal_symbols"].convert("¶"), "avsnitt", "Legal symbols conversion for '¶'")
    assertEqualWithColor(setup_normalization["legal_symbols"].convert("•"), "punkt", "Legal symbols conversion for '•'")
    assertEqualWithColor(setup_normalization["legal_symbols"].convert("1."), "første punkt", "Legal symbols conversion for '1.'")
    assertEqualWithColor(setup_normalization["legal_symbols"].convert("2."), "andre punkt", "Legal symbols conversion for '2.'")
    assertEqualWithColor(setup_normalization["legal_symbols"].convert("§ 5 - 7"), "paragraf fem til syv", "Legal symbols conversion for '§ 5 - 7'")

def test_ordinal(setup_normalization):
    ordinal = setup_normalization["ordinal"]

    assertEqualWithColor(ordinal.convert("III"), "den tredje", "Ordinal conversion for 'III'")
    assertEqualWithColor(ordinal.convert("IV"), "den fjerde", "Ordinal conversion for 'IV'")
    assertEqualWithColor(ordinal.convert("VII"), "den syvende", "Ordinal conversion for 'VII'")
    assertEqualWithColor(ordinal.convert("XII"), "den tolvte", "Ordinal conversion for 'XII'")
    assertEqualWithColor(ordinal.convert("XXI"), "den tjueførste", "Ordinal conversion for 'XXI'")


def test_money(setup_normalization):
    assertEqualWithColor(setup_normalization["money"].convert("$5"), "fem dollar", "Money conversion for '$5'")
    assertEqualWithColor(setup_normalization["money"].convert("€10"), "ti euro", "Money conversion for '€10'")
    assertEqualWithColor(setup_normalization["money"].convert("£20"), "tjue pund", "Money conversion for '£20'")
    assertEqualWithColor(setup_normalization["money"].convert("kr 100"), "ett hundre kroner", "Money conversion for 'kr 100'")
    assertEqualWithColor(setup_normalization["money"].convert("NOK 750,000"), ("syv hundre femti tusen norske kroner", "sju hundre femti tusen norske kroner"), "Money conversion for 'NOK 750,000'")
    assertEqualWithColor(setup_normalization["money"].convert("12.50 kr"), "tolv kroner og femti øre", "Money conversion for '12.50 kr'")

if __name__ == "__main__":
    pytest.main(["Test_pytest.py"])