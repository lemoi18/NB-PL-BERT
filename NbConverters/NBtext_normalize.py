import pandas as pd

from nltk.tokenize import TweetTokenizer
from nltk.tokenize.treebank import TreebankWordDetokenizer
import unicodedata

import os, sys
import re

import pandas as pd

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.dirname(__file__))

from nltk.tokenize import TweetTokenizer
from nltk.tokenize.treebank import TreebankWordDetokenizer
from NbConverters.Punct import Punct
from NbConverters.Date import Date

from NbConverters.Letters    import Letters
from NbConverters.Cardinal   import Cardinal
from NbConverters.Verbatim   import Verbatim
from NbConverters.Decimal    import Decimal
from NbConverters.Measure    import Measure
from NbConverters.Money      import Money
from NbConverters.Ordinal    import Ordinal
from NbConverters.Time       import Time
from NbConverters.Electronic import Electronic
from NbConverters.Digit      import Digit
from NbConverters.Fraction   import Fraction
from NbConverters.Telephone  import Telephone
from NbConverters.Address    import Address
from NbConverters.Roman    import Roman
from NbConverters.Range    import Range
from NbConverters.LegalSymbols    import LegalSymbols


import sys


from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained('NbAiLab/nb-bert-base')
months = ['jan',
 'feb',
 'mar',
 'apr',
 'jun',
 'jul',
 'aug',
 'sep',
 'okt',
 'nov',
 'decs',
 'januar',
 'februar',
 'mars',
 'april',
 'juni',
 'juli',
 'august',
 'september',
 'oktober',
 'november',
 'desember']

labels = {
    "PUNCT": Punct(),
    "DATE": Date(),
    "LETTERS": Letters(),
    "CARDINAL": Cardinal(),
    "VERBATIM": Verbatim(),
    "DECIMAL": Decimal(),
    "MEASURE": Measure(),
    "MONEY": Money(),
    "ORDINAL": Ordinal(),
    "TIME": Time(),
    "ELECTRONIC": Electronic(),
    "DIGIT": Digit(),
    "FRACTION": Fraction(),
    "TELEPHONE": Telephone(),
    "ADDRESS": Address(),
    "ROMAN": Roman(),
    "RANGE": Range(),
    "LEGALSYMBOLS": LegalSymbols()
}

def split_given_size(a, size):
    return np.split(a, np.arange(size,len(a),size))

word_tokenize = tokenizer.tokenize
#word_tokenize = TweetTokenizer().tokenize
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
def normalize_split(text):
    words = word_tokenize(text)
    words = reconstruct_words(words)
    chunks = split_given_size(words, 500)
    
    normalized_text = ""
    for words in chunks:
        sentence = tokenizer.convert_tokens_to_string(words)
        normalized_text += normalizer.normalize(sentence) + " "
        #sentence = TreebankWordDetokenizer().detokenize(words)
        #normalized_text += normalizer.normalize(sentence) + " "
    
    return normalized_text

def reconstruct_words(tokens):
    words = []
    current_word = ""
    for token in tokens:
        if token.startswith("##"):
            current_word += token[2:]
        else:
            if current_word:
                words.append(current_word)
            current_word = token
    if current_word:
        words.append(current_word)
    return words

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def is_oridinal(inputString):
    return inputString.endswith(("th", "nd", "st", "rd"))

def is_money(inputString):
    return inputString.startswith(('$', '€', '£', '¥', 'kr'))


def is_legal(inputString):
    return inputString.startswith(('§', '¶', '•'))

def is_time(inputString):
    return ":" in inputString

def is_cardinal(inputString):
    return "," in inputString or len(inputString) <= 3

def is_fraction(inputString):
    return "/" in inputString

def is_decimal(inputString):
    return "." in inputString

def is_range(inputString) : 
    return "-" in inputString

def is_url(inputString):
    return "//" in inputString or ".com" in inputString or ".html" in inputString

def has_month(inputString):
    return inputString.lower() in months or inputString == "May"

# Define normalization functions
def normalize_single(text, prev_text="", next_text=""):
    if is_url(text):
        text = labels['ELECTRONIC'].convert(text).upper()
    elif is_legal(text):
        text = labels['LEGALSYMBOLS'].convert(text)
    elif has_numbers(text):
        if has_month(prev_text):
            prev_text = labels['DATE'].get_month(prev_text.lower())
            text = labels['DATE'].convert(prev_text + " " + text).replace(prev_text, "").strip()
        elif has_month(next_text):
            next_text = labels['DATE'].get_month(next_text.lower())
            text = labels['DATE'].convert(text + " " + next_text).replace(next_text, "").strip()
        elif is_oridinal(text):
            text = labels['ORDINAL'].convert(text)
        elif is_time(text):
            text = labels['TIME'].convert(text)
        elif is_money(text):
            text = labels['MONEY'].convert(text)
        elif is_fraction(text):
            text = labels['FRACTION'].convert(text)
        elif is_decimal(text):
            text = labels['DECIMAL'].convert(text)
        elif is_cardinal(text):
            text = labels['CARDINAL'].convert(text)
        elif is_range(text):
            text = labels['RANGE'].convert(text)
        else:
            text = labels['DATE'].convert(text)
            print("text from date", text)

        if has_numbers(text):
            text = labels['CARDINAL'].convert(text)
    elif text == "#" and has_numbers(next_text):
        text = "number"

    return text.replace("$", "")



def normalize_text(text):
    text = remove_accents(text).replace('–', ' to ').replace('-', ' - ')
    words = word_tokenize(text)
    words = reconstruct_words(words)

    df = pd.DataFrame(words, columns=['before'])
    df['after'] = df['before']
    df['previous'] = df.before.shift(1).fillna('') + "|" + df.before + "|" + df.before.shift(-1).fillna('')

    df['after'] = df['previous'].apply(lambda m: normalize_single(m.split('|')[1], m.split('|')[0], m.split('|')[2]))

    return tokenizer.convert_tokens_to_string(df['after'].tolist()).replace("’ s", "'s").replace(" 's", "'s")

if __name__ == '__main__' : 
    text = 'Hei (23 Jan 2020, 12:10) § 1'
    out = normalize_text(text)
    print(out)

