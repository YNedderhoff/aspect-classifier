import codecs
import time

import modules.token as tk

from modules.evaluation import evaluate
from modules.affixes import findAffixes

def extractFeatures(filein):

	featvec = {}
	featvec["initial_token"] = len(featvec.keys())

	for sid, sentence in enumerate(tk.sentences(codecs.open(filein,encoding='utf-8'))):
		for tid,token in enumerate(sentence):
			# pos features
			"""
			if not "prev_pos_"+str(token.gold_pos) in featvec: featvec["prev_pos_"+str(token.gold_pos)] = len(featvec.keys())
			if not "prev_pos_"+str(token.predicted_pos) in featvec: featvec["prev_pos_"+str(token.predicted_pos)] = len(featvec.keys())
			"""
			# form features

			if not "current_form_"+str(token.form) in featvec: featvec["current_form_"+str(token.form)] = len(featvec)
			if not "prev_form_"+str(token.form) in featvec: featvec["prev_form_"+str(token.form)] = len(featvec)
			if not "next_form_"+str(token.form) in featvec: featvec["next_form_"+str(token.form)] = len(featvec)


	return featvec

if __name__=='__main__':
	t0 = time.time()

	import argparse
	argpar = argparse.ArgumentParser(description='')
	argpar.add_argument('-i','--infile',dest='infile',help='infile',required=True)
	#argpar.add_argument('-g','--gold',dest='gold',help='gold',required=True)
	#argpar.add_argument('-p','--prediction',dest='prediction',help='prediction',required=True)
	argpar.add_argument('-o','--output',dest='outputfile',help='output file',required=True)
	args = argpar.parse_args()

	outstream = open(args.outputfile,'w')

	# find the most occuring prefixes and affixes
	findAffixes(args.infile, 5)	

	# Data structure which maps features to dimensions

	print "\tExtracting features"
	y0 = time.time()

	featvec = extractFeatures(args.infile)

	y1 = time.time()
	print "\t\t"+str(y1-y0)+" sec."

	z0 = time.time()
	
	posDict = {}
	counter=0

	print "\tRead data and create Tokens (including feature vectors)"
	
	for sid, sentence in enumerate(tk.sentences(codecs.open(args.infile,encoding='utf-8'))):
		for tid,token in enumerate(sentence):

			# Creating posDict for evaluation
			posDict[counter] = [token.gold_pos, token.predicted_pos]

			# Create sparse feature vector representation for each token
			if tid == 0:
				token.createFeatureVector(featvec, sentence[tid], None, sentence[tid+1])
			elif tid == len(sentence)-1:
				token.createFeatureVector(featvec, sentence[tid], sentence[tid-1], None)
			else:
				token.createFeatureVector(featvec, sentence[tid], sentence[tid-1], sentence[tid+1])
			counter+=1
	
	z1 = time.time()
	print "\t\t"+str(z1-z0)+" sec."

	evaluate(posDict, outstream)

	outstream.close()

	t1 = time.time()
	print "\n\tDone. Time: "+ str(t1-t0) + "sec."


