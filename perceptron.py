import codecs
import time

import modules.token as tk

from modules.evaluation import evaluate
from modules.affixes import findAffixes

def extractFeatures(filein):

	featvec = {}
	featvec["initial_token"] = len(featvec.keys())

	for sentence in tk.sentences(codecs.open(filein,encoding='utf-8')):
		for token in sentence:
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

class posTagger(object):
	def __init__(self):
		pass

	def train(self, filein):
		# Data structure which maps features to dimensions

		print "\tExtracting features"
		y0 = time.time()

		featvec = extractFeatures(args.infile)

		y1 = time.time()
		print "\t\t"+str(y1-y0)+" sec."

		z0 = time.time()

		print "\tRead data and create Tokens (including feature vectors)"
	
		for sentence in tk.sentences(codecs.open(args.infile,encoding='utf-8')):
			for tid,token in enumerate(sentence):

				# Create sparse feature vector representation for each token
				if tid == 0:
					token.createFeatureVector(featvec, sentence[tid], None, sentence[tid+1])
				elif tid == len(sentence)-1:
					token.createFeatureVector(featvec, sentence[tid], sentence[tid-1], None)
				else:
					token.createFeatureVector(featvec, sentence[tid], sentence[tid-1], sentence[tid+1])
	
		z1 = time.time()
		print "\t\t"+str(z1-z0)+" sec."
	def test(self):
		pass

if __name__=='__main__':
	t0 = time.time()

	import argparse
	argpar = argparse.ArgumentParser(description='')

	mode = argpar.add_mutually_exclusive_group(required=True)
	mode.add_argument('-feat',dest='features',action='store_true',help='run in feature finding mode')
	mode.add_argument('-train',dest='train',action='store_true',help='run in training mode')
	mode.add_argument('-test',dest='test',action='store_true',help='run in test mode')
	mode.add_argument('-ev',dest='evaluate',action='store_true',help='run in evaluation mode')

	argpar.add_argument('-i','--infile',dest='infile',help='infile',required=True)
	#argpar.add_argument('-g','--gold',dest='gold',help='gold',required=True)
	#argpar.add_argument('-p','--prediction',dest='prediction',help='prediction',required=True)
	argpar.add_argument('-o','--output',dest='outputfile',help='output file',default='output.txt')
	args = argpar.parse_args()

	t = posTagger()

	if args.features:
		print "Running in feature mode\n"
		# find the most occuring prefixes and affixes
		findAffixes(args.infile, 5)
	elif args.train:
		print "Running in training mode\n"
		t.train(args.infile)
	elif args.test:
		print "Running in test mode\n"
		pass
	elif args.evaluate:
		print "Running in evaluation mode\n"

		outstream = open(args.outputfile,'w')
		evaluate(args.infile, outstream)
		outstream.close()

	t1 = time.time()
	print "\n\tDone. Time: "+ str(t1-t0) + "sec.\n"


