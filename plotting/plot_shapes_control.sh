# source utils/setup_cvmfs_sft.sh
# source utils/setup_python.sh

ERA=$1
INPUT=$2
ch=$3
suffix=$4

v="pt_1,pt_2,eta_1,eta_2,m_vis,m_sv_puppi,pt_tt_puppi,ptvis,jpt_1,jpt_2,jeta_1,jeta_2,bpt_1,bpt_2,puppimet,DiTauDeltaR,pZetaPuppiMissVis,mt_1_puppi,mt_2_puppi,mTdileptonMET_puppi,njets,nbtag,jdeta,dijetpt,mjj"
v="pt_1,pt_2,eta_1,eta_2,phi_1,phi_2,m_vis,m_sv_puppi,pt_tt_puppi,ptvis,jpt_1,jpt_2,jeta_1,jeta_2,jphi_1,jphi_2,jpt_r,jeta_r,jphi_r,Njet_r,bpt_1,bpt_2,puppimet,puppimetphi,DiTauDeltaR,pZetaPuppiMissVis,mt_1_puppi,mt_2_puppi,mTdileptonMET_puppi,njets,nbtag,jdeta,dijetpt,mjj,npv,mt_tot_puppi,ml_mass"

if [[ $suffix == "jets_r" ]]
then
    v="jpt_r,jeta_r,jphi_r,Njet_r"
fi

plotting/plot_shapes_control.py -l --era Run${ERA} --input $INPUT --variables ${v} --channels ${ch} --embedding --fake-factor --normalize-by-bin-width --suffix=$suffix
plotting/plot_shapes_control.py -l --era Run${ERA} --input $INPUT --variables ${v} --channels ${ch} --fake-factor --normalize-by-bin-width --suffix=$suffix
plotting/plot_shapes_control.py -l --era Run${ERA} --input $INPUT --variables ${v} --channels ${ch} --embedding --normalize-by-bin-width --suffix=$suffix
plotting/plot_shapes_control.py -l --era Run${ERA} --input $INPUT --variables ${v} --channels ${ch} --normalize-by-bin-width --suffix=$suffix

#v="NNrecoil_pt,nnmet,mt_1_nn,mt_2_nn,mt_tot_nn,pt_tt_nn,pZetaNNMissVis,pt_ttjj_nn,mTdileptonMET_nn"
#ch="mt,et,tt,em"
#plotting/plot_shapes_control.py -l  --era Run2017 --input shapes.root --variables ${v} --channels ${ch} --embedding --fake-factor
#plotting/plot_shapes_control.py -l  --era Run2017 --input shapes.root --variables ${v} --channels ${ch} --fake-factor
#plotting/plot_shapes_control.py -l  --era Run2017 --input shapes.root --variables ${v} --channels ${ch} --embedding
#plotting/plot_shapes_control.py -l  --era Run2017 --input shapes.root --variables ${v} --channels ${ch}

# v="m_vis,m_vis_high,ptvis,met,puppimet,metParToZ,metPerpToZ,puppimetParToZ,puppimetPerpToZ,pt_1,pt_2,eta_1,eta_2,njets,jpt_1,jpt_2,jeta_1,jeta_2"
# ch="mm"
# plotting/plot_shapes_control.py -l  --era Run2017 --input shapes.root --variables ${v} --channels ${ch}
# plotting/plot_shapes_control.py -l  --era Run2017 --input shapes.root --variables ${v} --channels ${ch} --category-postfix "peak"
