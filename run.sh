#!/bin/bash

#START=$(date +%s%N)

CORPORA="../team-lab-ss2015/data/pos"

head -200 $CORPORA/train.col >> $CORPORA/train_top5000.col
head -200 $CORPORA/dev.col >> $CORPORA/dev_top5000.col

# Finding possible features, e.g. Affixes.
#python perceptron.py -feat -i $CORPORA/train.col

#  Train the model
#python perceptron.py -train -i $CORPORA/train.col -m modelfile
python perceptron.py -train -i $CORPORA/train_top5000.col -m modelfile

# Test the model
#python perceptron.py -test -i $CORPORA/dev.col -m modelfile
#python perceptron.py -test -i $CORPORA/dev_top5000.col -m modelfile -o train_output.txt

# Evaluate the results
python perceptron.py -ev -i train_output.txt -m modelfile -o evaluation.txt

rm $CORPORA/train_top5000.col
rm $CORPORA/dev_top5000.col

#END=$(date +%s%N)
#DIFF=$(( $END - $START ))
#echo "It took $DIFF seconds"
#echo $END
#echo $(date +%s%N)
