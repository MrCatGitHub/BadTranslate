import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import checkLangCode
from googletrans import LANGUAGES
import random
import string

def generateRandomStrings(num, length=2):
    return [''.join(random.choices(string.ascii_lowercase, k=length)) for _ in range(num)]

def removeMatchesFromLanguages(randomList, languages):
    return [item for item in randomList if item not in languages]

randomStrings = generateRandomStrings(10, random.randint(2, 3))

filteredList = removeMatchesFromLanguages(randomStrings, LANGUAGES)
def test_check_valid_language():
    assert checkLangCode((random.choice(list(LANGUAGES)))) == True

def test_check_invalid_language():
    assert checkLangCode((random.choice(list(filteredList)))) == False
