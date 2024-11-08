""" from https://github.com/keithito/tacotron """

'''
Cleaners are transformations that run over the input text at both training and eval time.

Cleaners can be selected by passing a comma-delimited list of cleaner names as the "cleaners"
hyperparameter. Some cleaners are English-specific. You'll typically want to use:
  1. "english_cleaners" for English text
  2. "transliteration_cleaners" for non-English text that can be transliterated to ASCII using
     the Unidecode library (https://pypi.python.org/pypi/Unidecode)
  3. "basic_cleaners" if you do not want to transliterate (in this case, you should also update
     the symbols in symbols.py to match your data).
'''

import re
from unidecode import unidecode
from phonemizer import phonemize


# Regular expression matching whitespace:
_whitespace_re = re.compile(r'\s+')

# List of (regular expression, replacement) pairs for abbreviations:
_abbreviations = [(re.compile('\\b%s\\.' % x[0], re.IGNORECASE), x[1]) for x in [
  ('mrs', 'misess'),
  ('mr', 'mister'),
  ('dr', 'doctor'),
  ('st', 'saint'),
  ('co', 'company'),
  ('jr', 'junior'),
  ('maj', 'major'),
  ('gen', 'general'),
  ('drs', 'doctors'),
  ('rev', 'reverend'),
  ('lt', 'lieutenant'),
  ('hon', 'honorable'),
  ('sgt', 'sergeant'),
  ('capt', 'captain'),
  ('esq', 'esquire'),
  ('ltd', 'limited'),
  ('col', 'colonel'),
  ('ft', 'fort'),
]]


def expand_abbreviations(text):
  for regex, replacement in _abbreviations:
    text = re.sub(regex, replacement, text)
  return text


def expand_numbers(text):
  return normalize_numbers(text)


def lowercase(text):
  return text.lower()


def collapse_whitespace(text):
  return re.sub(_whitespace_re, ' ', text)


def convert_to_ascii(text):
  return unidecode(text)


def basic_cleaners(text):
  '''Basic pipeline that lowercases and collapses whitespace without transliteration.'''
  text = lowercase(text)
  text = collapse_whitespace(text)
  return text


def transliteration_cleaners(text):
  '''Pipeline for non-English text that transliterates to ASCII.'''
  text = re.sub(r'[\u064B-\u065F]', '', text)
  text = convert_to_ascii(text)
  print(f'Ascii content: {text}')
  text = lowercase(text)
  text = collapse_whitespace(text)
  phonemes = phonemize(text, language='ar', backend='espeak', strip=True, preserve_punctuation=False, with_stress=True)
  phonemes = collapse_whitespace(phonemes)
  return phonemes


def english_cleaners(text):
  '''Pipeline for English text, including abbreviation expansion.'''
  text = convert_to_ascii(text)
  text = lowercase(text)
  text = expand_abbreviations(text)
  phonemes = phonemize(text, language='en-us', backend='espeak', strip=True)
  phonemes = collapse_whitespace(phonemes)
  return phonemes


def english_cleaners2(text):
  '''Pipeline for English text, including abbreviation expansion. + punctuation + stress'''
  text = convert_to_ascii(text)
  text = lowercase(text)
  text = expand_abbreviations(text)
  phonemes = phonemize(text, language='en-us', backend='espeak', strip=True, preserve_punctuation=True, with_stress=True)
  phonemes = collapse_whitespace(phonemes)
  return text


def arabic_cleaners(text):
    # Remove diacritics (Harakat)
    text = re.sub(r'[\u064B-\u065F]', '', text)
    
    # Replace Arabic numerals with their corresponding words (optional)
    text = re.sub(r'٠', 'zero', text)
    text = re.sub(r'١', 'one', text)
    text = re.sub(r'٢', 'two', text)
    text = re.sub(r'٣', 'three', text)
    text = re.sub(r'٤', 'four', text)
    text = re.sub(r'٥', 'five', text)
    text = re.sub(r'٦', 'six', text)
    text = re.sub(r'٧', 'seven', text)
    text = re.sub(r'٨', 'eight', text)
    text = re.sub(r'٩', 'nine', text)
    # Add more replacements for other Arabic numerals...
    phonemes = phonemize(text, language='ar', backend='espeak', strip=True, preserve_punctuation=True, with_stress=True)
    return phonemes

