#!/bin/bash

# TODO: pipeline pro nahrání do MC
# TODO: použít `mimic3-server --preload-voice /usr/share/mycroft/mimic3/voices/n_UK/apope_low` a `mimic3 --remote`

# https://superuser.com/questions/708462/alias-scoping-in-bash-functions
shopt -s expand_aliases

if [ $2 = "en" ]; then
    alias mimic3='/home/mimic3/app/.venv/bin/mimic3' #--remote'
    alias mimic3-server='/home/mimic3/app/.venv/bin/mimic3-server'
elif [ $2 = "cs" ]; then
    echo "Czech not implemented yet" >&2
    exit 1
fi
alias ffmpeg='/cvmfs/software.metacentrum.cz/spack18/software/linux-debian11-x86_64_v2/gcc-10.2.1/ffmpeg-4.4.1-4b4plvbiawhrdfbuycgpodkgdlpdcuot/bin/ffmpeg'

#https://github.com/danielgatis/rembg/issues/448
export OMP_NUM_THREADS=$(nproc)

cd ..
source ./synthesis.sh $1 $2


