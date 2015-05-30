#!/bin/bash

COUNTER=0
MAXIMUM=20
LINES=12741

while [ $COUNTER -le $MAXIMUM ]; do

    let COUNTER2=$COUNTER+1

    screen -dmS "teamlab"$COUNTER2 ./run1.sh $(($COUNTER*$LINES)) $(($COUNTER2*$LINES))
    
    let COUNTER=COUNTER+1

done



