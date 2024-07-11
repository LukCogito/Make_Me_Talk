# A set of Python scripts for editing text file with e-book to form, suitable for a synthesis with Piper dialog system

import sys
import nltk

nltk.download('punkt')

# Definice fce pro odstranění prázdných řádek v textu
def odstran_prazdne_radky(path):
    # Načtu si textový file do proměnné podle cesty
    with open(path, 'r') as file:
        text = file.readlines()
        # Použiji lamda (syntax pro zápis fce na jednu řádku) k filtrování prázdných řádek; převádím na list, protože filter vrací jiný datový typ
    text = list(filter(lambda s: s != "\n", text))
    with open(path, 'w') as file:
        file.writelines(text)
    print(f"Prázdné řádky byly odstraněny ze fileu v {path}.")

def split_long_lines(path):

    with open(path, "r") as file:
        text = file.read()
        text_split = text.splitlines()

        for line in text_split:
            
            # 1000 chars is value under upper threshold that piper can synthesise for one epoch
            if len(line) >= 1000:
                sentences = nltk.sent_tokenize()
                sentences.reverse()

                for index in len(words)-1:
    
                    if words.reverse()[index] == ".":
                        words_reversed = words.reverse()
                        words_reversed.insert(index-1, "\n")
                        words = words_reversed.reverse()
                        line = " ".join(words)

        text = "\n".join(text_split)
        return text


# Pokud je skript spuštěn samostatně (a nikoliv jako modul)
if __name__ == "__main__":
    # Ověřím správnost zadaných argumentů
    # Pokud je argumentů méně než 3
    if len(sys.argv) < 3:
        # Vypíši uživateli hlášku s instruktáží
        print("Usage: python3 preprocessing.py <language> <input_file>")
        # A ukončím s hláškou o přítomnosti problému (1 = je přítomen)
        sys.exit(1)
    # Pokud druhý argument (jazyk) není en nebo cz
    path, jazyk = sys.argv[1], sys.argv[2]
    if jazyk not in ["en", "cz"]:
        # Vypíši uživateli hlášku s instruktáží
        print(f"Invalid language '{jazyk}'; language must be 'en' or 'cz'.")
        sys.exit(1)
        # A ukončím s hláškou o přítomnosti problému

    # Otestuji, jestli zadaný file existuje
    try:
        # Zkusím obsah fileu načíst do proměnné
        with open(path, 'r', encoding='utf-8') as file:
            pass
    # V případě výjimky vypíšu hlášku o chybě pro uživatele
    except FileNotFoundError:
        print(f"File '{path}' not found.")
        sys.exit(1)


    # Zvolím odpovídající slovník v závislosti na volbě jazyka
    dict = dict_en if jazyk == "en" else dict_cs

    # Vykonám odpovídající operace
    print(f"Zpracovávám file '{path}'... v jazyce {jazyk}")
    odstran_prazdne_radky(path)