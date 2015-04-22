#!/bin/bash

CORPORA="../team-lab-ss2015/data/pos"

paste $CORPORA/dev.col $CORPORA/dev-predicted.col >> $CORPORA/train.col

# Finding possible features, e.g. Affixes.
python perceptron.py -feat -i $CORPORA/train.col

#  Train the model
python perceptron.py -train -i $CORPORA/train.col

# Test the model
#python perceptron.py -test -i $CORPORA/train.col

# Evaluate the results
python perceptron.py -ev -i $CORPORA/train.col -o evaluation.txt

rm $CORPORA/train.col


