for era in 2018 2017 2016
do
    bash plotting/plot_shapes_mssm.sh $era /work/ltortero/MSSMvsSMRun2Legacy/CMSSW_10_2_21/src/CombineHarvester/MSSMvsSMRun2Legacy/output_shapes_mssm/ 1 1 tt mt et em --model-independent
    bash plotting/plot_shapes_mssm.sh $era /work/ltortero/MSSMvsSMRun2Legacy/CMSSW_10_2_21/src/CombineHarvester/MSSMvsSMRun2Legacy/output_shapes_mssm_vs_sm_h125/ 1 1 tt mt et em
done
