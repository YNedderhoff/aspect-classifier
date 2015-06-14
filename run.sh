#!/bin/bash

CORPORA="../team-lab-ss2015/data/pos"

train=0
test=0
evaluate=0
tag=1

#head -20000 $CORPORA/train.col >> $CORPORA/train_top5000.col
#head -20000 $CORPORA/dev.col >> $CORPORA/dev_top5000.col

if [ "$train" = 1 ]; then
    #python -u tagger.py -train -i $CORPORA/train.col -e 5 -m model
    #python -u tagger.py -train -i $CORPORA/train_top5000.col -t $p -e 5 -m $MODELS/model$COUNTER
    python -u tagger.py -train -i $CORPORA/train.col -e 10 -m model -decrease-alpha -shuffle-tokens -batch-training
fi

# Test the model
if [ "$test" = 1 ]; then
    python -u tagger.py -test -i $CORPORA/dev.col -m model -o prediction.col
    #python -u tagger.py -test -i $CORPORA/dev_top5000.col -m $MODELS/model$COUNTER -o $PREDICTIONS/prediction$COUNTER.col
    #python tagger.py -test -i $CORPORA/dev_top5000.col -m model -o prediction.col
fi

# Evaluate the results
if [ "$evaluate" = 1 ]; then
    python -u tagger.py -ev -i prediction.col -o evaluation.txt
    #python -u tagger.py -ev -i $CORPORA/test_stuff/nn.col -o evaluation.txt
    #python -u tagger.py -ev -i $CORPORA/test_stuff/leer.col -o evaluation.txt
fi

# Test the model
if [ "$tag" = 1 ]; then
    python -u tagger.py -tag -i $CORPORA/test-nolabels.col -m model -o prediction.col
    #python -u tagger.py -test -i $CORPORA/dev_top5000.col -m $MODELS/model$COUNTER -o $PREDICTIONS/prediction$COUNTER.col
    #python tagger.py -test -i $CORPORA/dev_top5000.col -m model -o prediction.col
fi

# Tag plain text file

#rm $CORPORA/train_top5000.col
#rm $CORPORA/dev_top5000.col
