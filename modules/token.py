class Token(object):
	def __init__( self, line ):
		entries = line.split('\t')
		self.form = entries[0].lower()
		self.gold_pos = entries[1]
		self.predicted_pos = entries [3]

	def createFeatureVector(self, featvec, currentToken, previousToken, nextToken):
		self.sparseFeatvec = {}
		
		#if previousToken: self.sparseFeatvec[featvec["prev_pos_"+str(previousToken.gold_pos)]] = 1
		
		self.sparseFeatvec[featvec["current_form_"+currentToken.form]] = 1
		if previousToken: self.sparseFeatvec[featvec["prev_form_"+previousToken.form]] = 1
		if nextToken: self.sparseFeatvec[featvec["next_form_"+nextToken.form]] = 1
		

		if not previousToken: self.sparseFeatvec[featvec["initial_token"]] = 1

def sentences( filestream ):

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
