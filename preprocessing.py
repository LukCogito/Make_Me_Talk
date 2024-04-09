# Sada Python skriptů pro úpravu textového souboru s e-knihou do formy, vhodné pro mimic3 dialogový systém

# Import knihoven
import re
from num2words import num2words
import sys


slovnik_en = {
        '+': 'plus',
        '€': ' Euro',
        '£': ' Pound',
        '%': 'percent',
        '>': 'greater than',
        '$': 'dollar ',
        '=': 'equals',
        '&': 'and',
        '|': 'or',
        '/': ' in proportion to ',
        '~': 'tilde',
        '×': 'times',
        '−': 'minus',
        '°': 'degree',
        '√': 'Square root',
        '*': 'asterisk',
        '_': 'Underscore',
        '□': 'Square symbol',
        '…': 'Ellipsis',
    }
slovnik_cs = {
        '+': 'plus',
        '€': ' euro',
        '£': ' libra',
        '%': ' procento',
        '>': ' větší než',
        '$': ' dolar',
        '=': ' rovná se',
        '&': ' a',
        '|': ' paralelně s',
        '/': ' v poměru k',
        '~': ' vlnovka',
        '×': ' krát',
        '−': ' minus',
        '°': ' stupeň',
        '√': ' druhá odmocnina',
        '*': ' hvězdička',
        '_': ' podtržítko',
        '□': ' čtverec',
        '...': ' trojtečka',
}

# Fce, která prohledá text a najde všechny speciální (neobvyklé) znaky v textu
def najdi_spec_znaky(text):
    # Vytvořím si pole na spec. znaky
    spec_znaky = set()
    # Procházím znaky v textu
    for znak in text:
        # Pokud není znak alfanumerický nebo číselný a zároveň není v poli se spec. znaky
        if not znak.isalnum() and znak not in spec_znaky:
            # Přidej jej do pole se spec. znaky
            spec_znaky.add(znak)
    # A vrať spec. znaky
    return spec_znaky

# Fce stavějící nad fcí najdi_spec_znaky, která načte soubor a vypíše všechny spec. znaky v něm obsažené
def nacti_soubor_vypis_spec_znaky(cesta):
    # Zkus soubor otevřít
    with open(cesta, 'r', encoding='utf-8') as soubor:
        # Načti jej do paměti
        text = soubor.read()
        # Aplikuj na něj fci najdi_spec_znaky
        spec_znaky = najdi_spec_znaky(text)

        # A vypiš všechny spec. znaky, které obsahuje
        print("Všechny speciální znaky bez duplicit:")
        for znak in spec_znaky:
            print(znak)

# Definice fce pro nahrazení spec. znaků v textu jejich přepisem v angličtině
def nahrad_spec_znaky(cesta, slovnik):

    # Zkousím soubor otevřít
    with open(cesta, 'r', encoding='utf-8') as soubor:
        # Načtu text ze souboru do proměnné text
        text = soubor.read()

    # Iteruji slovník se spec. znaky a přepisy
    for znak, prepis in slovnik.items():
        # Pro každou iteraci provedu nahrazení v textu
        text = text.replace(znak, prepis)
    
    # Zapíši změny do souboru
    with open(cesta, 'w') as soubor:
        soubor.write(text)

    print(f"Znaky v souboru '{cesta}' byly nahrazeny a změny uloženy.")



# Definice fce pro zmenšení písmen ve slovech delších než 4 písmena (která nejspíše nebudou zkratkami)
def zmensi_pismena(cesta):
    # Načtu si textový soubor do proměnné podle cesty
    with open(cesta, 'r') as soubor:
        text = soubor.read()

    # Vytvořím regulární výraz pro nalezení slov s alespoň 4 písmeny napsanými kapitálkami
    reg_vyraz = r'\b[A-Z]{4,}\b'

    # Definuji pod-funkci pro nahrazení shodujícího se vzorce pomocí malých písmen
    def ucin_malymi(shoda):
        return shoda.group().lower()

    # Použiji metodu .sub() k nahrazení shodujících se slov v textu
    vysledek = re.sub(reg_vyraz, ucin_malymi, text)

    # Zapíši změny do souboru
    with open(cesta, 'w') as soubor:
        soubor.write(vysledek)
    print(f"Znaky v souboru '{cesta}' byly nahrazeny a změny uloženy.")
    
