#!/bin/bash

CORPORA="../team-lab-ss2015/data/pos"

MODELS="models"
PREDICTIONS="predictions"
EVALUATIONS="/mount/studenten/projekt-cl/WS-2013-2014/student-workspace/nedderyk/teamlabproject15/evaluations"

affixes=0
train=1
test=1
evaluate=1

#head -20000 $CORPORA/train.col >> $CORPORA/train_top5000.col
#head -20000 $CORPORA/dev.col >> $CORPORA/dev_top5000.col

# Finding possible features, e.g. Affixes.
if [ "$affixes" = 1 ]; then
    python -u tagger.py -feat -i $CORPORA/train.col
fi

COUNTER=0

while read p; do
#  Train the model
    let COUNTER=COUNTER+1

    if [ "$COUNTER" -ge "$1" ]  && [ "$COUNTER" -lt "$2" ]; then
   

        if [ "$train" = 1 ]; then
            python -u tagger.py -train -i $CORPORA/train.col -t $p -e 5 -m $MODELS/model$COUNTER
            #python -u tagger.py -train -i $CORPORA/train_top5000.col -t $p -e 5 -m $MODELS/model$COUNTER
            #python tagger.py -train -i $CORPORA/train_top5000.col -e 5 -m model
        fi

        # Test the model
        if [ "$test" = 1 ]; then
            python -u tagger.py -test -i $CORPORA/dev.col -m $MODELS/model$COUNTER -o $PREDICTIONS/prediction$COUNTER.col
            #python -u tagger.py -test -i $CORPORA/dev_top5000.col -m $MODELS/model$COUNTER -o $PREDICTIONS/prediction$COUNTER.col
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
    fi

done <lmi.txt

#rm $CORPORA/train_top5000.col
#rm $CORPORA/dev_top5000.col
