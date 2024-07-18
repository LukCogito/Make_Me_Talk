#!/bin/bash

# Arguments
input_path=$1
language=$2
# Optional argument with default value
gender="${3:-male}"

# Check number of arguments
if [ $# -lt 2 ]; then
    echo "Usage: ./synthesis.sh <input_file> <language> <gender=male>" >&2
    exit 1
fi

# Check if input file exists
if [ ! -f "${input_path}" ]; then
    echo "Input file ${input_path} does not exist." >&2
    exit 1
fi

# Validate language and gender
case "$language" in
    en | cs ) ;;
    * ) echo "Invalid language '$language'; must be 'en' or 'cs'" >&2; exit 1;;
esac

case "$gender" in
    male | female ) ;;
    * ) echo "Invalid gender '$gender'; in universe of this script, gender must be 'male' or 'female'" >&2; exit 1;;
esac

# Set temporary and output directories
if [ -z "$TMPDIR" ]; then
  TMPDIR="./data/tmp"
fi
if [ -z "$OUTDIR" ]; then
  OUTDIR="./synthesis"
fi

# Map the content of the txt file into an array
mapfile -t lines < "$input_path"

# Extract filename without extension
file_name=$(basename -s .txt "$input_path")

mkdir -p $OUTDIR
mkdir -p $TMPDIR
mkdir -p "./voices/"
output_path="$OUTDIR/${file_name}.wav"

echo "A path to the output file: $output_path"

# Choose TTS model based on language and gender
if [ "$language" = "cs" ]; then
  if [ ! -f "./voices/cs_CZ-jirka-medium.onnx" ]; then
    wget -P ./voices/ https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/cs/cs_CZ/jirka/medium/cs_CZ-jirka-medium.onnx
    wget -P ./voices/ https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/cs/cs_CZ/jirka/medium/cs_CZ-jirka-medium.onnx.json
  fi
  cmd='echo "${lines[$i]}" | piper --model ./voices/cs_CZ-jirka-medium.onnx --output_file "$TMPDIR/audio${i}.wav"'
else
  if [ "$gender" = "male" ]; then
    if [ ! -f "./voices/en_GB-alan-medium.onnx" ]; then
      wget -P ./voices/ https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/alan/medium/en_GB-alan-medium.onnx
      wget -P ./voices/ https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/alan/medium/en_GB-alan-medium.onnx.json
    fi
    cmd='echo "${lines[$i]}" | piper --model ./voices/en_GB-alan-medium.onnx --output_file "$TMPDIR/audio${i}.wav"'
  else
    if [ ! -f "./voices/en_GB-cori-high.onnx" ]; then
      wget -P ./voices/ https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/cori/high/en_GB-cori-high.onnx
      wget -P ./voices/ https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/cori/high/en_GB-cori-high.onnx.json
    fi
    cmd='echo "${lines[$i]}" | piper --model ./voices/en_GB-cori-high.onnx --output_file "$TMPDIR/audio${i}.wav"'
  fi
fi

# Generate audio files and create a list for concatenation
for (( i=0; i<${#lines[@]}; i++ )); do
  eval $cmd
  echo "file 'audio${i}.wav'" >> $TMPDIR/concat.txt
  current_line=$((i + 1))
  # https://www.howtogeek.com/floating-point-math-in-linux-bash/
  ratio=$(echo "scale=2; $current_line/${#lines[@]}" | bc)
  percent=$(echo "$ratio * 100" | bc)
  echo "$current_line lines out of ${#lines[@]} ($percent %)"
done

# Concatenate audio files using ffmpeg
ffmpeg -hide_banner -loglevel error -f concat -safe 0 -i $TMPDIR/concat.txt -c copy $output_path

# Clean up temporary directory
if [ -f $output_path ]; then
    rm -rf $TMPDIR/ 2>/dev/null
fi