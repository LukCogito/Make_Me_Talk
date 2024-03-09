# Sada Python skriptů pro úpravu textového souboru s e-knihou do formy, vhodné pro mimic3 dialogový systém

# Import knihoven
import re
from num2words import num2words

# Import funkcí z en verze skriptu
from preprocesing_functions_en import nacti_soubor_vypis_spec_znaky, najdi_spec_znaky

# Definice fce pro nahrazení spec. znaků v textu jejich přepisem v angličtině
def nahrad_spec_znaky(cesta):

    # Vytvořím si slovník s přepisem často používaných znaků (možno upravit podle konkrétní knihy)
    slovnik = {
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
    except souborNotFoundError:
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
    except souborNotFoundError:
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
            return num2words(cislo, lang='cz')

        # Použiji metodu .sub() k nahrazení shodujících se čísel v textu
        vysledek = re.sub(reg_vyraz, nahrad_cislo, text)

        # Zapíši změny do souboru
        with open(cesta, 'w') as soubor:
            soubor.write(vysledek)
        print(f"Čísla v souboru '{cesta}' byla nahrazena slovy a změny uloženy.")

    # Pokud soubor nebyl nalezen, vypiš chybovou hlášku
    except souborNotFoundError:
        print(f"Soubor '{cesta}' nebyl nalezen.")

# Definice fce pro odstranění prázdných řádek v textu
def odstran_prazde_radky(cesta):
    try:
        # Načtu si textový soubor do proměnné podle cesty
        with open(cesta, 'r') as soubor:
            text = soubor.read()

        # Nahradím dvojité nové řádky (\n\n) jednoduchými novými řádky (\n), čímž odstraním prázdné řádky
        text = text.replace('\n\n', '\n')

        # Zapíši změny do souboru
        with open(cesta, 'w') as soubor:
            soubor.write(text)
        
        print(f"Prázdné řádky byly odstraněny ze souboru v {cesta}.")
    
    # Pokud soubor nebyl nalezen, vypiš chybovou hlášku
    except souborNotFoundError:
        print(f"Soubor '{cesta}' nebyl nalezen.")