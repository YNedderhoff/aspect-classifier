#!/bin/bash

CORPORA="../team-lab-ss2015/data/pos"

MODELS="models"
PREDICTIONS="predictions"
EVALUATIONS="/mount/projekte50/projekte/semrel/Users/moritz/TeamLab/git/evaluations2"

affixes=0
train=1
test=1
evaluate=1

head -200000 $CORPORA/train.col >> $CORPORA/train_top5000.col
head -200000 $CORPORA/dev.col >> $CORPORA/dev_top5000.col

# Finding possible features, e.g. Affixes.
if [ "$affixes" = 1 ]; then
    python -u tagger.py -feat -i $CORPORA/train.col
fi

COUNTER=$1

while [ "$COUNTER" -lt "$2" ]; do
#  Train the model
    let COUNTER=COUNTER+1

    if [ "$train" = 1 ]; then
        #python -u tagger.py -train -i $CORPORA/train.col -l $COUNTER -e 5 -m $MODELS/model$COUNTER
        python -u tagger.py -train -i $CORPORA/train_top5000.col -l $COUNTER -e 5 -m $MODELS/model$COUNTER
        #python tagger.py -train -i $CORPORA/train_top5000.col -e 5 -m model
    fi

    # Test the model
    if [ "$test" = 1 ]; then
        #python -u tagger.py -test -i $CORPORA/dev.col -m $MODELS/model$COUNTER -o $PREDICTIONS/prediction$COUNTER.col
        python -u tagger.py -test -i $CORPORA/dev_top5000.col -m $MODELS/model$COUNTER -o $PREDICTIONS/prediction$COUNTER.col
        #python tagger.py -test -i $CORPORA/dev_top5000.col -m model -o prediction.col
        rm -f $MODELS/model$COUNTER
    fi

    # Evaluate the results
    if [ "$evaluate" = 1 ]; then
        python -u tagger.py -ev -i $PREDICTIONS/prediction$COUNTER.col -o $EVALUATIONS/evaluation$COUNTER.txt
        #python -u tagger.py -ev -i $CORPORA/test_stuff/nn.col -o evaluation.txt
        #python -u tagger.py -ev -i $CORPORA/test_stuff/leer.col -o evaluation.txt
        rm -f $PREDICTIONS/prediction$COUNTER.col
    fi
done

rm $CORPORA/train_top5000.col
rm $CORPORA/dev_top5000.col
