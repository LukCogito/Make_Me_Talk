#!/bin/bash

# Načtu cestu k txt souboru s knihou
cesta_vstup="./data/fv1.txt"

# Namapuji obsah txt souboru do pole, kde bude každá jedna řádka samostatným prvkem
mapfile -t radky < "$cesta_vstup"

# Extrahuji z cesty název souboru bez přípony
jmeno_souboru=$(basename -s .txt "$cesta_vstup")

# Vytvořím cestu k výstupnímu souboru
cesta_vystup="./ebook_synthesis/${jmeno_souboru}.wav"

echo "Cesta k výstupnímu souboru: $cesta_vystup"

# Procházím pole položku po položce (procházím text řádku po řádce)
for (( i=0; i<${#radky[@]}; i++ )); do
  # Pro každou jednu iteraci provedu syntézu a indexovaný výstup uložím do adresáře temp
  tts --text "${radky[$i]}" --model_name "tts_models/cs/cv/vits" --out_path "./data/temp/audio${i}.wav"
done

# Nakonec spojím pomocí sox dílčí segmenty a vytvořím tak komplet
sox './data/temp/*' $cesta_vystup