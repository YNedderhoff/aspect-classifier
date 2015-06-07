#!/bin/bash



feature_groups=("form_" "word_len_" "position_" "prefix_" "suffix_" "lettercombs_")
maximums=("12536" "54" "134" "5122" "4780" "1057")
step_sizes=("16" "1" "1" "7" "7" "2")

total=${#feature_groups[*]}
# 
for (( i=0; i<=$(( $total -1 )); i++ )) do
    screen -dmS "teamlab"$i ./run_feat_group.sh ${maximums[$i]} ${feature_groups[$i]} ${step_sizes[$i]}
done
