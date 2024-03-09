#!/bin/bash

# Načtu cestu k txt souboru s knihou
cesta_vstup="./data/Sri_Ramana_Maharshi,_David_Godman_-_Be_as_You_Are__The_Teachings_of_Sri_Ramana_Maharshi-Penguin_Books_Ltd.txt"

# Extrahuji z ní název souboru bez přípony
jmeno_souboru=$(basename -s .txt "$cesta_vstup")

# Vytvořím cestu k výstupnímu souboru
cesta_vystup="./ebook_synthesis/${jmeno_souboru}.mp3"

echo "Syntetizuji knihu pomocí mimic3 TTS enginu..."

# Příkaz na syntézu knihy
cat $cesta_vstup | mimic3 > $cesta_vystup

echo "Syntéza dokončena."