import random, time, os, requests, asyncio, argparse
from packaging.version import InvalidVersion
from googletrans import Translator, LANGUAGES
from tkinter import Tk
from tqdm import tqdm

ver = "0.0.3-alpha.3"
exiting = 0
fallback = "en"

cli = argparse.ArgumentParser(description="BadTranslate CLI")
cli.add_argument("-s", "--simple", action="store_true", help="Use the simple mode")
args = cli.parse_args()

def unknownErr():
    print("Error 4: An unknown error ocurred")
def err1(q):
    if q == 0:
        input('Error 1: Unexpected String.')
    elif q == 1:
        input('Error 1: Unexpected String. Press "Enter" to exit.')

try:
    response = requests.get("https://github.com/MrCatGitHub/BadTranslate/releases/latest", allow_redirects=False)
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

async def translateText(text, iterations, langCode):
    translator = Translator()
    translated = text
    for i in tqdm(range(iterations), desc="Translating"):
        try:
            lang_code = random_language_code()
            randomTrans = await translator.translate(translated, dest=lang_code)
            resultTrans = await translator.translate(randomTrans.text, dest=langCode)
            translated = resultTrans.text
            tqdm.write(f"Iteration {i + 1}/{iterations}: {translated}")
        except Exception as e:
            tqdm.write(f"Error during translation at iteration {i + 1}: {e}")
    return translated
async def translateTextSimple(text, iterations, langCode):
    translator = Translator()
    translated = text
    for i in tqdm(range(iterations), desc="Translating"):
        try:
            lang_code = random_language_code()
            randomTrans = await translator.translate(translated, dest=lang_code)
            resultTrans = await translator.translate(randomTrans.text, dest=langCode)
            translated = resultTrans.text
        except:
            print("Something went wrong... =(")

def main():
    inputText = input("Enter the text you want to translate: ").strip()
    if not inputText:
        err1(1)
    langCode = input("Please select the destination language using short language codes: ").lower().strip()
    if checkLangCode(langCode):
        print(f'Language code "{langCode}" is detected as {LANGUAGES[langCode]}')
    elif langCode == "":
        langCode = "en"
        print("Set language to english.")
    else:
        print(f'Language code "{langCode}" is not valid.')
        print('Triggering fallback.')
        langCode = fallback
    if langCode == "0":
        print("no.")
        langCode = fallback
    iterations = input("Amount of iterations: (Default: 100) ").strip()
    if not iterations.strip():
        iterations = 100
    elif iterations.isdigit():
        iterations = int(iterations)
    elif not iterations.isdigit(): #                                           I don't care that this is technically not an integer;
        print(f'"{iterations}" is not an integer. Setting iterations to 100.')#it's integer enough for me.
        iterations = 100
    if iterations >= 1000:
        print("An extremely high number of iterations has been selected; this might take 15 minutes or more.")
    elif iterations >= 250:
        print("A high number of iterations has been selected; this might take a long time.")
    elif iterations <= 0:
        print("You've selected 0 or fewer iterations; nothing will happen.")
    if not args.simple:
        translated_text = asyncio.run(translateText(inputText, iterations, langCode))
    else:
        translated_text = asyncio.run(translateTextSimple(inputText, iterations, langCode))
    print("Original text:", inputText)
    print("Translated text:", translated_text)

    root = Tk()
    root.withdraw()
    root.clipboard_clear()
    root.clipboard_append(translated_text)
    root.update()
    root.destroy()
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
            err1(1)
launcher()