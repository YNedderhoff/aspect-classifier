#!/bin/bash

COUNTER=1
MAXIMUM=100

while [ "$COUNTER" -le "$MAXIMUM" ]; do

    screen -S "teamlab"$COUNTER -X quit

    let COUNTER=COUNTER+1

done





