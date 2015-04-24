class Token(object):
	def __init__( self, line ):

		# Splits line tab-wise, writes the values in parameters

		entries = line.split('\t')
		if len(entries) == 4:
			self.form = entries[0].lower()
			self.gold_pos = entries[1]
			self.predicted_pos = entries [3]

		elif len(entries) > 4: print "\tInput file not in expected format: Too many columns"
		else: print "\tInput file not in expected format: Too many columns"

	def createFeatureVector(self, featvec, currentToken, previousToken, nextToken):

		# creates a sparse representation of the feature vector (featvec)

		self.sparseFeatvec = {}
		
		# The current token
		self.sparseFeatvec[featvec["current_form_"+currentToken.form]] = 1

		# If exists, the previous token; else it is the initial token of the phrase
		if previousToken: self.sparseFeatvec[featvec["prev_form_"+previousToken.form]] = 1
		else: self.sparseFeatvec[featvec["initial_token"]] = 1

		# if exists, the next token
		if nextToken: self.sparseFeatvec[featvec["next_form_"+nextToken.form]] = 1

def sentences( filestream ):

	# A generator to read a file sentence-wise and generate a Token object for each line
	# A list of Token objects of every sentence is yielded

	sentence = []
	for line in filestream:
		line = line.rstrip()
		if line:
			sentence.append(Token(line))
		elif sentence:
			yield sentence
			sentence = []
	if sentence:
		yield sentence
