#!/bin/bash

CORPORA="../team-lab-ss2015/data/pos"

affixes=0
train=1
test=0
evaluate=0

head -20000 $CORPORA/train.col >> $CORPORA/train_top5000.col
head -20000 $CORPORA/dev.col >> $CORPORA/dev_top5000.col
#1178

# Finding possible features, e.g. Affixes.
if [ "$affixes" = 1 ]; then
    python -u tagger.py -feat -i $CORPORA/train.col
fi

if [ "$train" = 1 ]; then
    #python -u tagger.py -train -i $CORPORA/train.col -e 5 -m model
    #python -u tagger.py -train -i $CORPORA/train_top5000.col -t $p -e 5 -m $MODELS/model$COUNTER
    python -u tagger.py -train -i $CORPORA/train_top5000.col -e 10 -m model -t1 5 -t2 5 -t3 5 -t4 5 -t5 5 -t6 5
fi

# Test the model
if [ "$test" = 1 ]; then
    python -u tagger.py -test -i $CORPORA/dev.col -m model -o prediction.col
    #python -u tagger.py -test -i $CORPORA/dev_top5000.col -m $MODELS/model$COUNTER -o $PREDICTIONS/prediction$COUNTER.col
    #python tagger.py -test -i $CORPORA/dev_top5000.col -m model -o prediction.col
    rm -f $MODELS/model$COUNTER
fi

# Evaluate the results
if [ "$evaluate" = 1 ]; then
    python -u tagger.py -ev -i prediction.col -o evaluation.txt
    #python -u tagger.py -ev -i $CORPORA/test_stuff/nn.col -o evaluation.txt
    #python -u tagger.py -ev -i $CORPORA/test_stuff/leer.col -o evaluation.txt
fi

rm $CORPORA/train_top5000.col
rm $CORPORA/dev_top5000.col
