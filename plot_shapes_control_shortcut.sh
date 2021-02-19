for era in 2018 2017 2016
do
    for channel in tt mt et em
    do
         bash plotting/plot_shapes_control.sh ${era} control_shapes-${era}-${channel}.root ${channel} &
     done
 done
 wait
