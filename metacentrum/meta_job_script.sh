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

# TODO: generic path to Make_Me_Talk
cd $HOME/Make_Me_Talk/metacentrum

# to run mimic server, use --pid
# https://github.com/apptainer/singularity/issues/5884
singularity exec              \
     -B /cvmfs                \
    --pid                     \
    docker://mycroftai/mimic3 \
    /bin/bash meta_singularity_script.sh $BOOK $LANG
