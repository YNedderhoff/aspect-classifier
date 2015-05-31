#!/bin/bash

COUNTER=0
MAXIMUM=20
LINES=565

while [ "$COUNTER" -le "$MAXIMUM" ]; do

    let COUNTER2=$COUNTER+1

    if [ $(($COUNTER2*$LINES)) -gt 11288 ]; then
        screen -dmS "teamlab"$COUNTER2 ./run1b.sh $(($COUNTER*$LINES)) 11288 $COUNTER
    else
        screen -dmS "teamlab"$COUNTER2 ./run1b.sh $(($COUNTER*$LINES)) $(($COUNTER2*$LINES)) $COUNTER
    fi
    
    let COUNTER=COUNTER+1

done



