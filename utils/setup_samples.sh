#!/bin/bash
set -e

ERA=$1

#### ERA specific part. If a sample is not available comment it out here.
# Samples Run2016
basedir="/ceph/htautau/Run2Legacy_MSSM"
ARTUS_OUTPUTS_2016="$basedir/2016/ntuples/"
SVFit_Friends_2016="$basedir/2016/friends/SVFit/"
FF_Friends_2016="$basedir/2016/friends/FakeFactors_v2/"
NLOReweighting_Friends_2016="$basedir/2016/friends/NLOReweighting/"
ML_Friends_2016="$basedir/2016/friends/ML_mass/"

# Samples Run2017
ARTUS_OUTPUTS_2017="$basedir/2017/ntuples/"
SVFit_Friends_2017="$basedir/2017/friends/SVFit/"
FF_Friends_2017="$basedir/2017/friends/FakeFactors_v2/"
NLOReweighting_Friends_2017="$basedir/2017/friends/NLOReweighting/"
ML_Friends_2017="$basedir/2017/friends/ML_mass/"

# Samples Run2018
ARTUS_OUTPUTS_2018="$basedir/2018/ntuples/"
SVFit_Friends_2018="$basedir/2018/friends/SVFit/"
FF_Friends_2018="$basedir/2018/friends/FakeFactors_v2/"
NLOReweighting_Friends_2018="$basedir/2018/friends/NLOReweighting/"
#ML_Friends_2018="$basedir/2018/friends/ML_mass/"


# ERA handling
if [[ $ERA == *"2016"* ]]
then
    ARTUS_OUTPUTS=$ARTUS_OUTPUTS_2016
    SVFit_Friends=$SVFit_Friends_2016
    FF_Friends=$FF_Friends_2016
    NLOReweighting_Friends=$NLOReweighting_Friends_2016
    ML_Friends=$ML_Friends_2016
elif [[ $ERA == *"2017"* ]]
then
    ARTUS_OUTPUTS=$ARTUS_OUTPUTS_2017
    SVFit_Friends=$SVFit_Friends_2017
    FF_Friends=$FF_Friends_2017
    NLOReweighting_Friends=$NLOReweighting_Friends_2017
    ML_Friends=$ML_Friends_2017
elif [[ $ERA == *"2018"* ]]
then
    ARTUS_OUTPUTS=$ARTUS_OUTPUTS_2018
    SVFit_Friends=$SVFit_Friends_2018
    FF_Friends=$FF_Friends_2018
    NLOReweighting_Friends=$NLOReweighting_Friends_2018
    ML_Friends=$ML_Friends_2018
fi

### channels specific friend tree.
# Used for example to process the event channel without including the fakefactor friends
ARTUS_FRIENDS_EM="$SVFit_Friends $NLOReweighting_Friends $ML_Friends"
ARTUS_FRIENDS_ET="$SVFit_Friends $NLOReweighting_Friends $ML_Friends"
ARTUS_FRIENDS_MT="$SVFit_Friends $NLOReweighting_Friends $ML_Friends"
ARTUS_FRIENDS_TT="$SVFit_Friends $NLOReweighting_Friends $ML_Friends"
ARTUS_FRIENDS="$SVFit_Friends $NLOReweighting_Friends $ML_Friends"
ARTUS_FRIENDS_FAKE_FACTOR=$FF_Friends
