#!/bin/bash

CORPORA="../team-lab-ss2015/data/pos"

MODELS="models"
PREDICTIONS="predictions"
EVALUATIONS="/mount/projekte50/projekte/semrel/Users/moritz/TeamLab/git/evaluations_"$2

affixes=0
train=1
test=1
evaluate=1

head -20000 $CORPORA/train.col > $CORPORA/train_top5000b$2.col
head -20000 $CORPORA/dev.col > $CORPORA/dev_top5000b$2.col

# Finding possible features, e.g. Affixes.
if [ "$affixes" = 1 ]; then
    python -u tagger.py -feat -i $CORPORA/train.col
fi

COUNTER=0

while [ "$COUNTER" -lt "$1" ]; do
#  Train the model
    let COUNTER=COUNTER+$3

    if [ "$train" = 1 ]; then
        #python -u tagger.py -train -i $CORPORA/train.col -l $COUNTER -e 5 -m $MODELS/model$COUNTER
        python -u tagger.py -train -i $CORPORA/train_top5000b$2.col -e 10 -m $MODELS/model$2$COUNTER -t $COUNTER -f $2
        #python tagger.py -train -i $CORPORA/train_top5000.col -e 5 -m model
    fi

    # Test the model
    if [ "$test" = 1 ]; then
        #python -u tagger.py -test -i $CORPORA/dev.col -m $MODELS/model$COUNTER -o $PREDICTIONS/prediction$COUNTER.col
        python -u tagger.py -test -i $CORPORA/dev_top5000b$2.col -m $MODELS/model$2$COUNTER -o $PREDICTIONS/prediction$2$COUNTER.col
        #python tagger.py -test -i $CORPORA/dev_top5000.col -m model -o prediction.col
        rm -f $MODELS/model$2$COUNTER
    fi

    # Evaluate the results
    if [ "$evaluate" = 1 ]; then
        python -u tagger.py -ev -i $PREDICTIONS/prediction$2$COUNTER.col -o $EVALUATIONS/evaluation$COUNTER.txt
        #python -u tagger.py -ev -i $CORPORA/test_stuff/nn.col -o evaluation.txt
        #python -u tagger.py -ev -i $CORPORA/test_stuff/leer.col -o evaluation.txt
        rm -f $PREDICTIONS/prediction$2$COUNTER.col
    fi
done

rm $CORPORA/train_top5000b$2.col
rm $CORPORA/dev_top5000b$2.col
