import time
import codecs
import token as tk

def evaluate(filein, outfile):
	
	t0 = time.time()

	print "\tEvaluate predictions"

	posDict = {}
	counter=0

	predictionCount = 0
	uniqueTags = {}
	uniqueTagsScores = {}
	correctPredictions = 0

	for sentence in tk.sentences(codecs.open(filein,encoding='utf-8')):
		for tid,token in enumerate(sentence):
			
			predictionCount += 1

			# uniqueTags contains every existing POS tag, whether it exists only in
			# gold, predicted, or both. The value is the dict {'TP':0,'FN':0,'FP':0}

			if token.gold_pos not in uniqueTags:
				uniqueTags[token.gold_pos] = {'TP':0,'FN':0,'FP':0}
			if token.predicted_pos not in uniqueTags:
				uniqueTags[token.predicted_pos] = {'TP':0,'FN':0,'FP':0}

			# if the prediction was correct, TP of the gold POS is increased by 1
			# if not, the FN of the gold POS and FP of the predicted pos are increased by 1

			if token.gold_pos == token.predicted_pos:
				correctPredictions+=1
				uniqueTags[token.gold_pos]['TP']+=1
			else:
				uniqueTags[token.gold_pos]['FN']+=1
				uniqueTags[token.predicted_pos]['FP']+=1

	for pos in uniqueTags:

		# Computes Precision, Recall, Accuracy and F-Score for each Tag based on TP, FN, FP.

		uniqueTagsScores[pos]={'Precision':0.00, 'Recall':0.00, 'Accuracy':0.00, 'F-Score':0.00}
		if uniqueTags[pos]['TP']+uniqueTags[pos]['FP'] == 0:
			uniqueTagsScores[pos]['Precision'] = 0.00
		else:
			uniqueTagsScores[pos]['Precision']=round((float(uniqueTags[pos]['TP']))/(float(uniqueTags[pos]['TP'])+float(uniqueTags[pos]['FP']))*100.00, 2)

		if uniqueTags[pos]['TP']+uniqueTags[pos]['FN'] == 0:
			uniqueTagsScores[pos]['Recall'] = 0.00
		else: uniqueTagsScores[pos]['Recall']=round((float(uniqueTags[pos]['TP']))/(float(uniqueTags[pos]['TP'])+float(uniqueTags[pos]['FN']))*100.00, 2)

		if uniqueTags[pos]['TP']+uniqueTags[pos]['FP']+uniqueTags[pos]['FN'] == 0:
			uniqueTagsScores[pos]['Accuracy'] = 0.00
		else: uniqueTagsScores[pos]['Accuracy']=round(float(uniqueTags[pos]['TP'])/(float(uniqueTags[pos]['TP'])+float(uniqueTags[pos]['FN'])+float(uniqueTags[pos]['FP']))*100.00, 2)

		if uniqueTagsScores[pos]['Precision']+uniqueTagsScores[pos]['Recall'] == 0.00:
			uniqueTagsScores[pos]['F-Score'] = 0.00
		else: uniqueTagsScores[pos]['F-Score'] = round((2*float(uniqueTagsScores[pos]['Precision'])*float(uniqueTagsScores[pos]['Recall']))/(float(uniqueTagsScores[pos]['Precision'])+float(uniqueTagsScores[pos]['Recall'])), 2)
	

	precisionSum = 0.0
	recallSum = 0.0
	fscoreSum = 0.0

	falseTags = predictionCount-correctPredictions
	
	for pos in uniqueTagsScores:
		precisionSum += uniqueTagsScores[pos]['Precision']
		recallSum += uniqueTagsScores[pos]['Recall']
		fscoreSum += uniqueTagsScores[pos]['F-Score']

	overallPrecision = precisionSum/float(len(uniqueTagsScores))
	overallRecall = recallSum/float(len(uniqueTagsScores))
	overallFscore = fscoreSum/float(len(uniqueTagsScores))

	overallAccuracy = (float(correctPredictions)/float(predictionCount))*100

	t1 = time.time()
	print "\t\t"+str(t1-t0)+" sec."

	print "\tWrite evaluation results to file"
	
	z0 = time.time()	
	
	print >> outfile, "Total Predictions:\t"+str(predictionCount)
	print >> outfile, "Correct Predictions:\t"+str(correctPredictions)
	print >> outfile, "False Predictions:\t"+str(falseTags)
	print >> outfile, ""
	print >> outfile, "Overall Accuracy:\t"+str(overallAccuracy)
	print >> outfile, "Overall Precision:\t"+str(overallPrecision)
	print >> outfile, "Overall Recall:\t"+str(overallRecall)
	print >> outfile, "Overall F-Score:\t"+str(overallFscore)
	print >> outfile, ""

	print >> outfile, "Tagwise Accuracy, Precision, Recall and F-Score:\n"
	for pos in uniqueTagsScores.keys():
		print >> outfile, pos+"\tAccuracy: "+str(uniqueTagsScores[pos]['Accuracy'])+"\tPrecision: "+str(uniqueTagsScores[pos]['Precision'])+"\tRecall: "+str(uniqueTagsScores[pos]['Recall'])+"\tF-Score: "+str(uniqueTagsScores[pos]['F-Score'])
	
	z1 = time.time()
	print "\t\t"+str(z1-z0)+" sec."

