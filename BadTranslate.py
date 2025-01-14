import random
import time
from googletrans import Translator, LANGUAGES
from tkinter import Tk
import asyncio

def random_language_code():
    languages = list(LANGUAGES.keys())
    return random.choice(languages)

async def translate_text(text, iterations=100):
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
    translated_text = asyncio.run(translate_text(input_text, iterations=100))
    print("Original text:", input_text)
    print("Translated text:", translated_text)

    #root = Tk()
    #root.withdraw()
    #root.clipboard_clear()
    #root.clipboard_append(translated_text)
    #root.update()
    #root.destroy()
    #print("Copied result to clipboard.")

if __name__ == "__main__":
    main()
    yn = input('Done. Try another word? (y/n) ')
    if yn == 'y':
        main()
    elif yn == 'n':
        print ('Exiting now...')
        raise SystemExit()
    else:
        input('Unexpected String. Press "Enter" to exit')
