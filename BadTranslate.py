import random
import time
from googletrans import Translator, LANGUAGES
from tkinter import Tk

def random_language_code():
    languages = list(LANGUAGES.keys())
    return random.choice(languages)

def translate_text(text, iterations=100):
    translator = Translator()
    for i in range(iterations):
        try:
            lang_code = random_language_code()
            translated = translator.translate(text, dest=lang_code)
            text = translator.translate(translated.text, dest='en').text
            print(f"Iteration {i+1}/{iterations}: {text}")
        except Exception as e:
            print(f"Error during translation at iteration {i+1}: {e}")
            time.sleep(1)
    return text

def main():
    input_text = input("Enter the text you want to translate: ")
    translated_text = translate_text(input_text)
    print("Original text: ", input_text)
    print("Translated text: ", translated_text)
    Tk.withdraw()
    Tk.clipboard_clear()
    Tk.clipboard_append(translated_text)
    Tk.update()
    print('Copied result to clipboard.')
    Tk.destroy()

if __name__ == "__main__":
    main()
    yn = input('Done. Try another word? (y/n) ')
    if yn == 'y' or 'Y':
        main()
    elif yn == 'n' or 'N':
        print ('Exiting now...')
        raise SystemExit()
    else:
        input('Unexpected String. Press "Enter" to exit')
