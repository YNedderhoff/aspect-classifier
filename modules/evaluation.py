import time

def evaluate(posDict, outfile):
	
	t0 = time.time()

	print "\tEvaluate predictions"

	uniqueTags = {}
	uniqueTagsScores = {}
	correctPredictions = 0

	for key in posDict:

		# creates a dictionary with every existing tag (either existing only in gold, only in 
		# prediction, or both) the key and a dictionary each as the value containing TP, FN, FP
		# as the key and zero as the value.

		if posDict[key][0] not in uniqueTags.keys():
			uniqueTags[posDict[key][0]] = {'TP':0,'FN':0,'FP':0}
		if posDict[key][1] not in uniqueTags.keys():
			uniqueTags[posDict[key][1]] = {'TP':0,'FN':0,'FP':0}

	for key in posDict:

		# Computes TP, FN and FP for each unique tag.

		if posDict[key][0] == posDict[key][1]:
			correctPredictions+=1
			uniqueTags[posDict[key][0]]['TP']+=1
		else:
			uniqueTags[posDict[key][0]]['FN']+=1
			uniqueTags[posDict[key][1]]['FP']+=1

	for pos in uniqueTags.keys():

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
	predictionCount = len(posDict)
	
	for pos in uniqueTagsScores.keys():
		precisionSum += uniqueTagsScores[pos]['Precision']
		recallSum += uniqueTagsScores[pos]['Recall']
		fscoreSum += uniqueTagsScores[pos]['F-Score']

	overallPrecision = precisionSum/float(len(uniqueTagsScores))
	overallRecall = recallSum/float(len(uniqueTagsScores))
	overallFscore = fscoreSum/float(len(uniqueTagsScores))

	overallAccuracy = (float(correctPredictions)/float(predictionCount))*100
	falseTags = predictionCount-correctPredictions

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

