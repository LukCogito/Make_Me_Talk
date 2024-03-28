#!/bin/bash

if [ $2 = "en" ]; then
    alias mimic3='/home/mimic3/app/.venv/bin/mimic3'
elif [ $2 = "cs" ]; then
    echo "Czech not implemented yet" >&2
    exit 1
fi
alias ffmpeg='/cvmfs/software.metacentrum.cz/spack18/software/linux-debian11-x86_64_v2/gcc-10.2.1/ffmpeg-4.4.1-4b4plvbiawhrdfbuycgpodkgdlpdcuot/bin/ffmpeg'

cd ..
./synthesis.sh $1 $2

