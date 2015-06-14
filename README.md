# perceptron-pos-tagger
POS-Tagger (Perceptron), developed in the NLP Team Laboratory course (SS 15), University of Stuttgart

This perceptron part-of-speech tagger uses the following features:

 - is a word uppercased or not?
 - is a word capitalized or not?
 - the lowercased word form
 - the word length
 - the position of the word in the sentence
 - the prefixes of the word (lengths 2 to 5) 
 - the suffixes of the word (lengths 2 to 5) 
 - other letter combinations inside the word

The file tagger.py has the following parameters:

[-h] (-train | -test | -ev | -tag) -i IN_FILE [-e EPOCHS]
                 [-m MODEL] [-o OUTPUT_FILE] [-t1 TOP_X_FORM]
                 [-t2 TOP_X_WORD_LEN] [-t3 TOP_X_POSITION] [-t4 TOP_X_PREFIX]
                 [-t5 TOP_X_SUFFIX] [-t6 TOP_X_LETTERCOMBS] [-decrease-alpha]
                 [-shuffle-tokens] [-batch-training]

As you can see, this part-of-speech tagger can be run in 4 different modes: -train, -test, ev, and -tag.

-train

If you want to train your own model, you need a training corpus. It should consist of two tab-seperated columns, which are the word in the first column and the gold-tag in the second column. After every sentence, there needs to be an empty line.
You have to specify the number of training iterations (-e) and the name of the model file (-m) you want to create.
If you want, you can specify some optional parameters for the training. To reduce training time, you can cut out some weak features (ranked by local mutual information). This is implemented by using the top x features of FORM, WORD_LEN, POSITION, PREFIX, SUFFIX,LETTERCOMBS (as described above), rather than all of them. If you don't specify the -t parameters, every feature of this group will be used.
Additionally, you can enable a constant decreasing of the alpha (smooth the adjustments of the weight vector during the epochs), shuffeling of the tokens after every epoch, and batch-training.

An example call could be:

python -u tagger.py -train -i train.col -e 10 -m model -decrease-alpha -shuffle-tokens -batch-training

Here, you would use all features, and enable alpha decreasing, token shuffeling and batch training.

-test

If you want to test a model, you need a development file in the same format as the training file. Then you start the tagger.py with the parameter -test, the development file, the model that should be used, and the prediction file you want to create.
The prediction file is going to consist of three tab seperated columns, which are the word in the first column, the gold-tag in the second column, and the predicted tag in the third column.

An example call could be:

python -u tagger.py -test -i dev.col -m model -o prediction.col

-ev

If you want to evaluate a prediction file, you have to use the flag -ev. Other parameters are the prediction file you want to evaluate, and the evaluation file to which you want to write the results.

An example call could be:

python -u tagger.py -ev -i prediction.col -o evaluation.txt

-tag

If you have a good model and want to use it to tag plain text, you need to use the -tag flag. The input format needs to be in the same format as described above, but only the first column, since there are no gold-tags. The other parameters are the model you want to use and the prediction file you want to create.

An example call could be:

python -u tagger.py -tag -i test-nolabels.col -m model -o prediction.col
