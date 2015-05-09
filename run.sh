#!/bin/bash

CORPORA="../team-lab-ss2015/data/pos"

if [ -f "prediction.col" ]
then
	rm prediction.col
fi

head -1000 $CORPORA/train.col >> $CORPORA/train_top5000.col
head -1000 $CORPORA/dev.col >> $CORPORA/dev_top5000.col

# Finding possible features, e.g. Affixes.
#python tagger.py -feat -i $CORPORA/train.col

#  Train the model
#python tagger.py -train -i $CORPORA/train.col -e 10 -m model
#python tagger.py -train -i $CORPORA/train_top5000.col -e 5 -m model

# Test the model
#python tagger.py -test -i $CORPORA/dev.col -m model -o prediction.col
#python tagger.py -test -i $CORPORA/dev_top5000.col -m model -o prediction.col

# Evaluate the results
python tagger.py -ev -i leer.col -o evaluation.txt

rm $CORPORA/train_top5000.col
rm $CORPORA/dev_top5000.col
