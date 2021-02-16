#!/bin/bash

ERA=$1
CHANNEL=$2
VARIABLE=$3
TAG=$4

CONTROL=$5
USE_ML=$6

[[ ! -z $5 ]] || CONTROL=0

[[ ! -z $5 ]] || USE_ML=1

source utils/bashFunctionCollection.sh
source utils/setup_root.sh

ML_PREFIX=""
if [[ "$USE_ML" == 1 ]]
then
    ML_PREFIX="ML_"
fi

if [[ $CONTROL == 0 ]]
then
    logandrun python shapes/convert_to_synced_shapes.py -e $ERA \
                                                        -i output/shapes/${ERA}-${CHANNEL}-${ML_PREFIX}analysis-shapes-${TAG}/shapes-${ML_PREFIX}analysis-${ERA}-${CHANNEL}.root \
                                                        -o output/shapes/${ERA}-${CHANNEL}-${TAG}-${ML_PREFIX}synced_shapes_${VARIABLE} \
                                                        --variable-selection ${VARIABLE} \
                                                        -n 12
    OUTFILE=output/shapes/${ERA}-${CHANNEL}-${TAG}-${ML_PREFIX}synced_shapes_${VARIABLE}.root
    echo "[INFO] Adding written files to single output file $OUTFILE..."
    logandrun hadd -f $OUTFILE output/shapes/${ERA}-${CHANNEL}-${TAG}-${ML_PREFIX}synced_shapes_${VARIABLE}/*.root
else
    logandrun python shapes/convert_to_synced_shapes.py -e $ERA \
                                                        -i output/shapes/${ERA}-${CHANNEL}-${ML_PREFIX}control-shapes-${TAG}/shapes-control-${ERA}-${CHANNEL}.root \
                                                        -o output/shapes/${ERA}-${CHANNEL}-${TAG}-gof-${ML_PREFIX}synced_shapes \
                                                        --gof \
                                                        -n 12
fi
