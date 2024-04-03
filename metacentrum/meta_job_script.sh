#!/bin/bash
#PBS -N mimic3_synth
#PBS -l select=1:ncpus=1:mem=20gb:scratch_local=60gb
#PBS -l walltime=24:00:00 

export HOME=$HOMEDIR
export TMPDIR=$SCRATCHDIR
module add conda-modules
conda activate Make_Me_Talk_venv
module add ffmpeg

trap 'clean_scratch' EXIT TERM

cd $HOME/Make_Me_Talk/metacentrum

singularity exec              \
     -B /cvmfs                \
    docker://mycroftai/mimic3 \
    /bin/bash meta_singularity_script.sh $BOOK $LANG