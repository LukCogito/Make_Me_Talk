#!/bin/sh
#PBS -l select:1:ncpus=1:mem=20gb
#PBS -l walltime=24:00:00
#PBS -N mimic3_synth

HOME = $HOMEDIR
export TMPDIR=$SCRATCHDIR
module add conda-modules
conda activate Make_Me_Talk_venv

module add ffmpeg

trap clean_scratch EXIT TERM

cd $HOME/Make_Me_Talk
singularity exec docker://mycroftai/mimic3 ./synthesis.sh $BOOK $LANG


