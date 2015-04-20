#!/bin/bash

CORPORA="../team-lab-ss2015/data/pos"

paste $CORPORA/dev.col $CORPORA/dev-predicted.col >> $CORPORA/train.col

python perceptron.py -i $CORPORA/train.col -o evaluation.txt

rm $CORPORA/train.col


