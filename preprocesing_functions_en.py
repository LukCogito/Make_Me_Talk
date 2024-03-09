# Sada Python skriptů pro úpravu textového souboru s e-knihou do formy, vhodné pro mimic3 dialogový systém

# Import knihoven
import re
from num2words import num2words

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
    try:
        with open(cesta, 'r', encoding='utf-8') as soubor:
            # Načti jej do paměti
            text = soubor.read()
            # Aplikuj na něj fci najdi_spec_znaky
            spec_znaky = najdi_spec_znaky(text)

            # A vypiš všechny spec. znaky, které obsahuje
            print("Všechny speciální znaky bez duplicit:")
            for znak in spec_znaky:
                print(znak)

    # Pokud soubor nebyl nalezen, vypiš chybovou hlášku
    except FileNotFoundError:
        print(f"Soubor '{cesta}' nebyl nalezen.")

# Definice fce pro nahrazení spec. znaků v textu jejich přepisem v angličtině
def nahrad_spec_znaky(cesta):

    # Vytvořím si slovník s přepisem často používaných znaků (možno upravit podle konkrétní knihy)
    slovnik = {
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

    # Zkousím soubor otevřít
    try:
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

    # Pokud soubor nebyl nalezen, vypiš chybovou hlášku
    except FileNotFoundError:
        print(f"Soubor '{cesta}' nebyl nalezen.")


# Definice fce pro zmenšení písmen ve slovech delších než 4 písmena (která nejspíše nebudou zkratkami)
def zmensi_pismena(cesta):
    # Zkousím soubor otevřít
    try:
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
    
    # Pokud soubor nebyl nalezen, vypiš chybovou hlášku
    except FileNotFoundError:
        print(f"Soubor '{cesta}' nebyl nalezen.")


# Definice fce pro nahrazení čísel jejich přepisem slovy
def nahrad_cisla_slovy(cesta):
    try:
        # Načtu si textový soubor do proměnné podle cesty
        with open(cesta, 'r') as soubor:
            text = soubor.read()

        # Vytvořím regulární výraz pro nalezení čísel v textu
        reg_vyraz = r'\b\d+\b'

        # Definuji pod-funkci pro nahrazení shodujícího se vzorce čísly převedenými na slova
        def nahrad_cislo(shoda):
            cislo = int(shoda.group())
            return num2words(cislo)

        # Použiji metodu .sub() k nahrazení shodujících se čísel v textu
        vysledek = re.sub(reg_vyraz, nahrad_cislo, text)

        # Zapíši změny do souboru
        with open(cesta, 'w') as soubor:
            soubor.write(vysledek)
        print(f"Čísla v souboru '{cesta}' byla nahrazena slovy a změny uloženy.")

    # Pokud soubor nebyl nalezen, vypiš chybovou hlášku
    except FileNotFoundError:
        print(f"Soubor '{cesta}' nebyl nalezen.")
