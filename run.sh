#!/bin/bash

CORPORA="../team-lab-ss2015/data/pos"

paste $CORPORA/dev.col $CORPORA/dev-predicted.col >> $CORPORA/train.col

python evaluation.py -i $CORPORA/train.col

rm $CORPORA/train.col


