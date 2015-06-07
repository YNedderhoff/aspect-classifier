#!/bin/bash

COUNTER=0
MAXIMUM=5

while [ "$COUNTER" -le "$MAXIMUM" ]; do

    screen -S "teamlab"$COUNTER -X quit

    let COUNTER=COUNTER+1

done





