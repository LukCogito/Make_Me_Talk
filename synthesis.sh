#!/usr/bin/env bash

# Cesta k souboru s knihou je prvním parametrem
cesta_vstup=$1

# Jazyk modelu pro syntézu je druhým parametrem
jazyk=$2

# Ověřím správnost zadaných parametrů
if [ $# -lt 2 ]; then
    echo "Usage: ./synthesis.sh <language> <input_file>" >&2
    exit 1
elif [ ! -f "${cesta_vstup}" ]; then
    echo "Input file ${cesta_vstup} does not exist." >&2
    exit 1
else
    case "$jazyk" in
        en | cs ) ;;
        * ) echo "Invalid language '$jazyk'; must be 'en' or 'cs'" >&2; exit 1;;
    esac
fi

if [ -z "$TMPDIR" ]; then
  TMPDIR="./data/tmp"
fi

# Namapuji obsah txt souboru do pole, kde bude každá jedna řádka samostatným prvkem
mapfile -t radky < "$cesta_vstup"

# Extrahuji z cesty název souboru bez přípony
jmeno_souboru=$(basename -s .txt "$cesta_vstup")

# Vytvořím cestu k výstupnímu souboru
cesta_vystup="./ebook_synthesis/${jmeno_souboru}.wav"

echo "Cesta k výstupnímu souboru: $cesta_vystup"

# Pokud je kniha česky
if [ "$jazyk" = "cs" ]; then
  # Připrav příkaz pro syntézu v češtině
  cmd='tts --text "${radky[$i]}" --model_name "tts_models/cs/cv/vits" --out_path "$TMPDIR/audio${i}.wav"'
# V opačném příápadě
else
  # Připrav příkaz pro syntézu v angličtině
  cmd='echo "${radky[$i]}" | mimic3 > "$TMPDIR/audio${i}.wav"'
fi

# Procházím pole položku po položce (procházím text řádku po řádce)
for (( i=0; i<${#radky[@]}; i++ )); do
  # Pro každou jednu iteraci provedu syntézu a indexovaný výstup uložím do adresáře temp
  $(eval $cmd)
  echo  "file '$TMPDIR/audio${i}.wav'" >> $TMPDIR/concat.txt
done

# Nakonec spojím pomocí sox dílčí segmenty a vytvořím tak komplet
ffmpeg -f concat -i $TMPDIR/concat.txt -c copy $cesta_vystup
rm -rf $TMPDIR/ 2>/dev/null
