#!/bin/bash

CORPORA="../team-lab-ss2015/data/pos"

affixes=0
train=0
test=0
evaluate=1

head -1000 $CORPORA/train.col >> $CORPORA/train_top5000.col
head -1000 $CORPORA/dev.col >> $CORPORA/dev_top5000.col

# Finding possible features, e.g. Affixes.
if [ "$affixes" = 1 ]; then
    python -u tagger.py -feat -i $CORPORA/train.col
fi


#  Train the model
if [ "$train" = 1 ]; then
    #python -u tagger.py -train -i $CORPORA/train.col -e 10 -m model
    python tagger.py -train -i $CORPORA/train_top5000.col -e 5 -m model
fi

# Test the model
if [ "$test" = 1 ]; then
    #python -u tagger.py -test -i $CORPORA/dev.col -m model -o prediction.col
    python tagger.py -test -i $CORPORA/dev_top5000.col -m model -o prediction.col
fi

# Evaluate the results
if [ "$evaluate" = 1 ]; then
    python -u tagger.py -ev -i prediction.col -o evaluation.txt
    #python -u tagger.py -ev -i $CORPORA/test_stuff/nn.col -o evaluation.txt
    #python -u tagger.py -ev -i $CORPORA/test_stuff/leer.col -o evaluation.txt
fi

rm $CORPORA/train_top5000.col
rm $CORPORA/dev_top5000.col