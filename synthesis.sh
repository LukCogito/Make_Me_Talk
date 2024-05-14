#!/usr/bin/env bash

# Cesta k souboru s knihou je prvním parametrem
cesta_vstup=$1

# Jazyk modelu pro syntézu je druhým parametrem
jazyk=$2

vycistit_tmp=$3

if [ $# -gt 0 ] && [ "$cesta_vstup" = "help" ]; then
  echo "Usage: ./synthesis.sh <input_file> <language> [rm]"
  echo "  <input_file>  - path to the text file with the book"
  echo "  <language>    - language of the book (en/cs)"
  echo "  [rm]          - optional parameter to remove temporary files"
  exit 0
fi

# Ověřím správnost zadaných parametrů
if [ $# -lt 2 ]; then
    echo "Usage: ./synthesis.sh <input_file> <language> [rm]" >&2
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
if [ -z "$OUTDIR" ]; then
  OUTDIR="./ebook_synthesis"
fi

# Namapuji obsah txt souboru do pole, kde bude každá jedna řádka samostatným prvkem
mapfile -t radky < "$cesta_vstup"

# Extrahuji z cesty název souboru bez přípony
jmeno_souboru=$(basename -s .txt "$cesta_vstup")

# Vytvořím cestu k výstupnímu souboru a dočasnému adresáři
mkdir -p $OUTDIR
mkdir -p $TMPDIR
cesta_vystup="$OUTDIR/${jmeno_souboru}.wav"

echo "Cesta k výstupnímu souboru: $cesta_vystup"

# Pokud je kniha česky
if [ "$jazyk" = "cs" ]; then
  # Připrav příkaz pro syntézu v češtině
  cmd='tts --text "${radky[$i]}" --model_name "tts_models/cs/cv/vits" --out_path "$TMPDIR/audio${i}.wav"'
# V opačném příápadě
else
  # Spustím server pro syntézu
  mimic3-server --preload-voice en_UK/apope_low &
  sleep 5 # čekám 5 sekund, než se server zapne

  # Připrav příkaz pro syntézu v angličtině
  cmd='echo "${radky[$i]}" | iconv -f UTF-8 -t ISO-8859-1//TRANSLIT 2>/dev/null | mimic3 --remote > "$TMPDIR/audio${i}.wav"'
fi

# Procházím pole položku po položce (procházím text řádku po řádce)
for (( i=0; i<${#radky[@]}; i++ )); do
  # Pro každou jednu iteraci provedu syntézu a indexovaný výstup uložím do adresáře temp
  eval $cmd
    #echo  "file '$TMPDIR/audio${i}.wav'" >> $TMPDIR/concat.txt
    # Používat relativní cesty -- budou relativní vůci $TMPDIR/concat.txt
  echo  "file 'audio${i}.wav'" >> $TMPDIR/concat.txt
done

if [ "$jazyk" = "en" ]; then
  # Ukončím server pro syntézu
  pkill mimic3-server
fi

# Nakonec spojím pomocí ffmpeg dílčí segmenty a vytvořím tak komplet
  #ffmpeg -f concat -safe 0 -i $TMPDIR/concat.txt -c copy $cesta_vystup
  # S relativními cestami uvnitř concat.txt nemusím používat -safe 0
ffmpeg -f concat -i $TMPDIR/concat.txt -c copy $cesta_vystup
if [ $vycistit_tmp ]; then
  rm -rf $TMPDIR/ 2>/dev/null
fi