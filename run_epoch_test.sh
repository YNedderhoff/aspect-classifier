#!/bin/bash

CORPORA="../team-lab-ss2015/data/pos"

rm prediction_e*

# Finding possible features, e.g. Affixes.
#python tagger.py -feat -i $CORPORA/train.col

#  Train the model
python tagger.py -train -i $CORPORA/train.col -e 1 -m model_e1
python tagger.py -train -i $CORPORA/train.col -e 10 -m model_e10
python tagger.py -train -i $CORPORA/train.col -e 100 -m model_e100
python tagger.py -train -i $CORPORA/train.col -e 1000 -m model_e1000

# Test the model
python tagger.py -test -i $CORPORA/dev.col -m model_e1 -o prediction_e1.col
python tagger.py -test -i $CORPORA/dev.col -m model_e10 -o prediction_e10.col
python tagger.py -test -i $CORPORA/dev.col -m model_e100 -o prediction_e100.col
python tagger.py -test -i $CORPORA/dev.col -m model_e1000 -o prediction_e1000.col

# Evaluate the results
python tagger.py -ev -i prediction_e1.col -o evaluation_e1.txt
python tagger.py -ev -i prediction_e10.col -o evaluation_e10.txt
python tagger.py -ev -i prediction_e100.col -o evaluation_e100.txt
python tagger.py -ev -i prediction_e1000.col -o evaluation_e1000.txt

rm $CORPORA/train_top5000.col
rm $CORPORA/dev_top5000.col
