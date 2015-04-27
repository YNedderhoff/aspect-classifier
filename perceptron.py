import codecs
import time
import cPickle
import gzip

import modules.token as tk
import modules.classifier as cl

from modules.evaluation import evaluate
from modules.affixes import findAffixes


class posTagger(object):
	def __init__(self):
		pass

	def save(self, filename, model):
		stream = gzip.open(filename, "wb")
		cPickle.dump(model, stream)
		stream.close()

	def load(self, filename):
		stream = gzip.open(filename, "rb")
		self.model = cPickle.load(stream)
		stream.close()
	

	def train(self, filein, fileout, max_iterations):
		# Data structure which maps features to dimensions

		print "\tTraining file: "+filein

		print "\tExtracting features"
		y0 = time.time()

		featvec = self.extractFeatures(filein)

		y1 = time.time()
		print "\t\t"+str(y1-y0)+" sec."

		z0 = time.time()

		print "\tCreate Tokens (including feature vectors)"
		tokens = []
		tagset = set()
		for sentence in tk.sentences(codecs.open(filein,encoding='utf-8')):
			for tid,token in enumerate(sentence):

				# Create sparse feature vector representation for each token
				if tid == 0:
					try:
						token.createFeatureVector(featvec, sentence[tid], None, sentence[tid+1])
					except IndexError: # happens if sentence length is 1
						token.createFeatureVector(featvec, sentence[tid], None, None)
				elif tid == len(sentence)-1:
					token.createFeatureVector(featvec, sentence[tid], sentence[tid-1], None)
				else:
					token.createFeatureVector(featvec, sentence[tid], sentence[tid-1], sentence[tid+1])
				tokens.append(token)
				tagset.add(token.gold_pos)

		print "\tCreate Classifiers"
		classifiers = {}
		for tag in tagset:
			classifiers[tag] = cl.classifier(tag, len(featvec))
		
		for i in range(max_iterations):
			for ind,t in enumerate(tokens):
				if ind % 100 == 0:
					print "\t\t"+ str(ind) + "\t" + str(len(tokens))
				expanded_feat_vec = t.expandFeatVec(len(featvec))
				arg_max = ["", 0.0]
				for tag in classifiers:
					temp = classifiers[tag].classify(expanded_feat_vec)
					if temp > arg_max[1]:
						arg_max[0] = tag
						arg_max[1] = temp

				if arg_max[0] != t.gold_pos:
					classifiers[t.gold_pos].adjust_weights(expanded_feat_vec, True, 0.1)
					classifiers[arg_max[0]].adjust_weights(expanded_feat_vec, False, 0.1)
		self.save(fileout, classifiers)


		z1 = time.time()
		print "\t\t"+str(z1-z0)+" sec."

	def test(self, filein, model, fileout):
		classifiers = self.load(model)
		print len(classifiers)
		print "\t Test file: "+filein

		# Data structure which maps features to dimensions
		

		print "\tExtracting features"
		y0 = time.time()

		featvec = self.extractFeatures(filein)

		y1 = time.time()
		print "\t\t"+str(y1-y0)+" sec."

		z0 = time.time()

		print "\tCreate Tokens (including feature vectors)"
		tokens = []
		tagset = set()
		for sentence in tk.sentences(codecs.open(filein,encoding='utf-8')):
			for tid,token in enumerate(sentence):

				# Create sparse feature vector representation for each token
				if tid == 0:
					try:
						token.createFeatureVector(featvec, sentence[tid], None, sentence[tid+1])
					except IndexError: # happens if sentence length is 1
						token.createFeatureVector(featvec, sentence[tid], None, None)
				elif tid == len(sentence)-1:
					token.createFeatureVector(featvec, sentence[tid], sentence[tid-1], None)
				else:
					token.createFeatureVector(featvec, sentence[tid], sentence[tid-1], sentence[tid+1])
				tokens.append(token)
				tagset.add(token.gold_pos)

		#Temporarily save classification to file for evaluation:
		output = open(fileout, "w")
		for t in tokens:
			t.gold_pos = t.predicted_pos
			expanded_feat_vec = t.expandFeatVec(len(featvec))
			arg_max = ["", 0.0]
			for tag in classifiers:
				temp = classifiers[tag].classify(expanded_feat_vec)
				if temp > arg_max[1]:
					arg_max[0] = tag
					arg_max[1] = temp
			t.predicted_pos = arg_max[0]
			output.write(t.form.encode("utf-8") + "\t" + t.gold_pos.encode("utf-8") + "\t" + \
				     t.predicted_pos.encode("utf-8") + "\n")
		output.close()
		z1 = time.time()
		print "\t\t"+str(z1-z0)+" sec."

	def extractFeatures(self, filein):

		self.featvec = {}
		self.featvec["initial_token"] = len(self.featvec.keys())

		for sentence in tk.sentences(codecs.open(filein,encoding='utf-8')):
			for token in sentence:
				# pos features
				"""
				if not "prev_pos_"+str(token.gold_pos) in featvec: featvec["prev_pos_"+str(token.gold_pos)] = len(featvec.keys())
				if not "prev_pos_"+str(token.predicted_pos) in featvec: featvec["prev_pos_"+str(token.predicted_pos)] = len(featvec.keys())
				"""
				# form features

				if not "current_form_"+token.form in self.featvec: self.featvec["current_form_"+token.form] = len(self.featvec)
				if not "prev_form_"+token.form in self.featvec: self.featvec["prev_form_"+token.form] = len(self.featvec)
				if not "next_form_"+token.form in self.featvec: self.featvec["next_form_"+token.form] = len(self.featvec)

		print "\t"+str(len(self.featvec))+" features extracted"
		return self.featvec

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
	argpar.add_argument('-m','--model',dest='model',help='model',required=True)
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
		t.train(args.infile, args.model, 1)
	elif args.test:
		print "Running in test mode\n"
		t.test(args.infile, args.model, args.outputfile)
	elif args.evaluate:
		print "Running in evaluation mode\n"

		outstream = open(args.outputfile,'w')
		evaluate(args.infile, outstream)
		outstream.close()

	t1 = time.time()
	print "\n\tDone. Time: "+ str(t1-t0) + "sec.\n"


