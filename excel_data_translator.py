# pip install pandas openpyxl translate

import pandas as pd
from translate import Translator

file_path = '/content/Dewa.csv'

df = pd.read_csv(file_path)

df.drop_duplicates(inplace=True)

translator = Translator(to_lang="en")

def translate_to_english(text):
    try:
        translated = translator.translate(text)
        return translated
    except Exception as e:
        print(f"Error translating text: {text}. Error: {e}")
        return text

df['Title'] = df['Title'].apply(translate_to_english)
df['Text'] = df['Text'].apply(translate_to_english)

output_file_path = 'filtered_sorted_translated_data.xlsx'
df.to_excel(output_file_path, index=False)

print(f"Filtered, sorted, and translated data saved to {output_file_path}")
