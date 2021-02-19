#!/bin/bash

source utils/setup_cvmfs_sft.sh
source utils/setup_python.sh

ERA=$1
DIR=$2
JETFAKES=$3
EMBEDDING=$4
ML_MASS=$5
CHANNELS=${@:6}

EMBEDDING_ARG=""
if [ $EMBEDDING == 1 ]
then
    EMBEDDING_ARG="--embedding"
fi

JETFAKES_ARG=""
if [ $JETFAKES == 1 ]
then
    JETFAKES_ARG="--fake-factor"
fi

ML_MASS_ARG=""
if [ $ML_MASS == 1 ]
then
    ML_MASS_ARG="--ml_mass"
fi

for FILE in ${DIR}/${ERA}/cmb/prefit_shapes.root
do
    for OPTION in "" "--png"
    do
        ./plotting/plot_shapes_mssm.py -i $FILE -c $CHANNELS -e $ERA $OPTION $JETFAKES_ARG $EMBEDDING_ARG $ML_MASS_ARG --normalize-by-bin-width -o ${DIR}/${ERA}/cmb --blinded # --linear
    done
done
