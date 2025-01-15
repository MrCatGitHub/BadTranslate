import re
from shutil import get_archive_formats
from packaging.version import Version, InvalidVersion
import random
import time
from cv2 import checkRange
import requests
from googletrans import Translator, LANGUAGES
from tkinter import Tk
import asyncio

ver = "0.0.3-alpha.1"
def unknownErr():
    print("Error 004: An unknown error ocurred")
url = "https://github.com/MrCatGitHub/BadTranslate/releases/latest"
try:
    response = requests.get(url, allow_redirects=False)
    urlHead = response.headers.get("Location")
    if urlHead:
        ghVer = urlHead.rsplit("/", 1)[-1]
        ret = ghVer
    else:
        print("Error 002: Could not find version")
except requests.RequestException as e:
    print (f"Error: {e}")
ghVer = ghVer.lstrip("v")
ver = ver.lstrip("v")
try:
    if ghVer > ver:
        ret = 1
    elif ghVer < ver:
        ret = -1
    elif ghVer := ver:
        ret = 2
    else:
        ret = 0
except InvalidVersion as e:
    print(f"Error 003: Failed to parse version: {e}")
    ret = ("")

    
if ret == 1:
    print(f"Outdated version! Pleas update at github.com/MrCatGitHub/BadTranslate/releases/latest")
elif ret == -1:
    print("You are running a version from the future. You're either a developer, or something messed up big time.")
elif ret == 2:
    print("You are running the latest version!")
elif ret == 0:
    unknownErr()
else:
    print("")
def random_language_code():
    languages = list(LANGUAGES.keys())
    return random.choice(languages)

async def translate_text(text, iterations):
    translator = Translator()
    translated = text
    for i in range(iterations):
        try:
            lang_code = random_language_code()
            random_trans = await translator.translate(translated, dest=lang_code)
            eng_trans = await translator.translate(random_trans.text, dest='en')
            translated = eng_trans.text
            print(f"Iteration {i + 1}/{iterations}: {translated}")
        except Exception as e:
            print(f"Error during translation at iteration {i + 1}: {e}")
        time.sleep(1)
    return translated

def main():
    input_text = input("Enter the text you want to translate: ")
    iterations = int(input("Amount of iterations: (Default: 100) "))
    if not any(char.isdigit() for char in iterations):
        err1()
    if iterations == "":
        iterations == 100
    translated_text = asyncio.run(translate_text(input_text, iterations))
    print("Original text:", input_text)
    print("Translated text:", translated_text)
def err1():
    input('Error 1: Unexpected String. Press "Enter" to exit')

    root = Tk()
    root.withdraw()
    root.clipboard_clear()
    root.clipboard_append(translated_text)
    root.update()
    root.destroy()
    print("Copied result to clipboard.")

if __name__ == "__main__":
    main()
    yn = input('Done. Try another word? (y/n) ')
    if yn == 'y':
        main()
    elif yn == 'n':
        print ('Exiting now...')
        raise SystemExit()
    else:
        err1()

