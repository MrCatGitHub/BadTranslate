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

ver = "0.0.3-alpha.2"
exiting = 0
fallback = "en"
url = "https://github.com/MrCatGitHub/BadTranslate/releases/latest"

def unknownErr():
    print("Error 4: An unknown error ocurred")
def err1(q):
    if q == 0:
        print('Error 1: Unexpected String.')
    elif q == 1:
        input('Error 1: Unexpected String. Press "Enter" to exit.')

try:
    response = requests.get(url, allow_redirects=False)
    urlHead = response.headers.get("Location")
    if urlHead:
        ghVer = urlHead.rsplit("/", 1)[-1]
        ret = ghVer
    else:
        print("Error 2: Could not find version")
except requests.RequestException as e:
    print(f"Error: {e}")
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
    print(f"Error 3: Failed to parse: {e}")
    ret = ("")

def checkLangCode(lang):
    return lang in LANGUAGES
    
if ret == 1:
    print(f"Outdated version! Please update at github.com/MrCatGitHub/BadTranslate/releases/latest ({ver} < {ghVer})")
elif ret == -1:
    print(f"You are running a version from the future. You're either a developer, or something messed up big time. ({ver} > {ghVer})")
elif ret == 2:
    print(f"You are running the latest version! ({ver})")
elif ret == 0:
    unknownErr
else:
    print("")
def random_language_code():
    languages = list(LANGUAGES.keys())
    return random.choice(languages)

async def translate_text(text, iterations, langCode):
    translator = Translator()
    translated = text
    for i in range(iterations):
        try:
            lang_code = random_language_code()
            randomTrans = await translator.translate(translated, dest=lang_code)
            engTrans = await translator.translate(randomTrans.text, dest=langCode)
            translated = engTrans.text
            print(f"Iteration {i + 1}/{iterations}: {translated}")
        except Exception as e:
            print(f"Error during translation at iteration {i + 1}: {e}")
        time.sleep(1)
    return translated

#def detect(text):
#    translator = Translator()
#    try:
#        if asyncio.iscoroutinefunction(translator.detect):
#            result = translator.detect(text)
#        else:
#            result = translator.detect, text
#        return result
#    except Exception as e:
#        print(f"Error: {e}")
#        return None

def main():
    inputText = input("Enter the text you want to translate: ").strip()
    if not inputText:
        err1()
    langCode = input("Please select the destination language using short language codes: ").lower().strip()
    if langCode == "0":
        print("no.")
        langCode = fallback
    if checkLangCode(langCode):
        print(f'Language code "{langCode}" is detected as {LANGUAGES[langCode]}')
    else:
        print(f'Language code "{langCode}" is not valid.')
        print('Triggering fallback.')
        langCode = fallback
    iterations = input("Amount of iterations: (Default: 100) ")    
    if not iterations.strip():
        iterations = 100
    if iterations.isdigit():
        iterations = int(iterations)
    elif not iterations.isdigit(): #                                           I don’t care that this is technically not an integer;
        print(f'"{iterations}" is not an integer. Setting iterations to 100.')#it’s integer enough for me.
        iterations = 100
    if iterations >= 1000:
        print("An extremely high number of iterations has been selected; this might take 15 minutes or more.")
    elif iterations >= 250:
        print("A high number of iterations has been selected; this might take a long time.")
    elif iterations <= 0:
        print("You've selected 0 or fewer iterations; nothing will happen.")
    translated_text = asyncio.run(translate_text(inputText, iterations, langCode))
    print("Original text:", inputText)
    print("Translated text:", translated_text)

    root = Tk()
    root.withdraw
    root.clipboard_clear
    root.clipboard_append(translated_text)
    root.update
    root.destroy
    print("Copied result to clipboard.")

def launcher():
    if __name__ == "__main__":
        main()
        yn = input('Done. Try another word? (y/n) ')
        if yn == 'y':
            launcher()
        elif yn == 'n':
            print('Exiting now...')
            if ret == -1:
                print("Now get back in your DeLorean") #Back to the future reference hehe
            raise SystemExit
        else:
            exiting = 1
            err1(exiting)
launcher()