# Definice fce pro nahrazení čísel jejich přepisem slovy
def nahrad_cisla_slovy(cesta):
    # Načtu si textový soubor do proměnné podle cesty
    with open(cesta, 'r') as soubor:
        text = soubor.read()

    # Vytvořím regulární výraz pro nalezení čísel v textu
    reg_vyraz = r'\b\d+\b'

    # Definuji pod-funkci pro nahrazení shodujícího se vzorce čísly převedenými na slova
    def nahrad_cislo(shoda):
        cislo = int(shoda.group())
        return num2words(cislo, lang=sys.argv[1])

    # Použiji metodu .sub() k nahrazení shodujících se čísel v textu
    vysledek = re.sub(reg_vyraz, nahrad_cislo, text)

    # Zapíši změny do souboru
    with open(cesta, 'w') as soubor:
        soubor.write(vysledek)
    print(f"Čísla v souboru '{cesta}' byla nahrazena slovy a změny uloženy.")

# Definice fce pro odstranění prázdných řádek v textu
def odstran_prazdne_radky(cesta):
    # Načtu si textový soubor do proměnné podle cesty
    with open(cesta, 'r') as soubor:
        text = soubor.readlines()
        # Použiji lamda (syntax pro zápis fce na jednu řádku) k filtrování prázdných řádek; převádím na list, protože filter vrací jiný datový typ
    text = list(filter(lambda s: s != "\n", text))
    with open(cesta, 'w') as soubor:
        soubor.writelines(text)
    print(f"Prázdné řádky byly odstraněny ze souboru v {cesta}.")

def preved_do_kodovani(cesta, encoding='utf-8'):
    # Načtu si textový soubor do proměnné podle cesty
    with open(cesta, 'r') as soubor:
        text = soubor.read()
    with open(cesta, 'w', encoding=encoding) as soubor:
        soubor.write(text.encode(encoding, 'ignore').decode(encoding))
    print(f"Text v souboru '{cesta}' byl převeden do kódování {encoding} a změny uloženy.")


# Pokud je skript spuštěn samostatně (a nikoliv jako modul)
if __name__ == "__main__":
    # Ověřím správnost zadaných argumentů
    # Pokud je argumentů méně než 3
    if len(sys.argv) < 3:
        # Vypíši uživateli hlášku s instruktáží
        print("Usage: python3 preprocessing.py <language> <input_file>")
        # A ukončím s hláškou o přítomnosti problému (1 = je přítomen)
        sys.exit(1)
    # Pokud druhý argument (jazyk) není en nebo cs
    cesta, jazyk = sys.argv[1], sys.argv[2]
    if jazyk not in ["en", "cs"]:
        # Vypíši uživateli hlášku s instruktáží
        print(f"Invalid language '{jazyk}'; language must be 'en' or 'cs'.")
        sys.exit(1)
        # A ukončím s hláškou o přítomnosti problému

    # Otestuji, jestli zadaný soubor existuje
    try:
        # Zkusím obsah souboru načíst do proměnné
        with open(cesta, 'r', encoding='utf-8') as soubor:
            pass
    # V případě výjimky vypíšu hlášku o chybě pro uživatele
    except FileNotFoundError:
        print(f"File '{cesta}' not found.")
        sys.exit(1)


    # Zvolím odpovídající slovník v závislosti na volbě jazyka
    slovnik = slovnik_en if jazyk == "en" else slovnik_cs

    # Vykonám odpovídající operace
    ENCODING="latin-1"
    print(f"Zpracovávám soubor '{cesta}'... v jazyce {jazyk}")
    zmensi_pismena(cesta)
    nahrad_cisla_slovy(cesta)
    nahrad_spec_znaky(cesta, slovnik)
    preved_do_kodovani(cesta, encoding=ENCODING)
    odstran_prazdne_radky(cesta)