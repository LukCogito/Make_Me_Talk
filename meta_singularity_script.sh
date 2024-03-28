#!/bin/bash

if [ $2 -eq "en" ]; then
    alias mimic3='/home/mimic3/app/.venv/bin/mimic3'
elif [ $2 -eq "cs" ]; then
    echo "Czech not implemented yet" >&2
    exit 1
fi

./synthesis.sh $1 $2

