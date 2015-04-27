#!/bin/bash

CORPORA="../team-lab-ss2015/data/pos"

rm prediction.col

head -200 $CORPORA/train.col >> $CORPORA/train_top5000.col
head -200 $CORPORA/dev.col >> $CORPORA/dev_top5000.col

# Finding possible features, e.g. Affixes.
#python perceptron.py -feat -i $CORPORA/train.col

#  Train the model
python perceptron.py -train -i $CORPORA/train.col -m model
#python perceptron.py -train -i $CORPORA/train_top5000.col -m model

# Test the model
python perceptron.py -test -i $CORPORA/dev.col -m model -o prediction.col
#python perceptron.py -test -i $CORPORA/dev_top5000.col -m model -o prediction.col

# Evaluate the results
python perceptron.py -ev -i prediction.col -o evaluation.txt

rm $CORPORA/train_top5000.col
rm $CORPORA/dev_top5000.col
