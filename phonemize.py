import string
from phonemizer.backend import EspeakBackend
import os
from phonemizer.backend import EspeakBackend

os.environ['PHONEMIZER_ESPEAK_LIBRARY'] = '/home/lemoi18/local/espeak-ng/lib/libespeak-ng.so.1.52.0.1'



from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained('NbAiLab/nb-bert-base')  # You can change this to any other Norwegian tokenizer if needed
import phonemizer

from phonemizer import phonemize
global_phonemizer = phonemizer.backend.EspeakBackend(language='nb', preserve_punctuation=True,  with_stress=True)
from text_normalize import normalize_text, remove_accents



special_mappings = {
    "a": "ɐ",
    "'t": 't',
    "'ve": "v",
    "'m": "m",
    "'re": "ɹ",
    "d": "d",
    'll': "l",
    "n't": "nt",
    "'ll": "l",
    "'d": "d",
    "'": "ʔ",
    "wasn": "wˈɒzən",
    "hasn": "hˈæzn",
    "doesn": "dˈʌzən",
}


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




def phonemize_function(text, lang_fasttext):
    try:

        if lang_fasttext == 'en':
                global_phonemizer = phonemizer.backend.EspeakBackend(language='en', preserve_punctuation=True,  with_stress=True)

                text = normalize_text(remove_accents(text))
        if lang_fasttext == 'no':
        global_phonemizer = phonemizer.backend.EspeakBackend(language='nb', preserve_punctuation=True,  with_stress=True)
        text = normalize_text(remove_accents(text))

            
        words = tokenizer.tokenize(text)
        words = reconstruct_words(words)
        phonemes_bad = [global_phonemizer.phonemize([word], strip=True)[0] if word not in string.punctuation else word for word in words]
        input_ids = []
        phonemes = []
        
        for i in range(len(words)):
            word = words[i]
            phoneme = phonemes_bad[i] if i < len(phonemes_bad) else ""
            
            for k, v in special_mappings.items():
                if word == k:
                    phoneme = v
                    break
            
            if word == "'s":
                if i > 0:
                    if phonemes[i - 1][-1] in ['s', 'ʃ', 'n']:
                        phoneme = "z"
                    else:
                        phoneme = "s"
                        
            if i < len(words) - 1:
                if words[i + 1] == "'t":
                    if word == "haven":
                        phoneme = "hˈævn"
                    if word == "don":
                        phoneme = "dˈəʊn"
            
            if word == "the":
                if i < len(words) - 1:
                    next_phoneme = phonemes_bad[i + 1].replace('ˈ', '').replace('ˌ', '') if i + 1 < len(phonemes_bad) else ""
                    if next_phoneme and next_phoneme[0] in 'ɪiʊuɔɛeəɜoæʌɑaɐ':
                        phoneme = "ðɪ"
                        
            if word == "&": 
                if i > 0 and i < len(words) - 1:
                    phoneme = "ænd"
                    
            if word == "A":
                if i > 0:
                    if words[i - 1] == ".":
                        phoneme = "ɐ"
                        
            if "@" in word and len(word) > 1:
                phonemes.append(word.replace('@', ''))
                input_ids.append(tokenizer.convert_tokens_to_ids(word.replace('@', '')))
                continue
            
           

            input_ids.append(tokenizer.convert_tokens_to_ids([word])[0])
            phonemes.append(phoneme)
            if len(input_ids) != len(phonemes):
                print(f"Length mismatch: input_ids({len(input_ids)}) != phonemes({len(phonemes)})")
        assert len(input_ids) == len(phonemes)
        return {'input_ids' : input_ids, 'phonemes': phonemes}
    except Exception as e:
        print("Error in phonemization")
        print(f"Exception: {e}")
        raise e